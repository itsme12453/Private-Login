from pymongo import MongoClient
from bson.objectid import ObjectId

class Database:

    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client.details

    def insert_data(self, collection_name, data):
        self.db[collection_name].insert_one(data)
    
    def new_person(self, collection_name, id, data):
        self.db[collection_name].update_one({"_id": ObjectId(id)}, {"$push": {"people": data}})

    def find_data(self, collection_name, query):
        raw_result = self.db[collection_name].find(query)
        result_array = []
        for result in raw_result:
            result["name"] = str(result["name"])
            result_array.append(result)
        
        return result_array