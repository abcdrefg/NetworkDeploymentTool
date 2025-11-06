from UnitTestManager import UnitTestManager
from TestbedManager import TestbedManager
import os
from json import dumps

if __name__ == '__main__':
    os.remove('test_results.json')
    TestbedManager().get_devices()
    unit_test_manager = UnitTestManager()
    test_results = unit_test_manager.execute()
    with open("test_results.json", "w") as outfile:
        outfile.write(dumps(test_results))