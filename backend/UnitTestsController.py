from flask import Blueprint, request, jsonify
import json

unit_test_controller = Blueprint('unit_test_controller', __name__)
bad_request = {
                      'message': "Bad request!",
                      'status': 400,
                      'Error': 'Wrong data.',
                  }, 400

class UnitTestsController:

    @unit_test_controller.route('/getTests', methods=['GET'])
    def get_tests():
        return 'x'
        # return get_unit_tests()

    @unit_test_controller.route('disableTest', methods=['POST'])
    def disable_test():
        if not request.is_json:
            return bad_request
        json_data = request.get_json()
        # disable_test(json_data["testname"])
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    @unit_test_controller.route('activateTest', methods=['POST'])
    def enable_test():
        if not request.is_json:
            return bad_request
        json_data = request.get_json()
        # activate_test(json_data["testname"])
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    @unit_test_controller.route('insertTest', methods=['POST'])
    def insert_test():
        if not request.is_json:
            return bad_request
        json_data = request.get_json()
        # add_test(json_data["file"], json_data["filename"])
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
