class ChatMessage:
	def __init__(self, role, content, is_insert = False, id=None):
		self.role = role
		self.content = content
		self.id = id
		self.is_insert = is_insert

class Conversation:
	def __init__(self, messages = []):
		self.messages = messages
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
	