from flask import Blueprint, request, jsonify
from DatabaseConnection import DatabaseConnection

account_controller = Blueprint('account_controller', __name__)


class AccountServices:
    @account_controller.route('/changePassword', methods=['POST'])
    def change_password():
        bad_request = {
                          'message': "Bad request!",
                          'status': 400,
                          'Error': 'Wrong credentials.',
                      }, 400
        if not request.is_json:
            return bad_request
        json_data = request.get_json()
        print(json_data)
        if json_data["newPassword"] == None or json_data["oldPassword"] == None or json_data["token"] == None:
            return bad_request
        database_conn = DatabaseConnection()
        if database_conn.change_password(json_data["token"], json_data["oldPassword"], json_data["newPassword"]):
            return "success"
        return bad_request
