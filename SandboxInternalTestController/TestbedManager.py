import bson.json_util

from server.vyos.VyAPIConnection import VyAPIConnection
from server.vyos.VyRouterAuthData import ApiAuthData


class TestbedManager:
    def get_devices(self):
        f = open("net_devices.json", "r")
        network_dev_data = bson.json_util.loads(f.read())
        devices = {}
        for credentials in network_dev_data:
            devices[credentials['name']] = VyAPIConnection(ApiAuthData(credentials['host'], credentials['secret']))
        return devices
