from VersionControlManager import VersionControlManager
from flask import Blueprint, request, jsonify
from DatabaseConnection import DatabaseConnection
from DeviceConfigManager import DeviceConfigManager
import json

version_controller = Blueprint('version_controller', __name__)
bad_request = {
                  'message': "Bad request!",
                  'status': 400,
                  'Error': 'Wrong credentials.',
              }, 400

class VersionController:

    @version_controller.route('/getHistoricalVersionDiff', methods=['POST'])
    def get_historical_version_diff():
        if not request.is_json:
            return  bad_request
        json_data = request.get_json()
        if json_data["Id"] == None:
            return bad_request
        vcm = VersionControlManager()
        diffrences = vcm.generate_diff_from_spec_conf(json_data["Id"])
        return diffrences

    @version_controller.route('/getVersions', methods=['GET'])
    def get_versions():
        database_conn = DatabaseConnection()
        versions = database_conn.get_versions()
        versions_list = []
        for version in versions:
            version_dict = {}
            version_dict["Id"] = str(version["_id"])
            version_dict["Timestamp"] = version["timestamp"]
            versions_list.append(version_dict)
        return versions_list

    @version_controller.route('/rollbackToId', methods=['POST'])
    def rollback_to_id():
        if not request.is_json:
            return  bad_request
        json_data = request.get_json()
        if json_data["Id"] == None:
            return bad_request
        database_conn = DatabaseConnection()
        configs = database_conn.get_config_version_by_id(json_data["Id"])
        for device_name in configs:
            configs[device_name] = configs[device_name].split("\n")
        device_config_manager = DeviceConfigManager()
        device_config_manager.rollback_configs(configs)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}