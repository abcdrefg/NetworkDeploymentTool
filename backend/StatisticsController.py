from flask import Blueprint, request, jsonify
from DatabaseConnection import DatabaseConnection
from UnitTestManager import UnitTestManager
statistics_controller = Blueprint('statistics_controller', __name__)

@statistics_controller.route('/getNumberOfDevices', methods=['GET'])
def get_number_of_devices():
    database_conn = DatabaseConnection()
    number_of_devices = len(database_conn.get_devices())
    return str(number_of_devices)

@statistics_controller.route('/getNumberOfUnitTests', methods=['GET'])
def get_number_of_tests():
    number_of_test_files = len(UnitTestManager().get_test_files())
    return str(number_of_test_files)

@statistics_controller.route('/getLastDeploy', methods=['GET'])
def get_last_deploy():
    database_conn = DatabaseConnection()
    last_version = list(database_conn.get_versions())[-1]
    return jsonify(str(last_version["timestamp"]))