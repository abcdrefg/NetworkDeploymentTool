from abc import ABC


class CommandLineAuthData(ABC):
    """Vendor bundle implements with host, username, password, port, netmiko device_type, etc."""

    host: str
    username: str
    password: str
    port: int


class ApiAuthData(ABC):
    """Vendor bundle implements with host and API credentials."""

    host: str
