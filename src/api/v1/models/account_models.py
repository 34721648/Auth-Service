from flask_restx import (
    Model,
    fields,
)

login_model = Model(
    'LoginModel',
    {
        'access_token': fields.String,
        'refresh_token': fields.String,
        'message': fields.String,
    },
)

login_session_model = Model(
    'Session',
    {
        'user_id': fields.String,
        'user_agent': fields.String,
        'created_at': fields.String,
    },
)

login_history_model = Model(
    'LoginHistoryModel',
    {
        'data': fields.List(fields.Nested(login_session_model)),
        'has_next': fields.Boolean,
        'has_prev': fields.Boolean,
        'total_pages': fields.Integer,
        'page_size': fields.Integer,
        'current_page': fields.Integer,
    },
)
