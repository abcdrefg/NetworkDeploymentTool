import glob
from pyats import aetest
from DatabaseConnection import DatabaseConnection
import time

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
        db_conn = DatabaseConnection()
        active_tests = db_conn.get_active_tests()
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

def add_test(file, filename):
    database_conn = DatabaseConnection()
    try:
        database_conn.insert_unit_test({
            "testname": filename,
            "isActive": "false"
        })
    except:
        return "Test already exist"
    with open("testcases/" + filename, 'w') as test_file:
        test_file.write(file)
        test_file.close()
    return "Success"

def get_unit_tests():
    database_conn = DatabaseConnection()
    unit_tests_list = []
    for unit_test_info in database_conn.get_unit_tests():
        unit_tests_list.append({
            "testname": unit_test_info["testname"],
            "isActive": unit_test_info["isActive"]
        })
    return unit_tests_list

def activate_test(testname):
    database_conn = DatabaseConnection()
    database_conn.change_unit_test_status(testname, 'true')

def disable_test(testname):
    database_conn = DatabaseConnection()
    database_conn.change_unit_test_status(testname, 'false')
