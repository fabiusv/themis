import datetime
from typing import Optional
import pydantic # type: ignore
from .Conversation import Conversation
from .MetaData import MetaData

class Context(pydantic.BaseModel):

   user_id: str
   context_id: str
   creation: datetime.datetime
   last_modification: datetime.datetime
   expiry: datetime.datetime | None = None
   conversation: Conversation
   meta_data: MetaData
   

   def encode(self):
      return {"user_id": self.user_id, "context_id": self.context_id, "creation":int(self.creation.timestamp()), "last_modification": int(self.last_modification.timestamp()), "expiry": int(self.expiry.timestamp()) if self.expiry else None, "conversation": self.conversation.encode(), "meta_data": self.meta_data.encode()}
   @staticmethod
   def decode(context_dict):
      return Context(user_id=context_dict["user_id"], context_id=context_dict["context_id"], creation=datetime.datetime.fromtimestamp(context_dict["creation"]), last_modification=datetime.datetime.fromtimestamp(context_dict["last_modification"]), expiry=datetime.datetime.fromtimestamp(context_dict["expiry"]) if context_dict["expiry"] else None, conversation=Conversation.decode(context_dict["conversation"]), meta_data=MetaData.decode(context_dict["meta_data"]))
