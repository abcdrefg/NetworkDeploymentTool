from pymongo import MongoClient
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId


class DatabaseConnection:
    client = MongoClient("mongodb://localhost:27017/")
    database_name = client["NetworkDeployment"]

    user_collection = "Users"
    devices_collection = "NetworkDevices"

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

    def get_device_by_name(self, name):
        return None

    def insert_device(self, device):
        collection = self.database_name[self.devices_collection]
        collection.insert_one(device)

    def get_devices(self, devices):
        collection = self.database_name[self.devices_collection]
        devices_configs_cursor = collection.find({"name": { "$in": devices}})
        devices_confs = []
        for device in devices_configs_cursor:
            devices_confs.append(device)
        return devices_confs
