from enum import Enum
from typing import Callable, Dict, List, Tuple, Type

from device_bundles.base.api_connection import APIConnection
from device_bundles.base.router_auth import ApiAuthData, CommandLineAuthData
from device_bundles.base.ssh_connection import SSHConnection
from device_bundles.base.telnet_connection import TelnetConnection


class ConnectionKind(Enum):
    SSH = "ssh"
    TELNET = "telnet"
    API = "api"


class Operation(Enum):
    DEPLOY_CONFIG = "deploy_config"
    GET_RUNNING_CONFIG = "get_running_config"
    CHECK_CONNECTION = "check_connection"
    SANDBOX_CONSOLE_CONFIG = "sandbox_console_config"
    NETWORK_MAPPING = "network_mapping"
    UNIT_TESTS = "unit_tests"


class DeviceBundleConfig:
    """
    Registers one vendor bundle. Connection and auth implementations live in the
    vendor package (e.g. device_bundles/vyos/); this class only wires them together.
    """

    def __init__(
        self,
        device_type: str,
        gns3_template_name: str,
        operation_connections: Dict[Operation, ConnectionKind],
        parse_interface_ips: Callable[[str], List[Tuple[str, str]]],
        ssh_connection_class: Type[SSHConnection],
        telnet_connection_class: Type[TelnetConnection],
        api_connection_class: Type[APIConnection],
        command_line_auth_factory: Callable[..., CommandLineAuthData],
        api_auth_factory: Callable[..., ApiAuthData],
        *,
        sandbox_console_username: str = "",
        sandbox_console_password: str = "",
    ):
        self.device_type = device_type
        self.gns3_template_name = gns3_template_name
        self.operation_connections = operation_connections
        self.parse_interface_ips = parse_interface_ips
        self.ssh_connection_class = ssh_connection_class
        self.telnet_connection_class = telnet_connection_class
        self.api_connection_class = api_connection_class
        self.command_line_auth_factory = command_line_auth_factory
        self.api_auth_factory = api_auth_factory
        self.sandbox_console_username = sandbox_console_username
        self.sandbox_console_password = sandbox_console_password

    def connection_for(self, operation: Operation) -> ConnectionKind:
        return self.operation_connections[operation]

    def command_line_auth(self, host, username, password, port=22) -> CommandLineAuthData:
        return self.command_line_auth_factory(host, username, password, port=port)

    def api_auth(self, host, api_key) -> ApiAuthData:
        return self.api_auth_factory(host, api_key)

    def create_ssh_connection(self, credentials: CommandLineAuthData) -> SSHConnection:
        return self.ssh_connection_class(credentials)

    def create_telnet_connection(self, credentials: CommandLineAuthData) -> TelnetConnection:
        return self.telnet_connection_class(credentials)

    def create_api_connection(self, credentials: ApiAuthData) -> APIConnection:
        return self.api_connection_class(credentials)


class BundleRegistry:
    _bundles: Dict[str, DeviceBundleConfig] = {}

    @classmethod
    def register(cls, config: DeviceBundleConfig) -> None:
        cls._bundles[config.device_type.lower()] = config

    @classmethod
    def get(cls, device_type: str) -> DeviceBundleConfig:
        key = (device_type or "").lower()
        if key not in cls._bundles:
            raise KeyError(
                f"No device bundle registered for '{device_type}'. "
                f"Registered: {list(cls._bundles.keys())}"
            )
        return cls._bundles[key]

    @classmethod
    def get_for_device(cls, device: dict) -> DeviceBundleConfig:
        return cls.get(device.get("deviceType", ""))

    @classmethod
    def registered_types(cls) -> List[str]:
        return list(cls._bundles.keys())

    @classmethod
    def ssh_for_device(cls, device: dict) -> SSHConnection:
        bundle = cls.get_for_device(device)
        credentials = bundle.command_line_auth(
            device["host"], device["username"], device["password"]
        )
        return bundle.create_ssh_connection(credentials)

    @classmethod
    def telnet_for_console(cls, device: dict, host: str, port: str) -> TelnetConnection:
        bundle = cls.get_for_device(device)
        credentials = bundle.command_line_auth(
            host,
            device.get("username") or bundle.sandbox_console_username,
            device.get("password") or bundle.sandbox_console_password,
            port=int(port),
        )
        return bundle.create_telnet_connection(credentials)

    @classmethod
    def api_for_device(cls, device: dict) -> APIConnection:
        bundle = cls.get_for_device(device)
        return bundle.create_api_connection(bundle.api_auth(device["host"], device["secret"]))
