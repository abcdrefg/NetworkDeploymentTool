from telnetlib import Telnet
from time import sleep

from device_bundles.base.telnet_connection import TelnetConnection
from device_bundles.vyos.router_auth import VyosCommandLineAuthData


class VyosTelnetConnection(TelnetConnection):
    LOGIN_PROMPT = "vyos login: "
    PASSWORD_PROMPT = "Password: "
    CONFIG_MODE_COMMAND = b"conf \n"
    COMMIT_COMMAND = b"commit \n"
    TIMEOUT_BETWEEN_COMMANDS = 0.05

    def __init__(self, credentials: VyosCommandLineAuthData):
        super().__init__(credentials)
        self.connection = Telnet(credentials.host, credentials.port)
        self.connection.write(b"\n")
        self.connection.read_until(self.LOGIN_PROMPT.encode("ascii"))
        self.connection.write(credentials.username.encode("ascii") + b"\n")
        self.connection.read_until(self.PASSWORD_PROMPT.encode("ascii"))
        self.connection.write(credentials.password.encode("ascii") + b"\n")
        sleep(1)

    def load_config_commands(self, config_commands):
        self._enter_config_mode()
        for command in config_commands:
            self._send_single_command(command)
        self.connection.write(b"\n")
        self._send_commit()

    def _enter_config_mode(self):
        self.connection.write(self.CONFIG_MODE_COMMAND)
        sleep(self.TIMEOUT_BETWEEN_COMMANDS)

    def _send_single_command(self, command):
        self.connection.write(command.encode("ascii"))
        sleep(self.TIMEOUT_BETWEEN_COMMANDS)

    def _send_commit(self):
        self.connection.write(self.COMMIT_COMMAND)
        sleep(self.TIMEOUT_BETWEEN_COMMANDS)
