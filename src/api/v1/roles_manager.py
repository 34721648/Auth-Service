from http import HTTPStatus

from flask_jwt_extended import jwt_required
from flask_restx import (
    Namespace,
    Resource,
)

from api.v1.models.shared_models import message_model
from api.v1.parsers.role_management_parsers import manage_role_parser
from api.v1.permissions import role_required
from db.config import db
from limiter import limiter
from services.account import AccountService
from services.exceptions import RelationDoesntExists
from services.role import RoleService
from services.roles_manager import RolesManager

role_management_api = Namespace('v1/role-management', description='Account operations')
role_management_api.models[message_model.name] = message_model

role_service = RoleService(db)
account_service = AccountService(db)
roles_manager = RolesManager(db, account_service, role_service)

role_management_api.authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header',
    },
}


@role_management_api.route('/set-role')
class SetRole(Resource):
    @limiter.limit('60 per minute')
    @jwt_required()
    @role_required('admin')
    @role_management_api.expect(manage_role_parser)
    @role_management_api.marshal_with(message_model)
    @role_management_api.doc(security='Bearer')
    def post(self):
        args = manage_role_parser.parse_args()
        roles_manager.set_role(args['user_id'], args['role_name'])
        return {'msg': 'Role successfully setted!'}, HTTPStatus.OK


@role_management_api.route('/delete-role')
class DeleteRole(Resource):
    @limiter.limit('60 per minute')
    @jwt_required()
    @role_required('admin')
    @role_management_api.expect(manage_role_parser)
    @role_management_api.marshal_with(message_model)
    @role_management_api.doc(security='Bearer')
    def delete(self):
        args = manage_role_parser.parse_args()
        try:
            roles_manager.delete_role(args['user_id'], args['role_name'])
        except RelationDoesntExists:
            return {'msg': 'Relation not found!'}, HTTPStatus.NOT_FOUND
        return {'msg': 'Role relation successfully removed!'}, HTTPStatus.OK
