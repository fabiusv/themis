
import pydantic
from .ChatMessage import ChatMessage

class Conversation(pydantic.BaseModel):
	messages: list[ChatMessage] = []
	def convertToOpenAI(self, remove_inserts = True):
		tempChatHistory = []
		for message in self.messages:
			print(message.content)
			if remove_inserts:
				if not message.is_insert:
					tempChatHistory.append({"role": message.role, "content": message.content})
			else:
				tempChatHistory.append({"role": message.role, "content": message.content})
		
		if self.messages[-1].is_insert:
			tempChatHistory.append({"role": self.messages[-1].role, "content": self.messages[-1].content})
		print("Last message: ")
		print(self.messages[-1].content)
		print(tempChatHistory)	
		return tempChatHistory
	def append(self, message):
		self.messages.append(message)
		return self
	def encode(self):
		return {"messages": [message.encode() for message in self.messages]}
	@staticmethod
	def decode(conversation_dict):
		return Conversation(messages=[ChatMessage.decode(message_dict) for message_dict in conversation_dict["messages"]])

