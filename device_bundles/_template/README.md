# Device bundle template

Copy this folder to `device_bundles/<your_device>/` and implement every module below.
Shared contracts live in `device_bundles/base/`; vendor-specific behavior stays in your package.

## Required files per vendor

| File | Purpose |
|------|---------|
| `router_auth.py` | `CommandLineAuthData` / `ApiAuthData` implementations for your platform |
| `ssh_connection.py` | Subclass `device_bundles.base.ssh_connection.SSHConnection` |
| `telnet_connection.py` | Subclass `device_bundles.base.telnet_connection.TelnetConnection` |
| `api_connection.py` | Subclass `device_bundles.base.api_connection.APIConnection` |
| `bundle_config.py` | `DeviceBundleConfig` instance + `BundleRegistry.register()` |
| `__init__.py` | Import `bundle_config` so registration runs |

Optional: `network_mapper.py` only if generic `base/network_mapper.py` is not enough.

## `bundle_config.py`

Wire your classes and auth factories:

```python
MY_BUNDLE = DeviceBundleConfig(
    device_type="example",
    gns3_template_name="ExampleRouter",
    operation_connections={...},
    parse_interface_ips=parse_example_interface_ips,
    ssh_connection_class=ExampleSSHConnection,
    telnet_connection_class=ExampleTelnetConnection,
    api_connection_class=ExampleAPIConnection,
    command_line_auth_factory=example_command_line_auth,
    api_auth_factory=example_api_auth,
)
BundleRegistry.register(MY_BUNDLE)
```

## Registration

Add `import device_bundles.<your_device>` in `device_bundles/__init__.py`.
MongoDB `deviceType` must match `device_type` (case-insensitive).
