from abc import ABC, abstractmethod

from device_bundles.base.router_auth import CommandLineAuthData


class SSHConnection(ABC):
    def __init__(self, credentials: CommandLineAuthData):
        self.credentials = credentials

    @abstractmethod
    def get_config_as_commands(self):
        pass

    @abstractmethod
    def send_command_set(self, commands):
        pass

    @abstractmethod
    def check_connection(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def save(self):
        pass
