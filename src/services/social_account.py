from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from db.config import db_session
from db.models import (
    SocialAccount,
    User,
)
from services.exceptions import (
    UserAlreadyExists,
    UserDoesntExists,
)


class SocialAccountService:
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db

    def login(self, social_id: str, social_name: SocialAccount) -> User:
        social_account = SocialAccount.query.filter_by(social_id=social_id, social_name=social_name).first()
        if social_account is None:
            raise UserDoesntExists

        social_account = SocialAccount.query.filter_by(social_id=social_id, social_name=social_name).first()
        return User.query.filter_by(id=social_account.user_id).first()

    def register_user(self, social_id: str, social_name: SocialAccount, email: str):
        user = User(login=email, email=email)
        try:
            with db_session(self.db) as session:
                session.add(user)
        except IntegrityError:
            raise UserAlreadyExists

        social_account = SocialAccount(user_id=user.id, social_id=social_id, social_name=social_name)
        with db_session(self.db) as session:
            session.add(social_account)
