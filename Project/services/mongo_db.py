from pymongo import MongoClient
import base64
import os
import urllib
from bson.objectid import ObjectId

class MongoService:
    def __init__(self,database=None, collection=None):
        self.database = database
        self.collection = collection


    def establish_connection(self):
        try:
            mongo_uri ="" 
            mongo_uri += str('mongodb+srv://'+ os.getenv("MONGO_USER") +
                    ':'+ urllib.parse.quote(os.getenv("MONGO_PASSWORD")) + os.getenv("MONGO_HOST"))
            print(22222222222,mongo_uri)
            client = MongoClient(mongo_uri,tls=True, tlsAllowInvalidCertificates=True)
            return client
        
        except Exception as ex:
            print("Exception occured:", ex)
            return({"message" : f"Something went wrong. Error In Establish Connection with MongoDb {ex}"}, 500)

    def list_database(self):
        try:
            # List DataBase
            client = self.establish_connection()
            if type(client)==tuple:
                return client
            else:
                database_list = [i["name"] for i in client.list_databases()]
                return ({"result":database_list},200)
            
        except Exception as ex:
            print("Exception occured:", ex)
            return({"message" : f"Error In Listing MongoDb database  {ex}"}, 500)

    def list_collections(self):
        try:
            # List Collection of database
            client = self.establish_connection()
            if type(client)==tuple:
                return client
            else:
                mydatabase = client[self.database]
                if mydatabase.list_collection_names():
                    return ({"result":mydatabase.list_collection_names()},200)
                else:
                    return ({"message":"Please Check the database Name"},212)

        except Exception as ex:
            print("Exception occured:", ex)
            return({"message" : f"Error In Listing MongoDb Collections  {ex}"}, 500)

    def get_data(self, single, template_id=None):
        try:
            client = self.establish_connection()
            if type(client)==tuple:
                return client
            else:
                mydatabase = client[self.database]
                collection_name = mydatabase[self.collection]
                if not single:
                    item_details = collection_name.find({}, {'_id': False})
                    items_ = list(item_details)
                    return items_
                else:
                    document = collection_name.find_one({"_id": ObjectId(template_id)})
                    document['_id'] = str(document['_id'])
                if document:
                    return document
                else:
                    return None
        except Exception as ex:
            print("Exception occured:", ex)
            return({"message" : f"Error In Get Data from MongoDb {ex}"}, 500)
        
    def insert_data(self, input_data):
        client = self.establish_connection()
        mydatabase = client[self.database]
        collection_name = mydatabase[self.collection]
        result = collection_name.insert_one(input_data)
        if result.inserted_id:
            print("Data inserted successfully. Inserted ID:", result.inserted_id)
            return result
        else:
            print("Data insertion failed.")
        pass

    def update_data(self, input_id, update_data):
        client = self.establish_connection()
        mydatabase = client[self.database]
        collection_name = mydatabase[self.collection]
        filter_query = {"_id": ObjectId(input_id)}
        update_query = {"$set": update_data}
        result = collection_name.update_one(filter_query, update_query)
        return result

    def delete_template_by_id(self,document_id):
        try:
            client = self.establish_connection()
            mydatabase = client[self.database]
            collection_name = mydatabase[self.collection]
            result = collection_name.delete_one({"_id": ObjectId(document_id)})
        except Exception as e:
            print(f"Error: {e}")