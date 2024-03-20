import glob
from pyats import aetest
import time
import bson.json_util

class UnitTestManager:

    def execute(self):
        test_results = self.run_testscripts(self.get_active_test_files())
        return test_results

    def get_active_test_files(self):
        active_tests_names = self.get_active_test_names()
        test_files = self.get_test_files()
        test_files = map(lambda file : file.replace('testcases/', ''), test_files)
        return filter(lambda file : file in active_tests_names, test_files)

    def get_active_test_names(self):
        active_tests = self.get_active_tests()
        tests_name_list = []
        for test in active_tests:
            tests_name_list.append(test["testname"])
        return tests_name_list

    def get_test_files(self):
        return glob.glob("testcases/*.py")

    def run_testscripts(self, tests_list):
        results_list = []
        for test in tests_list:
            time.sleep(1)
            try:
                result = aetest.main(testable = 'testcases/' + test)
            except:
                result = 'invalid test'
            results_list.append({
                "testname": test.replace('testcases/', ''),
                "result": str(result)
            })
        return results_list

    def get_active_tests(self):
        f = open("active_tests.json", "r")
        return bson.json_util.loads(f.read())
