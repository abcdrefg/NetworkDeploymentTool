from netmiko import ConnectHandler
from VyRouterAuthData import CommandLineAuthData

class VySSHConnection:

    def __init__(self, credentials: CommandLineAuthData):
        self.credentials = credentials
        self.connection = ConnectHandler(**{
          "device_type": credentials.device_type,
          "host": credentials.host,
          "username": credentials.username,
          "password": credentials.password,
          "port": credentials.port,
        })

    def get_config_as_commands(self):
        output = self.connection.send_command('show config commands')
        return output