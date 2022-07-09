import hashlib
import os
from typing import Optional

from flask_sqlalchemy import (
    Pagination,
    SQLAlchemy,
)
from sqlalchemy.exc import IntegrityError

from db.config import db_session
from db.models import (
    AuthType,
    Password,
    User,
    UserSession,
)
from services.exceptions import (
    UnvailableLogin,
    UserAlreadyExists,
    UserDoesntExists,
    WrongPassword,
)

SALT_SIZE = 32
HASH_ITERATIONS = 10000


class AccountService:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def registrate_user(
        self,
        login: str,
        password: str,
        email: str,
        auth_type: AuthType,
        is_superuser: bool = False,
    ) -> None:

        stored_hash = self._generate_password_hex_str(password)
        user = User(
            login=login,
            email=email,
            auth_type=auth_type,
            is_superuser=is_superuser,
        )
        try:
            with db_session(self.db) as session:
                session.add(user)
        except IntegrityError:
            raise UserAlreadyExists

        password = Password(user_id=user.id, password=stored_hash)
        with db_session(self.db) as session:
            session.add(password)

    def login(
        self,
        login: str,
        password: str,
    ):
        user = User.query.filter_by(login=login, auth_type=AuthType.default).first()
        if user is None:
            raise UserDoesntExists

        password_from_db = Password.query.filter_by(user_id=user.id).first()

        stored_bytes = bytes.fromhex(password_from_db.password)
        user_password_salt = stored_bytes[:SALT_SIZE]
        user_password_hash = stored_bytes[SALT_SIZE:]
        entered_password_hash = self._get_hash(password, user_password_salt)

        if entered_password_hash != user_password_hash:
            raise WrongPassword

        return True

    def edit_user_login(self, user_id: str, new_login: str):
        user = User.query.filter_by(id=user_id).first()
        try:
            with db_session(self.db):
                user.login = new_login
        except IntegrityError:
            raise UnvailableLogin

    def edit_user_password(self, user_id: str, new_password: str):
        user = User.query.filter_by(id=user_id).first()
        new_stored_hash = self._generate_password_hex_str(new_password)
        with db_session(self.db):
            user.password = new_stored_hash

    def get_user_by_login(self, login: str) -> str:
        return User.query.filter_by(login=login).first()

    def register_user_session(self, user_id: str, user_agent: str) -> None:
        user_session = UserSession(user_id=user_id, user_agent=user_agent)
        with db_session(self.db) as session:
            session.add(user_session)

    def get_user_sessions(
        self,
        user_id: str,
        page_size: Optional[int] = 10,
        page_number: Optional[int] = 1,
    ) -> Pagination:
        return UserSession.query.filter_by(user_id=user_id).paginate(
            page_number, page_size, error_out=False,
        )

    def _generate_password_hex_str(self, password: str) -> str:
        salt = os.urandom(SALT_SIZE)
        password_hash = self._get_hash(password, salt)
        return salt.hex() + password_hash.hex()

    def _get_hash(self, password: str, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, HASH_ITERATIONS)
