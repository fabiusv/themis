from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from themis import Dataclasses
class UserDatabaseManager():
   def __init__(self):
      uri = "mongodb+srv://fabiusv:BcY2tswvrIKjEbwO@themiscluster.destxlo.mongodb.net/?retryWrites=true&w=majority"
      self.client = MongoClient(uri, server_api=ServerApi('1'))
      self.db = self.client["themis"]
      self.collection = self.db["users"]

   def insert(self, user):
      self.collection.insert_one(user.encode())

   def edit(self, user):
      self.collection.update_one({"user_id": user.id}, {"$set": user.encode()})

   def find_by_id(self, user_id):
      print("finding")
      users_json = self.collection.find({"user_id":user_id})
      result =  [Dataclasses.User.decode(i) for i in users_json]
      if len(result) == 0:
         return None
      return result[0]

   def find_by_username(self, username):
      users_json = self.collection.find({"username":username})
      result =  [Dataclasses.User.decode(i) for i in users_json]
      if len(result) == 0:
         return None
      return result[0]
   
   def find_by_email(self, email):
      users_json = self.collection.find({"email":email})
      result =  [Dataclasses.User.decode(i) for i in users_json]
      if len(result) == 0:
         return None
      return result[0]
      
   def delete(self, user_id):
      self.collection.delete_one({"user_id":user_id})
