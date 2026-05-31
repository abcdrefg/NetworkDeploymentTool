from abc import ABC, abstractmethod

from device_bundles.base.router_auth import ApiAuthData


class APIConnection(ABC):
    def __init__(self, credentials: ApiAuthData):
        self.credentials = credentials

    @abstractmethod
    def get_interface_data(self):
        pass
