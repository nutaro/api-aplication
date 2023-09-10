from datetime import datetime

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Roles(Base):

    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String, nullable=False, unique=True)


class Claims(Base):

    __tablename__ = 'claims'

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    description = Column(String, nullable=False, unique=True)
    active = Column(Boolean, nullable=False, default=True)

    user_claims = relationship("UsersClaims", back_populates="claims")


class Users(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    role = relationship("Roles")


class UsersClaims(Base):

    __tablename__ = 'user_claims'

    user_id = Column(Integer, ForeignKey('users.id'),
                     nullable=False, primary_key=True)
    claim_id = Column(Integer, ForeignKey('claims.id'),
                      nullable=False, primary_key=True)

    users = relationship("Users")
    claims = relationship("Claims", back_populates="user_claims")

    UniqueConstraint('claim_id', 'user_id',
                     name="user_claims_un")
