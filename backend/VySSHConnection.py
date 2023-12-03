from netmiko import ConnectHandler
from VyRouterAuthData import CommandLineAuthData

class VySSHConnection:

    connection=None

    def __init__(self, connection_describe):
        self.connection_describe: CommandLineAuthData = connection_describe

    def establish_connection(self):
        self.connection = ConnectHandler(device_type=self.connection_describe.device_type,
                              host=self.connection_describe.host,
                              username=self.connection_describe.username,
                              password=self.connection_describe.password,
                              port = self.connection_describe.port)
        return self

    def get_connection(self):
        return self.connection

    def close_connection(self):
        self.connection.disconnect()