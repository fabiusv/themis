import pydantic
from typing import Optional
from .PersonFile import PersonFile
from .PersonalStorage import PersonalStorage as Personal
from ..python_extensions import optional_unwrap

class User(pydantic.BaseModel):
  user_id: str
  username: str
  api_key: str
  email: Optional[str]
  password_hash: Optional[str]

  personal_storage: Personal
      
  def encode(self):
    print("Trying to encode")
    return {"user_id": self.user_id, "username": self.username, "api_key": self.api_key, "email": self.email, "password_hash": self.password_hash, "personal_storage": self.personal_storage.encode()}
  @staticmethod
  def decode(user_dict):
    return User(user_id=user_dict["user_id"], username=user_dict["username"], api_key=user_dict["api_key"], email=user_dict["email"], password_hash=user_dict["password_hash"], personal_storage=Personal.decode(user_dict["personal_storage"]))
   