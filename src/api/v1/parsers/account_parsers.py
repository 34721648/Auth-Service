from flask_restx import reqparse

login_parser = reqparse.RequestParser()
login_parser.add_argument('login', type=str, required=True, location='form')
login_parser.add_argument('password', type=str, required=True, location='form')
login_parser.add_argument('User-Agent', location='headers')

register_parser = reqparse.RequestParser()
register_parser.add_argument('login', type=str, required=True, location='form')
register_parser.add_argument('password', type=str, required=True, location='form')
register_parser.add_argument('email', type=str, required=True, location='form')

edit_login_parser = reqparse.RequestParser()
edit_login_parser.add_argument('new_login', type=str, required=True, location='form')

edit_password_parser = reqparse.RequestParser()
edit_password_parser.add_argument('new_password', type=str, required=True, location='form')

logout_parser = reqparse.RequestParser()
logout_parser.add_argument('access_token', type=str, required=True, location='form')
logout_parser.add_argument('refresh_token', type=str, required=True, location='form')

login_history_parser = reqparse.RequestParser()
login_history_parser.add_argument('page_size', type=int, default=10, location='args')
login_history_parser.add_argument('page_number', type=int, default=1, location='args')

google_login_parser = reqparse.RequestParser()
google_login_parser.add_argument('User-Agent', location='headers')
