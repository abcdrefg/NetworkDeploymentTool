from typing import Callable, Dict, List, Tuple, Type

from device_bundles.base.api_connection import APIConnection
from device_bundles.base.bundle_config import (
    BundleRegistry,
    ConnectionKind,
    DeviceBundleConfig,
    Operation,
)
from device_bundles.base.router_auth import ApiAuthData, CommandLineAuthData
from device_bundles.base.ssh_connection import SSHConnection
from device_bundles.base.telnet_connection import TelnetConnection
from device_bundles.vyos.api_connection import VyosAPIConnection
from device_bundles.vyos.router_auth import VyosApiAuthData, VyosCommandLineAuthData
from device_bundles.vyos.ssh_connection import VyosSSHConnection
from device_bundles.vyos.telnet_connection import VyosTelnetConnection


def parse_vyos_interface_ips(output: str) -> List[Tuple[str, str]]:
    """Parse VyOS `show interfaces` text into (interface_name, ip_address) pairs."""
    ip_addresses = []
    for line in output.split("\n"):
        if not line.startswith("eth"):
            continue
        columns = line.split()
        if len(columns) < 2:
            continue
        ip_address = columns[1]
        if ip_address == "-":
            continue
        ip_addresses.append((columns[0], ip_address))
    return ip_addresses


def vyos_command_line_auth(host, username, password, port=22) -> VyosCommandLineAuthData:
    return VyosCommandLineAuthData(host, username, password, port=port)


def vyos_api_auth(host, api_key) -> VyosApiAuthData:
    return VyosApiAuthData(host, api_key)


VYOS_BUNDLE = DeviceBundleConfig(
    device_type="vyos",
    gns3_template_name="vyos",
    operation_connections={
        Operation.DEPLOY_CONFIG: ConnectionKind.SSH,
        Operation.GET_RUNNING_CONFIG: ConnectionKind.SSH,
        Operation.CHECK_CONNECTION: ConnectionKind.SSH,
        Operation.SANDBOX_CONSOLE_CONFIG: ConnectionKind.TELNET,
        Operation.NETWORK_MAPPING: ConnectionKind.API,
        Operation.UNIT_TESTS: ConnectionKind.API,
    },
    parse_interface_ips=parse_vyos_interface_ips,
    ssh_connection_class=VyosSSHConnection,
    telnet_connection_class=VyosTelnetConnection,
    api_connection_class=VyosAPIConnection,
    command_line_auth_factory=vyos_command_line_auth,
    api_auth_factory=vyos_api_auth,
    sandbox_console_username="vyos",
    sandbox_console_password="vyos",
)

BundleRegistry.register(VYOS_BUNDLE)
