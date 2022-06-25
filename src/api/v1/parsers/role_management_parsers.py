from flask_restx import reqparse

manage_role_parser = reqparse.RequestParser()
manage_role_parser.add_argument('user_id', type=str, required=True, location='form')
manage_role_parser.add_argument('role_name', type=str, required=True, location='form')
