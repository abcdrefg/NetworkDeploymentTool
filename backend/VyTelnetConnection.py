from netmiko import ConnectHandler
from VyRouterAuthData import CommandLineAuthData

class VyTelnetConnection:

    def __init__(self, credentials: CommandLineAuthData):
        self.credentials = credentials
        self.connection = ConnectHandler(**{
          "device_type": credentials.device_type,
          "host": credentials.host,
          "username": credentials.username,
          "password": credentials.password,
          "port": credentials.port,
        })

    def load_config_commands(self, config_commands):
        output = self.connection.send_command(config_commands)
