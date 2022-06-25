from flask_restx import (
    Model,
    fields,
)

message_model = Model('MessageModel', {'msg': fields.String})
