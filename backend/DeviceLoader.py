from genie.testbed import load
from netmiko import ConnectHandler

def check_connection(connection_wrapper):
    try:
        conn = ConnectHandler(device_type=connection_wrapper.os,
                              host=connection_wrapper.host,
                              username=connection_wrapper.username,
                              password=connection_wrapper.password,
                              secret=connection_wrapper.secret)
        conn.disconnect()
        return True
    except:
        return False

def get_running_config(connection_wrapper):
    try:
        conn = ConnectHandler(device_type=connection_wrapper.os,
        host=connection_wrapper.host,
        username=connection_wrapper.username,
        password=connection_wrapper.password,
        secret=connection_wrapper.secret)
        conn.enable()
        output = conn.send_command("sh run")
        conn.disconnect()
        return output
    except:
        return "Can't reach the device"


def get_devices_running_confs(device_confs):
    running_configs = []
    for device_conf in device_confs:
        conn_wrapper = ConnectionWrapper(device_conf)
        running_configs.append(ConfigsWrapper(conn_wrapper, get_running_config(conn_wrapper).replace("Building configuration...\n\n", "")).__dict__)
    return running_configs

class ConnectionWrapper:
    def __init__(self, device_dict):
        self.device_type = device_dict["deviceType"]
        self.host = device_dict["host"]
        self.username = device_dict["username"]
        self.password = device_dict["password"]
        self.secret = device_dict["secret"]
        self.name = device_dict["name"]
        self.os = 'cisco_ios_telnet'

class ConfigsWrapper:
    def __init__(self, conn_wrapper, device_config):
        self.name = conn_wrapper.name
        self.host = conn_wrapper.host
        self.config = device_config
        self.deviceType = conn_wrapper.device_type
        self.username = conn_wrapper.username
        self.password = conn_wrapper.password
        self.secret = conn_wrapper.secret