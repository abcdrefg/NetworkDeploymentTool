import json

from flask import Blueprint, request, jsonify

from server.core.DatabaseConnection import DatabaseConnection

unit_test_controller = Blueprint('unit_test_controller', __name__)
bad_request = {
                      'message': "Bad request!",
                      'status': 400,
                      'Error': 'Wrong data.',
                  }, 400


class UnitTestsController:
    @unit_test_controller.route('/getTests', methods=['GET'])
    def get_tests():
        return get_unit_tests()

    @unit_test_controller.route('disableTest', methods=['POST'])
    def disable_test():
        if not request.is_json:
            return bad_request
        json_data = request.get_json()
        disable_test(json_data["testname"])
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    @unit_test_controller.route('activateTest', methods=['POST'])
    def enable_test():
        if not request.is_json:
            return bad_request
        json_data = request.get_json()
        activate_test(json_data["testname"])
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    @unit_test_controller.route('insertTest', methods=['POST'])
    def insert_test():
        if not request.is_json:
            return bad_request
        json_data = request.get_json()
        add_test(json_data["file"], json_data["filename"])
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def add_test(file, filename):
    database_conn = DatabaseConnection()
    try:
        database_conn.insert_unit_test({
            "testname": filename,
            "isActive": "false"
        })
    except:
        return "Test already exist"
    with open("testcases/" + filename, 'w') as test_file:
        test_file.write(file)
        test_file.close()
    return "Success"


def get_unit_tests():
    database_conn = DatabaseConnection()
    unit_tests_list = []
    for unit_test_info in database_conn.get_unit_tests():
        unit_tests_list.append({
            "testname": unit_test_info["testname"],
            "isActive": unit_test_info["isActive"]
        })
    return unit_tests_list


def activate_test(testname):
    database_conn = DatabaseConnection()
    database_conn.change_unit_test_status(testname, 'true')


def disable_test(testname):
    database_conn = DatabaseConnection()
    database_conn.change_unit_test_status(testname, 'false')
