import os
from json import dumps

from SandboxInternalTestController.TestbedManager import TestbedManager
from SandboxInternalTestController import SandboxInternalTestController


if __name__ == '__main__':
    try:
        os.remove('test_results.json')
    except FileNotFoundError:
        pass
    TestbedManager().get_devices()
    unit_test_manager = SandboxInternalTestController()
    test_results = unit_test_manager.execute()
    with open("test_results.json", "w") as outfile:
        outfile.write(dumps(test_results))
