from pymongo import MongoClient
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash

class DatabaseConnection:

    client = MongoClient("mongodb://localhost:27017/")
    database_name = client["NetworkDeployment"]

    user_collection = 'Users'


    def get_users(self, login, password):
        collection = self.database_name[self.user_collection]
        user = collection.find_one({ "username": login })
        if user == None:
            return False
        if self.check_password(user["password"], password):
            return user["_id"]
        return False

    def check_password(self, passwordHash, password):
        return check_password_hash(passwordHash, password)

    def change_password(self, login, password):
        collection = self.database_name[self.user_collection]
        user = collection.find_one({"username": login})
        print(generate_password_hash(password))
        newUser = {"$set": { "password": generate_password_hash(password)}}
        collection.update_one(user, newUser)

