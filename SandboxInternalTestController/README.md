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

## Docker image

Build from the **repository root** (the image includes `device_bundles/` and `testcases/`):

```bash
docker build -f SandboxInternalTestController/Dockerfile -t sandbox-test-controller .
```

The GNS3 sandbox server should use an image named `sandbox-server` (see `server/sandbox/Gns3Controller.py`). Tag accordingly:

```bash
docker tag sandbox-test-controller sandbox-server
```

The container **does not run tests on start** — it stays alive (`sleep infinity`) so the main server can use the Docker API: copy `net_devices.json`, `active_tests.json`, and testcase files into `/home/TestController`, then `exec` `./test_exec.sh`. Results are read from `test_results.json`.

Example (manual):

```bash
docker run -d --name sandbox-test sandbox-server
docker exec sandbox-test /home/TestController/test_exec.sh
docker exec sandbox-test cat /home/TestController/test_results.json
```
