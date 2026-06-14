# VyOS device bundle — registers with BundleRegistry on import.
from device_bundles.vyos import bundle_config  # noqa: F401
from device_bundles.vyos.bundle_config import VYOS_BUNDLE

__all__ = ["VYOS_BUNDLE", "bundle_config"]
