from genie.testbed import load
from DatabaseConnection import DatabaseConnection
from VyAPIConnection import VyAPIConnection
from VyRouterAuthData import  ApiAuthData

class TestbedManager:

    devices = {}

    def __init__(self):
        database_conn = DatabaseConnection()
        for credentials in database_conn.get_devices():
            self.devices[credentials['name']] = VyAPIConnection(ApiAuthData(credentials['host'], credentials['secret']))
