from flask import Flask
from flask_restx import Api

from api.v1.account import account_api
from api.v1.role import role_api
from api.v1.roles_manager import role_management_api
from db.config import (
    db,
    migrate,
)
from jwt_config import jwt
from oauth import oauth
from settings import settings

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = settings.db.dsn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = settings.jwt.secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = settings.jwt.access_token_expire_time
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = settings.jwt.refresh_token_expire_time
app.config['JWT_TOKEN_LOCATION'] = settings.jwt.token_location

oauth.init_app(app)
jwt.init_app(app)
db.init_app(app)
migrate.init_app(app, db)

app.app_context().push()
api = Api(app, version='0.0', title='Auth service')
api.add_namespace(account_api)
api.add_namespace(role_api)
api.add_namespace(role_management_api)
app.secret_key = 'secret key'


def main():
    app.run(host='0.0.0.0', port='5001', debug=True)


if __name__ == '__main__':
    main()
