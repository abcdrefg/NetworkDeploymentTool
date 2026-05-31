"""
Device bundles: base defines contracts + registry; each vendor package implements
router_auth, ssh_connection, telnet_connection, and api_connection.
"""
from device_bundles.base.bundle_config import BundleRegistry, ConnectionKind, DeviceBundleConfig, Operation
from device_bundles.base.router_auth import ApiAuthData, CommandLineAuthData

import device_bundles.vyos  # noqa: F401 — register built-in bundles

__all__ = [
    "ApiAuthData",
    "BundleRegistry",
    "CommandLineAuthData",
    "ConnectionKind",
    "DeviceBundleConfig",
    "Operation",
]
