from flask import Blueprint, request, jsonify
from DatabaseConnection import DatabaseConnection
user_auth = Blueprint('user_auth', __name__)

class User_authenticator:
    def __init__(self):
        self.bad_request = {
                'message': "Bad request!",
                'status': 400,
                'Error': 'Unexpected error.',
            }, 400

    @user_auth.route('/authenticate', methods=['POST'])
    def auth_user():
        if not request.is_json:
            return self.bad_request
        json_data = request.get_json()
        if json_data["login"] == None or json_data["password"] == None:
            return self.bad_request
        database_cursor = DatabaseConnection()
        if database_cursor.get_users(json_data["login"], json_data["password"]):

            return jsonify({'login': json_data["login"], 'token': str(database_cursor.get_users(json_data["login"], json_data["password"]))})
        return {
                'message': "Wrong Credentials",
                'status': 400,
                'Error': 'Unexpected error.',
            }, 400
