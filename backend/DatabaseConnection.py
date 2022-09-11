from pymongo import MongoClient
import pymongo
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
        newUser = {"$set": {"password": generate_password_hash(newPassword)}}
        updateResult = collection.update_one(user, newUser)  # toRead
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



