from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
from dotenv import load_dotenv
import os

class ContextDatabaseManager():
   def __init__(self):
      load_dotenv()

      key = os.getenv("mongodb_key")
      uri = "mongodb+srv://fabiusv:"+ key + "@themiscluster.destxlo.mongodb.net/?retryWrites=true&w=majority"
      self.client = MongoClient(uri, server_api=ServerApi('1'))
      self.db = self.client["themis"]
      self.collection = self.db["context"]

   def insert(self, context):
      self.collection.insert_one(context.encode())
   def edit(self, context):
      self.collection.update_one({"context_id": context.context_id}, {"$set": context.encode()})
   def update_conversation(self, context_id, conversation):
      self.collection.update_one({"context_id": context_id}, {"$set": {"conversation": conversation.encode(), "last_update": datetime.datetime.now()}})
   def find_by_id(self, query):
      result = list(self.collection.find({"context_id":query}))
      
      if len(result) == 0:
         return None
      return result[0]
   
   def delete(self, query):
      self.collection.delete_many(query)