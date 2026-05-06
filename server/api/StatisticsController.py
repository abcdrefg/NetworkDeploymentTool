from flask import Blueprint, request, jsonify

from core.DatabaseConnection import DatabaseConnection

statistics_controller = Blueprint('statistics_controller', __name__)


@statistics_controller.route('/getNumberOfDevices', methods=['GET'])
def get_number_of_devices():
    database_conn = DatabaseConnection()
    number_of_devices = len(database_conn.get_devices())
    return str(number_of_devices)


@statistics_controller.route('/getNumberOfUnitTests', methods=['GET'])
def get_number_of_tests():
    database_conn = DatabaseConnection()
    number_of_tests = len(list(database_conn.get_unit_tests()))
    return str(number_of_tests)


@statistics_controller.route('/getLastDeploy', methods=['GET'])
def get_last_deploy():
    database_conn = DatabaseConnection()
    last_version = list(database_conn.get_versions())[-1]
    return jsonify(str(last_version["timestamp"]))
