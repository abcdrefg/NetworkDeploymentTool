# Sandbox Internal Test Controller Package

This package contains the `SandboxInternalTestController` component, extracted from `server` so it can be maintained as a separate top-level module.

## Contents

- `SandboxInternalTestController.py` - Executes and manages active unit test scripts.
- `TestbedManager.py` - Loads testbed devices from `net_devices.json`.
- `UnitTestTrigger.py` - Runs test execution flow and writes `test_results.json`.
- `__init__.py` - Exposes `SandboxInternalTestController` for package imports.

## Usage

Import with:

```python
from SandboxInternalTestController import SandboxInternalTestController
```
