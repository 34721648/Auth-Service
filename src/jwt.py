from flask_jwt_extended import JWTManager

from db.config import token_storage

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload['jti']
    token_in_redis = token_storage.get_value(jti)
    return token_in_redis is not None
