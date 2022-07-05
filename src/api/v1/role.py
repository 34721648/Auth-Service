from http import HTTPStatus

from flask_jwt_extended import jwt_required
from flask_restx import (
    Namespace,
    Resource,
)

from api.v1.models.role_models import role_model
from api.v1.models.shared_models import message_model
from api.v1.parsers.role_parsers import (
    role_create_parser,
    role_delete_parser,
    role_edit_parser,
)
from api.v1.permissions import role_required
from db.config import db
from services.exceptions import (
    RoleAlreadyExists,
    RoleDoesntExists,
)
from services.role import RoleService

role_api = Namespace('v1/role', description='Account operations')
role_api.models[role_model.name] = role_model
role_api.models[message_model.name] = message_model

role_service = RoleService(db)

role_api.authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header',
    },
}


@role_api.route('/roles')
class RolesView(Resource):
    @jwt_required()
    @role_required('admin')
    @role_api.doc('get list of roles')
    @role_api.marshal_with(role_model, as_list=True, code=HTTPStatus.OK)
    @role_api.doc(security='Bearer')
    def get(self):
        return role_service.get_all_roles()

    @jwt_required()
    @role_required('admin')
    @role_api.expect(role_create_parser)
    @role_api.marshal_with(role_model, as_list=False, code=HTTPStatus.CREATED)
    @role_api.doc(security='Bearer')
    def post(self):
        args = role_create_parser.parse_args()
        try:
            role = role_service.create_role(
                name=args['name'],
                description=args['description'],
            )
        except RoleAlreadyExists:
            return {'msg': 'Role already exists!'}, HTTPStatus.CONFLICT
        role_data = {
            'id': role.id,
            'name': role.name,
            'description': role.description,
        }
        return role_data, HTTPStatus.CREATED

    @jwt_required()
    @role_required('admin')
    @role_api.expect(role_delete_parser)
    @role_api.marshal_with(message_model)
    @role_api.doc(security='Bearer')
    def delete(self):
        args = role_create_parser.parse_args()
        try:
            role_service.delete_role(args['name'])
        except RoleDoesntExists:
            return {'msg': 'Role not found!'}, HTTPStatus.NOT_FOUND
        return {'msg': 'Role deleted!'}, HTTPStatus.OK


@role_api.route('/edit-role')
class EditRole(Resource):
    @jwt_required()
    @role_required('admin')
    @role_api.marshal_with(message_model)
    @role_api.expect(role_edit_parser)
    @role_api.doc(security='Bearer')
    def put(self):
        args = role_edit_parser.parse_args()
        try:
            role_service.edit_role(args['name'], args['new_name'], args['new_descritpion'])
        except RoleAlreadyExists:
            return {'msg': 'Role already exists!'}, HTTPStatus.CONFLICT
        return {'msg': 'Role edited!'}, HTTPStatus.OK
