import enum
import random
import uuid

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    backref,
    relationship,
)

from db.config import db


class SocialName(enum.Enum):
    google = 'google'


class Countries(enum.Enum):
    ru = 'ru'
    eu = 'eu'
    us = 'us'


def random_country():
    return random.choice([Countries.ru, Countries.eu, Countries.us])


def create_users_partition(target, connection, **kw) -> None:
    connection.execute(
        f"""
            CREATE TABLE IF NOT EXISTS "users_ru"
            PARTITION OF "users" FOR VALUES IN ('{Countries.ru}')
        """,
    )
    connection.execute(
        f"""
            CREATE TABLE IF NOT EXISTS "users_eu"
            PARTITION OF "users" FOR VALUES IN ('{Countries.eu}')
        """,
    )
    connection.execute(
        f"""
            CREATE TABLE IF NOT EXISTS "users_us"
            PARTITION OF "users" FOR VALUES IN ('{Countries.us}')
        """,
    )


class TimestampMixin:
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())


class Role(db.Model, TimestampMixin):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(20), unique=True)
    description = Column(String(255))


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'

    id = Column(BigInteger(), primary_key=True)
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'))
    role_id = Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'))


class User(db.Model, TimestampMixin):
    __tablename__ = 'users'
    __table_args__ = (
        {
            'postgresql_partition_by': 'LIST (country)',
            'listeners': [('after_create', create_users_partition)],
        }
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    is_superuser = Column(Boolean(), default=False)

    # For countries used random values currently (for learning purposes)
    country = Column(Enum(Countries), nullable=False, default=random_country)

    roles = relationship(
        'Role',
        secondary='roles_users',
        backref=backref('users', lazy='dynamic'),
    )

    def __repr__(self):
        return f'<User {self.login}>'


class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'))
    user_agent = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())


class Password(db.Model):
    __tablename__ = 'passwords'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'))
    password = Column(String(512), nullable=False)


class SocialAccount(db.Model):
    __tablename__ = 'social_users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'))
    social_id = Column(String(255), nullable=False, unique=True)
    social_name = Column(Enum(SocialName), nullable=False)
