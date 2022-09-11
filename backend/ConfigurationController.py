import json

from flask import Blueprint, request, jsonify
from DatabaseConnection import DatabaseConnection
from DeviceLoader import ConnectionWrapper, check_connection, get_running_config, get_devices_running_confs

configuration_controller = Blueprint('configuration_controller', __name__)
bad_request = {
                      'message': "Bad request!",
                      'status': 400,
                      'Error': 'Wrong data.',
                  }, 400

class ConfigurationController:

    @configuration_controller.route('/getCommands', methods=['GET'])
    def get_commands():
        database_cursor = DatabaseConnection()
        devices_with_commands = database_cursor.get_device_commands()
        list_of_devices_with_commands = []
        for device in devices_with_commands:
            list_of_devices_with_commands.append(CommandWrapper(device["name"], device["commands"]).__dict__)
        return list_of_devices_with_commands

    @configuration_controller.route('/upsertCommands', methods=['PUT'])
    def upsert_commands():
        print(request.get_json())
        database_cursor = DatabaseConnection()
        if not request.is_json:
            return bad_request
        json_data = request.get_json()
        database_cursor.upsert_commands(json_data)
        return json.dumps({'success': True}), 200, {'ContentType':'application/json'}

class CommandWrapper:

    def __init__(self, name, commands):
        self.name = name
        self.commands = commands