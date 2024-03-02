import pydantic

class ChatMessage(pydantic.BaseModel):
  role: str
  content: str
  id: str = "ExampleID"
  is_insert: bool = False
   
  def encode(self):  
    return {"role": self.role, "content": self.content, "is_insert": self.is_insert, "id": self.id} 

  @staticmethod
  def decode(message_dict):
	  return ChatMessage(role=message_dict["role"], content=message_dict["content"], is_insert=message_dict["is_insert"], id=message_dict["id"])
	
	