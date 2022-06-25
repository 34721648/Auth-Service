from flask_restx import reqparse

role_create_parser = reqparse.RequestParser()
role_create_parser.add_argument('name', type=str, required=True, location='form')
role_create_parser.add_argument('description', type=str, required=False, location='form')

role_edit_parser = reqparse.RequestParser()
role_edit_parser.add_argument('name', type=str, required=True, location='form')
role_edit_parser.add_argument('new_name', type=str, required=False, location='form')
role_edit_parser.add_argument('new_description', type=str, required=False, location='form')

role_delete_parser = reqparse.RequestParser()
role_delete_parser.add_argument('name', type=str, required=True, location='form')
