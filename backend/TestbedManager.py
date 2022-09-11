from genie.testbed import load
from DatabaseConnection import DatabaseConnection
import os
import json
import htmldiff
class TestbedManager:

    def create_testbed_dict(self):
        database_conn = DatabaseConnection()
        config_wrappers_map = database_conn.get_device_connection_configs_map()
        device_dict = {}
        for device_name in config_wrappers_map.keys():
            config_wrapper = config_wrappers_map[device_name]
            device_dict[device_name] = \
                {
                    "type": config_wrapper.device_type,
                    "os": "iosxe"
                }
            device_dict[device_name]["connections"] = \
                {
                    "cli": {
                        "ip": config_wrapper.host,
                        "protocol": "telnet"
                    }
                }
            device_dict[device_name]["credentials"] = \
                {
                    "default": {
                        "username": config_wrapper.username,
                        "password": config_wrapper.password
                    }
                }
        testbed_dict = {}
        testbed_dict["devices"] = device_dict
        #testbed = load(testbed_dict)
        #device = testbed.devices["FirstDevice"]
        #device.connect()

