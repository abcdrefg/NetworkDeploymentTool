from genie.testbed import load
from DatabaseConnection import DatabaseConnection

class TestbedManager:

    def create_testbed(self):
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
                    },
                    "enable": {
                        "password": config_wrapper.secret
                    }
                }
        testbed_dict = {}
        testbed_dict["devices"] = device_dict
        testbed = load(testbed_dict)
        return testbed

