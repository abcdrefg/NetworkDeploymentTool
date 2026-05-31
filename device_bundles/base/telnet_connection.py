from abc import ABC, abstractmethod

from device_bundles.base.router_auth import CommandLineAuthData


class TelnetConnection(ABC):
    def __init__(self, credentials: CommandLineAuthData):
        self.credentials = credentials

    @abstractmethod
    def load_config_commands(self, config_commands):
        pass
