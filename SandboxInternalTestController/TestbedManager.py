import bson.json_util

from device_bundles import BundleRegistry
import device_bundles  # noqa: F401 — register device bundles


class TestbedManager:
    def get_devices(self):
        f = open("net_devices.json", "r")
        network_dev_data = bson.json_util.loads(f.read())
        devices = {}
        for device_record in network_dev_data:
            devices[device_record['name']] = BundleRegistry.api_for_device(device_record)
        return devices
