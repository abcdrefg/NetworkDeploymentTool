from flask import Flask
from flask_cors import CORS

from api.AccountController import account_controller
from api.ConfigurationController import configuration_controller
from api.DeploymentController import deployment_controller
from api.DeviceController import device_controller
from api.LoginAuth import user_auth
from api.StatisticsController import statistics_controller
from api.UnitTestsController import unit_test_controller
from api.VersionsController import version_controller

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

if __name__ == '__main__':
    running_app.run(host='localhost')





