from http import HTTPStatus

from flask import url_for
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_restx import (
    Namespace,
    Resource,
)

from api.v1.models.account_models import (
    login_history_model,
    login_model,
    login_session_model,
)
from api.v1.models.shared_models import message_model
from api.v1.parsers.account_parsers import (
    edit_login_parser,
    edit_password_parser,
    login_history_parser,
    login_parser,
    logout_parser,
    register_parser,
)
from api.v1.utils import user_session_to_dict
from db.config import (
    db,
    token_storage,
)
from db.models import AuthType
from oauth import oauth
from services.account import AccountService
from services.exceptions import (
    UnvailableLogin,
    UserAlreadyExists,
    UserDoesntExists,
    WrongPassword,
)
from settings import settings

account_api = Namespace('v1/account', description='Account operations')
account_service = AccountService(db)
account_api.authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header',
    },
}

account_api.models[message_model.name] = message_model
account_api.models[login_model.name] = login_model
account_api.models[login_session_model.name] = login_session_model
account_api.models[login_history_model.name] = login_history_model


@account_api.route('/register')
class Register(Resource):
    @account_api.expect(register_parser)
    @account_api.marshal_with(message_model)
    def post(self):
        args = register_parser.parse_args()
        try:
            account_service.registrate_user(
                login=args['login'],
                password=args['password'],
                email=args['email'],
                auth_type=AuthType.default,
            )
        except UserAlreadyExists:
            return {'msg': 'User already exists!'}, HTTPStatus.CONFLICT
        return {'msg': 'Account created!'}, HTTPStatus.OK


@account_api.route('/login')
class Login(Resource):
    @account_api.expect(login_parser)
    @account_api.marshal_with(login_model, skip_none=True)
    def post(self):
        args = login_parser.parse_args()
        try:
            account_service.login(login=args['login'], password=args['password'])
        except UserDoesntExists:
            return {'msg': 'Authorization Error!'}, HTTPStatus.UNAUTHORIZED
        except WrongPassword:
            return {'msg': 'Authorization Error!'}, HTTPStatus.UNAUTHORIZED

        user_id = account_service.get_user_id_by_login(login=args['login'])

        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)

        account_service.register_user_session(user_id, args['User-Agent'])

        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


@account_api.route('/logout')
class Logout(Resource):
    @jwt_required()
    @account_api.expect(logout_parser)
    @account_api.marshal_with(message_model)
    @account_api.doc(security='Bearer')
    def post(self):
        args = logout_parser.parse_args()
        access_token_decoded = decode_token(args['access_token'])
        refresh_token_decoded = decode_token(args['refresh_token'])

        token_storage.set_value(access_token_decoded['jti'], '', time_to_leave=settings.jwt.access_token_expire_time)
        token_storage.set_value(refresh_token_decoded['jti'], '', time_to_leave=settings.jwt.refresh_token_expire_time)

        return {'msg': 'Successfully logged out!'}, HTTPStatus.OK


@account_api.route('/login-history')
class LoginHistory(Resource):
    @jwt_required()
    @account_api.expect(login_history_parser)
    @account_api.marshal_with(login_history_model)
    @account_api.doc(security='Bearer')
    def get(self):
        user_id = get_jwt_identity()
        paginated = account_service.get_user_sessions(user_id)

        user_sessions_dicts = [user_session_to_dict(user_session) for user_session in paginated.items]
        response_data = {
            'data': user_sessions_dicts,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev,
            'total_pages': paginated.pages,
            'page_size': paginated.per_page,
            'current_page': paginated.page,
        }
        return response_data, HTTPStatus.OK


@account_api.route('/edit-login')
class EditLogin(Resource):
    @jwt_required()
    @account_api.expect(edit_login_parser)
    @account_api.marshal_with(message_model)
    @account_api.doc(security='Bearer')
    def put(self):
        args = edit_login_parser.parse_args()
        user_id = get_jwt_identity()
        try:
            account_service.edit_user_login(user_id, args['new_login'])
        except UnvailableLogin:
            return {'msg': 'Login not available!'}, HTTPStatus.CONFLICT
        return {'msg': 'Login successfully changed!'}, HTTPStatus.OK


@account_api.route('/edit-password')
class EditPassword(Resource):
    @jwt_required()
    @account_api.expect(edit_password_parser)
    @account_api.marshal_with(message_model)
    @account_api.doc(security='Bearer')
    def put(self):
        args = edit_password_parser.parse_args()
        user_id = get_jwt_identity()
        account_service.edit_user_password(user_id, args['new_password'])
        return {'msg': 'Password successfully changed!'}, HTTPStatus.OK


@account_api.route('/refresh-token')
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    @account_api.marshal_with(login_model, skip_none=True)
    @account_api.doc(security='Bearer')
    def post(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)

        refresh_token_jti = get_jwt()['jti']
        token_storage.set_value(refresh_token_jti, '', time_to_leave=settings.jwt.refresh_token_expire_time)

        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


@account_api.route('/login-google')
class GoogleLogin(Resource):
    def get(self):
        redirect_uri = url_for('v1/account_google_authorize', _external=True)
        return oauth.google.authorize_redirect(redirect_uri)


@account_api.route('/authorize-google')
class GoogleAuthorize(Resource):
    def get(self):
        return oauth.google.authorize_access_token()
