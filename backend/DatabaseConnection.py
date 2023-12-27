from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from DeviceLoader import ConnectionWrapper

class DatabaseConnection:
    client = MongoClient("mongodb://localhost:27017/")
    database_name = client["NetworkDeployment"]

    user_collection = "Users"
    devices_collection = "NetworkDevices"
    commands_collection = "DevicesCommands"
    deployment_status = "DeploymentStatus"
    config_versions = "ConfigVersions"
    unit_tests = "UnitTests"

    def get_users(self, login, password):
        collection = self.database_name[self.user_collection]
        user = collection.find_one({"username": login})
        if user == None:
            return False
        if self.check_password(user["password"], password):
            return user["_id"]
        return False

    def check_password(self, passwordHash, password):
        return check_password_hash(passwordHash, password)

    def change_password(self, id, oldPassword, newPassword):
        collection = self.database_name[self.user_collection]
        user = collection.find_one({"_id": ObjectId(id)})
        if not (self.check_password(user.get('password'), oldPassword)):
            return False
        return True

    def get_device_connection_configs_map(self):
        device_conn_map = {}
        for device_conn_conf in self.get_devices():
            device_conn_map[device_conn_conf["name"]] = ConnectionWrapper(device_conn_conf)
        return device_conn_map

    def insert_device(self, device):
        collection = self.database_name[self.devices_collection]
        collection.insert_one(device)

    def get_devices(self):
        collection = self.database_name[self.devices_collection]
        devices_configs_cursor = collection.find()
        devices_confs = []
        for device in devices_configs_cursor:
            devices_confs.append(device)
        return devices_confs

    def get_tokens(self):
        collection = self.database_name[self.user_collection]
        return [str(id) for id in collection.find().distinct('_id')]

    def get_device_commands(self):
        collection = self.database_name[self.commands_collection]
        return collection.find()

    def upsert_commands(self, deviceCommands):
        collection = self.database_name[self.commands_collection]
        list_to_insert = []
        list_to_update = []
        for device in deviceCommands:
            if collection.find_one({"name": device["name"]}) == None:
                list_to_insert.append(device)
                continue;
            collection.update_one({"name": device["name"]}, {"$set": {"commands": device["commands"]}})
        if list_to_insert:
            collection.insert_many(list_to_insert)

    def get_configs_to_send_by_device_name(self):
        collection = self.database_name[self.commands_collection]
        device_configs = collection.find()
        device_configs_by_name = {}
        for device_config in device_configs:
            device_configs_by_name[device_config["name"]] = device_config["commands"]
        return device_configs_by_name

    def get_deployment_status(self):
        collection = self.database_name[self.deployment_status]
        return collection.find_one()

    def finish_syntax_tests(self):
        collection = self.database_name[self.deployment_status]
        status = collection.find_one()
        collection.update_one(status, {"$set": {"SyntaxTest": "True"}})

    def finish_unit_tests(self):
        collection = self.database_name[self.deployment_status]
        status = collection.find_one()
        collection.update_one(status, {"$set": {"UnitTest": "True"}})

    def finish_deploy(self):
        collection = self.database_name[self.deployment_status]
        status = collection.find_one()
        collection.update_one(status, {"$set": {"Deployed": "True"}})

    def insert_config_version(self, config_dict, is_current_config):
        collection = self.database_name[self.config_versions]
        config = collection.insert_one(config_dict)
        if is_current_config:
            self.update_current_conf(config.inserted_id)

    def update_current_conf(self, id):
        collection = self.database_name[self.deployment_status]
        status = collection.find_one()
        collection.update_one(status, {"$set": {"CurrentConfig": id}})

    def get_current_configs(self):
        collection = self.database_name[self.deployment_status]
        status = collection.find_one()
        curr_conf_id = status["CurrentConfig"]
        collection_configs = self.database_name[self.config_versions]
        configs = collection_configs.find_one({"_id": curr_conf_id})
        return configs["configs"]

    def remove_config_records(self):
        collection = self.database_name[self.commands_collection]
        collection.drop()

    def set_start_status(self):
        collection = self.database_name[self.deployment_status]
        status = collection.find_one()
        collection.update_one(status, {"$set": {"Deployed": "False", "SyntaxTest": "False", "UnitTest": "False"}})

    def get_config_version_by_id(self, version_id):
        collection = self.database_name[self.config_versions]
        configs = collection.find_one({"_id": ObjectId(version_id)})
        return configs["configs"]

    def get_versions(self):
        collection = self.database_name[self.config_versions]
        return collection.find()

    def get_unit_tests(self):
        collection = self.database_name[self.unit_tests]
        return collection.find()

    def insert_unit_test(self, unit_test):
        collection = self.database_name[self.unit_tests]
        collection.insert_one(unit_test)

    def change_unit_test_status(self, testname, status):
        collection = self.database_name[self.unit_tests]
        unit_test = collection.find_one({"testname": testname})
        collection.update_one(unit_test, {"$set": {"isActive": status}})

    def get_active_tests(self):
        collection = self.database_name[self.unit_tests]
        return collection.find({"isActive": "true"})
