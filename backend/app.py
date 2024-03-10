from flask import Flask
from flask_cors import CORS

from AccountController import account_controller
from ConfigurationController import configuration_controller
from DeploymentController import deployment_controller
from DeviceController import device_controller
from LoginAuth import user_auth
from StatisticsController import statistics_controller
from UnitTestsController import unit_test_controller
from VersionsController import version_controller

running_app = Flask(__name__)
running_app.register_blueprint(user_auth, url_prefix='/loginService')
running_app.register_blueprint(account_controller, url_prefix='/accountService')
running_app.register_blueprint(device_controller, url_prefix= '/deviceController')
running_app.register_blueprint(configuration_controller, url_prefix='/configurationController')
running_app.register_blueprint(deployment_controller, url_prefix='/deploymentController')
running_app.register_blueprint(version_controller, url_prefix='/versionController')
running_app.register_blueprint(unit_test_controller, url_prefix='/unitTestController')
running_app.register_blueprint(statistics_controller, url_prefix='/statisticsService')
CORS(running_app)


from DatabaseConnection import DatabaseConnection
from SandboxController import SandboxController

sandbox_controller = SandboxController()
sandbox_controller.create_sandbox()
configs_by_router_name = {}

from VySSHConnection import VySSHConnection
from VyRouterAuthData import CommandLineAuthData

for credentials in DatabaseConnection().get_devices():
    print(credentials['name'])
    configs_by_router_name[credentials['name']] = VySSHConnection(CommandLineAuthData(credentials['host'], credentials['username'], credentials['password'])).get_config_as_commands()

sandbox_controller.write_configs_to_routers(configs_by_router_name)

sandbox_controller.prepare_test_server()


if __name__ == '__main__':
    running_app.run(host='localhost')





