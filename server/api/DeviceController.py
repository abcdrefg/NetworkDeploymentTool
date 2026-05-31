import json

from flask import Blueprint, request, jsonify

from server.core.DatabaseConnection import DatabaseConnection
from device_bundles import BundleRegistry
import device_bundles  # noqa: F401 — register device bundles

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
        connection = BundleRegistry.ssh_for_device(json_data)
        if not connection.check_connection():
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
        running_confs = []
        for device in database_conn.get_devices():
            running_confs.append(
                {
                    "name": device["name"],
                    "config": BundleRegistry.ssh_for_device(device).get_config_as_commands(),
                    "secret": device["secret"],
                    "password": device["password"],
                    "username": device["username"],
                    "host": device["host"],
                    "deviceType": device["deviceType"]
                }
            )
        return jsonify(running_confs)

    @device_controller.route('/getDatabaseConfigs', methods=['GET'])
    def get_conn_configs_from_database():
        database_conn = DatabaseConnection()
        db_devices = []
        for device in database_conn.get_devices():
            db_devices.append({"name": device["name"], "host": device["host"]})
        return jsonify(db_devices)
