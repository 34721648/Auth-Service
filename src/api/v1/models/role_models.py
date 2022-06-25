from flask_restx import (
    Model,
    fields,
)

role_model = Model(
    'RoleModel',
    {
        'id': fields.String,
        'name': fields.String,
        'description': fields.String,
    },
)
