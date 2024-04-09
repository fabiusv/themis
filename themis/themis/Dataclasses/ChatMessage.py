import pydantic

class ChatMessage(pydantic.BaseModel):
  role: str
  content: str 
  id: str = "ExampleID"
  is_insert: bool = False
  file_ids: int = []
  
  def encode(self):  
    return {"role": self.role, "content": self.content, "is_insert": self.is_insert, "id": self.id, "file_ids": self.file_ids} 

  @staticmethod
  def decode(message_dict):
    return ChatMessage(
      role=message_dict.get("role"), 
      content=message_dict.get("content"), 
      is_insert=message_dict.get("is_insert", False), 
      id=message_dict.get("id", "ExampleID"),
      file_ids=message_dict.get("file_ids", [])
    )
  
  