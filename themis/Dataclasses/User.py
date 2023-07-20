import pydantic
from typing import Optional

class User(pydantic.BaseModel):
  user_id: str
  username: str
  api_key: str
  email: Optional[str]
  password_hash: Optional[str]
      
  def encode(self):
    return {"user_id": self.user_id, "username": self.username, "api_key": self.api_key, "email": self.email, "password_hash": self.password_hash}
  @staticmethod
  def decode(user_dict):
    return User(user_id=user_dict["user_id"], username=user_dict["username"], api_key=user_dict["api_key"], email=user_dict["email"], password_hash=user_dict["password_hash"])
   