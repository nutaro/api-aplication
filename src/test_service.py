import pytest

from service import UserService, RoleService, ClaimService, UserClaimService
from models import Base


from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session


@pytest.fixture(scope="session")
def engine():
    url = "sqlite:///:memory:"
    return create_engine(url, echo=True)


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, tables):
    connection = engine.connect()
    connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    connection.close()


def test_create_user(db_session) -> None:
    user_service = UserService(db_session)
    first_user = user_service.create('victor', 'bla@bla.com', 'guy', '123')
    assert first_user.name == 'victor'
    assert isinstance(first_user.id, int)
    assert first_user.role.description == 'guy'


def test_create_user_with_same_role(db_session) -> None:
    user_service = UserService(db_session)
    first_user = user_service.create('victor', 'bla@bla.com', 'guy', '123')
    second_user = user_service.create('sergio', 'bla@lalala.com', 'guy', '123')
    assert first_user.role_id == second_user.role_id


def test_create_user_duplicated_email(db_session) -> None:
    user_service = UserService(db_session)
    user_service.create('victor', 'bla@bla.com', 'guy', '123')
    with pytest.raises(IntegrityError):
        user_service.create('sergio', 'bla@bla.com', 'guy', '123')


def test_create_role(db_session) -> None:
    role_service = RoleService(db_session)
    role = role_service.create('guy')
    assert role.description == 'guy'
    assert isinstance(role.id, int)


def test_duplicated_role(db_session) -> None:
    role_service = RoleService(db_session)
    role_service.create('guy')
    with pytest.raises(IntegrityError):
        role_service.create('guy')


def test_get_non_existing_role(db_session) -> None:
    role_service = RoleService(db_session)
    with pytest.raises(NoResultFound):
        role_service.get_by_description('lalalalal')


def test_get_role_by_description(db_session) -> None:
    role_service = RoleService(db_session)
    role = role_service.create('guy')
    assert role.id == role_service.get_by_description("guy").id


def test_create_claim(db_session) -> None:
    claim_service = ClaimService(db_session)
    claim = claim_service.create('profile')
    assert claim.description == "profile"
    assert isinstance(claim.id, int)


def test_duplicated_claim(db_session) -> None:
    claim_service = ClaimService(db_session)
    claim_service.create('profile')
    with pytest.raises(IntegrityError):
        claim_service.create('profile')


def test_get_non_existing_claim(db_session) -> None:
    claim_service = ClaimService(db_session)
    with pytest.raises(NoResultFound):
        claim_service.get_by_description('lalalalal')


def test_get_claim_by_description(db_session) -> None:
    claim_service = ClaimService(db_session)
    claim = claim_service.create('profile')
    assert claim.id == claim_service.get_by_description("profile").id


def test_get_claims_by_status(db_session) -> None:
    claim_service = ClaimService(db_session)
    claim_service.create('profile')
    claim_service.create('admin', active=False)
    claims = claim_service.get_by_status(True)
    assert claims[0][0].description == 'profile'


def test_get_claims_by_status_raises(db_session) -> None:
    claim_service = ClaimService(db_session)
    claim_service.create('admin', active=False)
    with pytest.raises(NoResultFound):
        claim_service.get_by_status(True)


def test_create_one_user_claim(db_session) -> None:
    user_service = UserService(db_session)
    user = user_service.create('victor', 'bla@bla.com', 'guy', '123')
    claim_service = ClaimService(db_session)
    claim = claim_service.create('profile')
    user_claim_service = UserClaimService(db_session)
    user_claim = user_claim_service.create(user.id, claim.id)
    assert user_claim.users.name == 'victor'
    assert user_claim.claims.description == 'profile'


def test_create_two_claims_one_user(db_session) -> None:
    user_service = UserService(db_session)
    user = user_service.create('victor', 'bla@bla.com', 'guy', '123')
    claim_service = ClaimService(db_session)
    claim = claim_service.create('profile')
    user_claim_service = UserClaimService(db_session)
    user_claim = user_claim_service.create(user.id, claim.id)
    claim = claim_service.create('password')
    user_claim = user_claim_service.create(user.id, claim.id)
    user_claims = user_claim_service.get_by_user_id(user.id)
    assert user_claim.users.name == 'victor'
    assert user_claims[1][0].claims.description == "password"
    assert len(user_claims) == 2


def test_create_two_users_one_claim(db_session) -> None:
    user_service = UserService(db_session)
    first_user = user_service.create('victor', 'bla@bla.com', 'guy', '123')
    second_user = user_service.create('sergio', 'bla@lala.com', 'guy', '123')
    claim_service = ClaimService(db_session)
    claim = claim_service.create('profile')
    user_claim_service = UserClaimService(db_session)
    user_claim_service.create(first_user.id, claim.id)
    user_claim_service.create(second_user.id, claim.id)
    user_claims = user_claim_service.get_by_claim_id(claim.id)
    assert user_claims[0][0].users.name == "victor"
    assert user_claims[1][0].users.name == "sergio"
    assert len(user_claims) == 2


def test_duplicated_users_claim(db_session) -> None:
    user_service = UserService(db_session)
    user = user_service.create('victor', 'bla@bla.com', 'guy', '123')
    claim_service = ClaimService(db_session)
    claim = claim_service.create('profile')
    user_claim_service = UserClaimService(db_session)
    user_claim_service.create(user.id, claim.id)
    with pytest.raises(IntegrityError):
        user_claim_service.create(user.id, claim.id)


def test_get_non_existing_users_claim_by_user(db_session) -> None:
    user_claim_service = UserClaimService(db_session)
    with pytest.raises(NoResultFound):
        user_claim_service.get_by_user_id(15)


def test_get_non_existing_users_claim_by_claim(db_session) -> None:
    user_claim_service = UserClaimService(db_session)
    with pytest.raises(NoResultFound):
        user_claim_service.get_by_claim_id(15)
