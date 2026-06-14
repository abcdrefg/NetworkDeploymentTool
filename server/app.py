from flask import Flask
from flask_cors import CORS

from server.api.AccountController import account_controller
from server.api.ConfigurationController import configuration_controller
from server.api.DeploymentController import deployment_controller
from server.api.DeviceController import device_controller
from server.api.LoginAuth import user_auth
from server.api.StatisticsController import statistics_controller
from server.api.UnitTestsController import unit_test_controller
from server.api.VersionsController import version_controller

running_app = Flask(__name__)
running_app.register_blueprint(user_auth, url_prefix='/loginService')
running_app.register_blueprint(account_controller, url_prefix='/accountService')
running_app.register_blueprint(device_controller, url_prefix='/deviceController')
running_app.register_blueprint(configuration_controller, url_prefix='/configurationController')
running_app.register_blueprint(deployment_controller, url_prefix='/deploymentController')
running_app.register_blueprint(version_controller, url_prefix='/versionController')
running_app.register_blueprint(unit_test_controller, url_prefix='/unitTestController')
running_app.register_blueprint(statistics_controller, url_prefix='/statisticsService')
CORS(running_app)

import os

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', 'localhost')
    port = int(os.environ.get('FLASK_PORT', 5000))
    running_app.run(host=host, port=port)
