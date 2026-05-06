import json

from flask import Blueprint, request, jsonify

from core.DatabaseConnection import DatabaseConnection
from vyos.VyRouterAuthData import CommandLineAuthData
from vyos.VySSHConnection import VySSHConnection

configuration_controller = Blueprint('configuration_controller', __name__)
bad_request = {
                      'message': "Bad request!",
                      'status': 400,
                      'Error': 'Wrong data.',
                  }, 400


class ConfigurationController:
    @configuration_controller.route('/getCommands', methods=['GET'])
    def get_commands():
        database_conn = DatabaseConnection()
        running_confs = []
        device_commands = database_conn.get_device_commands()
        for device in database_conn.get_devices():
            db_commands = list(filter(lambda x: x["name"] == device["name"], device_commands))
            if len(db_commands) == 0:
                db_commands = VySSHConnection(CommandLineAuthData(device["host"], device["username"],
                                                                  device["password"])).get_config_as_commands()
            else:
                db_commands = db_commands[0]["commands"]
            running_confs.append({
                "name": device["name"],
                "commands": db_commands
            })
        return running_confs

    @configuration_controller.route('/upsertCommands', methods=['PUT'])
    def upsert_commands():
        database_cursor = DatabaseConnection()
        if not request.is_json:
            return bad_request
        json_data = request.get_json()
        database_cursor.upsert_commands(json_data)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    @configuration_controller.route('/isEditEnabled', methods=['GET'])
    def is_edit_enabled():
        database_conn = DatabaseConnection()
        deploy_stat = database_conn.get_deployment_status()
        if deploy_stat["SyntaxTest"] == "True":
            return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
