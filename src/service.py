import hashlib
import string
import random

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from models import Users, Roles, Claims, UsersClaims


class Service:  # pragma: no cover

    def __init__(self, session: Session) -> None:
        self._session = session

    def __exit__(self) -> None:  # pragma: no cover
        self._session.close()


class UserService(Service):

    @staticmethod
    def password_generator() -> str:
        special = "!@#$%^&*()"
        characters = list(string.ascii_letters + string.digits + special)
        random.shuffle(characters)
        password = []
        for i in range(14):
            password.append(random.choice(characters))
        random.shuffle(password)
        return "".join(password)

    def _hash_password(self, value: str) -> str:
        return hashlib.sha512(value.encode("utf-8")).hexdigest()

    def create(self, name: str, email: str, role: str, password) -> Users:
        hashed_password = self._hash_password(password)
        role = self._get_role(role)
        user = Users(name=name, email=email,
                     password=hashed_password, role=role)
        self._session.add(user)
        self._session.commit()
        return user

    def get_by_id(self, value: int) -> Users:
        statement = select(Users).where(Users.id == value)
        results = self._session.execute(statement)
        result = results.fetchone()
        if result is None:
            raise NoResultFound
        return result[0]

    def _get_role(self, description) -> Roles:
        role_service = RoleService(self._session)
        try:
            return role_service.get_by_description(description)
        except NoResultFound:
            return role_service.create(description)


class RoleService(Service):

    def create(self, description: str) -> Roles:
        role = Roles(description=description)
        self._session.add(role)
        self._session.commit()
        return role

    def get_by_description(self, value: str) -> Roles:
        statement = select(Roles).where(Roles.description == value)
        results = self._session.execute(statement)
        result = results.fetchone()
        if result is None:
            raise NoResultFound
        return result[0]


class ClaimService(Service):

    def create(self, description: str, active=True) -> Claims:
        claim = Claims(description=description, active=active)
        self._session.add(claim)
        self._session.commit()
        return claim

    def get_by_description(self, value: str) -> Claims:
        statement = select(Claims).where(Claims.description == value)
        results = self._session.execute(statement)
        result = results.fetchone()
        if result is None:
            raise NoResultFound
        return result[0]

    def get_by_status(self, value: bool) -> [Claims]:
        statement = select(Claims).where(Claims.active == value)
        results = self._session.execute(statement)
        result = results.fetchall()
        if len(result) == 0:
            raise NoResultFound
        return result


class UserClaimService(Service):

    def create(self, user_id: int, claim_id: int) -> UsersClaims:
        claim = UsersClaims(user_id=user_id, claim_id=claim_id)
        self._session.add(claim)
        self._session.commit()
        return claim

    def get_by_user_id(self, user_id: int) -> [UsersClaims]:
        statement = select(UsersClaims).where(UsersClaims.user_id == user_id)
        results = self._session.execute(statement)
        result = results.fetchall()
        if len(result) == 0:
            raise NoResultFound
        return result

    def get_by_claim_id(self, claim_id: int) -> [UsersClaims]:
        statement = select(UsersClaims).where(UsersClaims.claim_id == claim_id)
        results = self._session.execute(statement)
        result = results.fetchall()
        if len(result) == 0:
            raise NoResultFound
        return result
