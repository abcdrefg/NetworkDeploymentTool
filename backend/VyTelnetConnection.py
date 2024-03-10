from netmiko import ConnectHandler
from telnetlib import Telnet
from VyRouterAuthData import CommandLineAuthData
from time import sleep
class VyTelnetConnection:

    VYOS_LOGIN_INDICATOR = "vyos login: "
    VYOS_PASSWORD_INDICATOR = "Password: "
    TIMEOUT_BETWEEN_COMMANDS = 0.05
    def __init__(self, credentials: CommandLineAuthData):
        self.credentials = credentials
        self.connection = Telnet(credentials.host, credentials.port)
        self.connection.write(b"\n")
        self.connection.read_until(self.VYOS_LOGIN_INDICATOR.encode('ascii'))
        self.connection.write(credentials.username.encode('ascii') + b"\n")
        self.connection.read_until(self.VYOS_PASSWORD_INDICATOR.encode('ascii'))
        self.connection.write(credentials.password.encode('ascii') + b"\n")
        sleep(1)
        # self.connection = ConnectHandler(**{
        #   "device_type": credentials.device_type,
        #   "host": credentials.host,
        #   "username": credentials.username,
        #   "password": credentials.password,
        #   "port": credentials.port,
        # })

    def load_config_commands(self, config_commands):
        print(config_commands)
        self.__enter_config_mode()
        for command in config_commands:
            self.__send_single_command(command)
        self.connection.write(b"\n")
        self.__send_commit()

    def __enter_config_mode(self):
        self.connection.write(b"conf \n")
        sleep(self.TIMEOUT_BETWEEN_COMMANDS)

    def __send_single_command(self, command):
        self.connection.write(command.encode('ascii'))
        sleep(self.TIMEOUT_BETWEEN_COMMANDS)

    def __send_commit(self):
        self.connection.write(b"commit \n")
        sleep(self.TIMEOUT_BETWEEN_COMMANDS)