from flask import Flask
from LoginAuth import user_auth
from AccountController import account_controller
from flask_cors import CORS
from DeviceController import device_controller
from ConfigurationController import configuration_controller
from DeploymentController import deployment_controller
from VersionsController import version_controller
from UnitTestsController import unit_test_controller
from StatisticsController import statistics_controller


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


from VyNetworkMapper import VyNetworkMapper
from DatabaseConnection import DatabaseConnection
mapper = VyNetworkMapper(DatabaseConnection())
mapper.generate_network_map()

networks = mapper.get_networks().keys()


from VyAPIConnection import VyAPIConnection
from VyRouterAuthData import ApiAuthData
r1_conn = VyAPIConnection(ApiAuthData('192.168.18.90', 'MY-KEY'))
number_of_ports_r1 = len(r1_conn.get_eth_ints())

from ProxmoxApiService import ProxmoxApiService
ProxmoxApiService().set_host('192.168.18.102').set_credentials('root', 'Admin12!').create_connection().create_router_vm(number_of_ports_r1)



