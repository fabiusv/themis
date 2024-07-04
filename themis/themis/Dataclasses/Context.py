import datetime
from typing import Optional
import pydantic # type: ignore
from .Conversation import Conversation
from .MetaData import MetaData
from typing import List

class Context(pydantic.BaseModel):
   user_id: str
   context_id: str
   creation: datetime.datetime
   last_modification: datetime.datetime
   expiry: datetime.datetime | None = None
   conversation: Conversation
   meta_data: MetaData
   extra_functions: List[dict] = []

   def encode(self):
      return {"user_id": self.user_id, "context_id": self.context_id, "creation":int(self.creation.timestamp()), "last_modification": int(self.last_modification.timestamp()), "expiry": int(self.expiry.timestamp()) if self.expiry else None, "conversation": self.conversation.encode(), "meta_data": self.meta_data.encode(), "extra_functions": self.extra_functions if self.extra_functions else []} 
   @staticmethod
   def decode(context_dict):
      return Context(user_id=context_dict["user_id"], context_id=context_dict["context_id"], creation=datetime.datetime.fromtimestamp(context_dict["creation"]), last_modification=datetime.datetime.fromtimestamp(context_dict["last_modification"]), expiry=datetime.datetime.fromtimestamp(context_dict["expiry"]) if context_dict["expiry"] else None, conversation=Conversation.decode(context_dict["conversation"]), meta_data=MetaData.decode(context_dict["meta_data"]), extra_functions=context_dict["extra_functions"] if context_dict["extra_functions"] else [])
   @staticmethod
   def dummy():
      return Context(user_id="dummy", context_id="dummy", creation=datetime.datetime.now(), last_modification=datetime.datetime.now(), conversation=Conversation.dummy(), meta_data=MetaData.dummy())