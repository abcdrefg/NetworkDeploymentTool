import json

from flask import Blueprint, request, jsonify
from DeviceConfigManager import DeviceConfigManager
from DatabaseConnection import DatabaseConnection
from VersionControlManager import VersionControlManager
from UnitTestManager import UnitTestManager

deployment_controller = Blueprint('deployment_controller', __name__)

class DeploymentController():

    @deployment_controller.route('/testConfigs', methods=['GET'])
    def test_configs():
        manager = DeviceConfigManager()
        error_array = manager.test_configs()
        return error_array

    @deployment_controller.route('/getStatus', methods=['GET'])
    def get_deployment_status():
        database_conn = DatabaseConnection()
        status = database_conn.get_deployment_status()
        deploy_status = "SyntaxTest";
        if status["SyntaxTest"] == "True":
            deploy_status = "UnitTest"
        if status["UnitTest"] == "True":
            deploy_status = "Deployment"
        return json.dumps({'success': True, 'DeployStatus': deploy_status}), 200, {'ContentType': 'application/json'}

    @deployment_controller.route('/finishSyntaxTest', methods=['HEAD'])
    def finish_syntax_test():
        database_conn = DatabaseConnection()
        database_conn.finish_syntax_tests()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    @deployment_controller.route('/finishUnitTest', methods=['HEAD'])
    def finish_unit_test():
        database_conn = DatabaseConnection()
        database_conn.finish_unit_tests()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    @deployment_controller.route('/deployConfigurations', methods=['GET'])
    def deploy_configurations():
        manager = DeviceConfigManager()
        status = manager.deploy_config();
        if status == 'success':
            database_conn = DatabaseConnection()
            database_conn.finish_deploy()
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        return json.dumps({'success': False, 'errors': status}), 400, {'ContentType': 'application/json'}

    @deployment_controller.route('/getDiffrences', methods=['GET'])
    def get_diff():
        vcm = VersionControlManager()
        return vcm.generate_diff_with_current_config()

    @deployment_controller.route('/createSnapshot', methods=['HEAD'])
    def create_snapshot():
        vcm = VersionControlManager()
        vcm.generate_config(True)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    @deployment_controller.route('/checkDeploy', methods=['GET'])
    def check_deploy():
        database_conn = DatabaseConnection()
        deploy_stat = database_conn.get_deployment_status()
        if deploy_stat["Deployed"] == "True":
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    @deployment_controller.route('/startNewProcess', methods=['HEAD'])
    def start_new_process():
        database_conn = DatabaseConnection()
        database_conn.set_start_status()
        database_conn.remove_config_records()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    @deployment_controller.route('/terminateProcess', methods=['HEAD'])
    def terminate_process():
        database_conn = DatabaseConnection()
        database_conn.set_start_status()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    @deployment_controller.route('/runTests', methods=['GET'])
    def run_test():
        utm = UnitTestManager()
        results = utm.execute()
        return results