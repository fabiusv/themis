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
			tempChatHistory.append({"role": message.role, "content": message.content})
				
		return tempChatHistory
	def append(self, message):
		self.messages.append(message)
		return self
	