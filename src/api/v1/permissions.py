from functools import wraps
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity

from db.config import db
from services.account import AccountService
from services.role import RoleService
from services.roles_manager import RolesManager

role_service = RoleService(db)
account_service = AccountService(db)
roles_manager = RolesManager(db, account_service, role_service)


def role_required(role: str):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user_id = get_jwt_identity()
            is_superuser = roles_manager.is_superuser(user_id)
            roles_list = roles_manager.get_user_roles(user_id)

            roles_names = [role_service.get_role_name_by_id(role.id) for role in roles_list]

            if (role in roles_names) or is_superuser:
                return fn(*args, **kwargs)
            return {'msg': 'You have not permission!'}, HTTPStatus.FORBIDDEN
        return decorator

    return wrapper
