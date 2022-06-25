from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from db.config import db_session
from db.models import Role
from services.exceptions import (
    RoleAlreadyExists,
    RoleDoesntExists,
)


class RoleService:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all_roles(self) -> list:
        return Role.query.all()

    def create_role(
        self,
        name: str,
        description: Optional[str] = None,
    ) -> Role:
        role = Role(
            name=name,
            description=description,
        )
        try:
            with db_session(self.db) as session:
                session.add(role)
        except IntegrityError:
            raise RoleAlreadyExists
        return role

    def edit_role(
        self,
        name: str,
        new_name: Optional[str] = None,
        new_description: Optional[str] = None,
    ) -> None:

        role = Role.query.filter_by(name=name).first()

        if new_name:
            try:
                with db_session(self.db):
                    role.name = new_name
            except IntegrityError:
                raise RoleAlreadyExists

        if new_description:
            with db_session(self.db):
                role.description = new_description

    def delete_role(self, name: str) -> None:
        role = Role.query.filter_by(name=name).first()
        try:
            with db_session(self.db) as session:
                session.delete(role)
        except UnmappedInstanceError:
            raise RoleDoesntExists

    def get_role_id_by_name(self, name: str) -> str:
        role = Role.query.filter_by(name=name).first()
        return role.id

    def get_role_name_by_id(self, role_id: str) -> str:
        role = Role.query.filter_by(id=role_id).first()
        return role.name
