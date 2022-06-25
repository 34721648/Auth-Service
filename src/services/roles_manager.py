from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import UnmappedInstanceError

from db.config import db_session
from db.models import (
    RolesUsers,
    User,
)
from services.account import AccountService
from services.exceptions import RelationDoesntExists
from services.role import RoleService


class RolesManager:
    def __init__(
        self,
        db: SQLAlchemy,
        account_service: AccountService,
        role_service: RoleService,
    ):

        self.db = db
        self.account_service = account_service
        self.role_service = role_service

    def set_role(self, user_id: str, role_name: str) -> None:
        role_id = self.role_service.get_role_id_by_name(role_name)
        user_role = RolesUsers(user_id=user_id, role_id=role_id)

        with db_session(self.db) as session:
            session.add(user_role)

    def delete_role(self, user_id: str, role_name: str) -> None:
        role_id = self.role_service.get_role_id_by_name(role_name)
        user_role = RolesUsers.query.filter_by(user_id=user_id, role_id=role_id).first()
        try:
            with db_session(self.db) as session:
                session.delete(user_role)
        except UnmappedInstanceError:
            raise RelationDoesntExists

    def get_user_roles(self, user_id: str) -> list[RolesUsers]:
        return RolesUsers.query.filter_by(user_id=user_id).all()

    def is_superuser(self, user_id: str) -> bool:
        return User.query.filter_by(id=user_id).first().is_superuser
