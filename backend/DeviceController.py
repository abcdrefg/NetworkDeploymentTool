import json

from flask import Blueprint, request, jsonify
from DatabaseConnection import DatabaseConnection
from DeviceLoader import ConnectionWrapper, check_connection, get_running_config, get_devices_running_confs

device_controller = Blueprint('device_controller', __name__)
bad_request = {
                      'message': "Bad request!",
                      'status': 400,
                      'Error': 'Wrong data.',
                  }, 400

class DeviceAddController:

    @device_controller.route('/addDevice', methods=['POST'])
    def add_device():
        if not request.is_json:
            return bad_request
        json_data = request.get_json()
        if json_data["deviceType"] == None or json_data["username"] == None or json_data["host"] == None or json_data["password"] == None or json_data["name"] == None:
            print(json_data)
            return bad_request
        connection_wrapper = ConnectionWrapper(json_data)
        if not check_connection(connection_wrapper):
            print("bad connection when adding")
            return bad_request
        try:
            database_conn = DatabaseConnection()
            database_conn.insert_device(json_data)
            return jsonify("success")
        except:
            print("similar device exist in database")
            return bad_request

    @device_controller.route('/getRunningConfigs', methods=['GET'])
    def get_running_configs():
        database_conn = DatabaseConnection()
        running_confs = get_devices_running_confs(database_conn.get_devices())
        return running_confs


