from DatabaseConnection import DatabaseConnection

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