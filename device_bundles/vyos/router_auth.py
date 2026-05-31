from device_bundles.base.router_auth import ApiAuthData, CommandLineAuthData


class VyosCommandLineAuthData(CommandLineAuthData):
    NETMIKO_DEVICE_TYPE = "vyos"

    def __init__(self, host, username, password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.device_type = self.NETMIKO_DEVICE_TYPE


class VyosApiAuthData(ApiAuthData):
    def __init__(self, host, api_key):
        self.host = host
        self.api_key = api_key
