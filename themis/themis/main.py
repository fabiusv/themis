import json
from .functions.function_dict import function_dict, openai_function_documentation
from .functions.web_search.search import performSearch
from .functions.maps.routes.routes import public_transport_route_fetching_handler

from .Dataclasses import *

from .OpenAIChatWrapper import OpenAIChat
from .localization.localizer import get_localization

class ThemisHandler():

	def __init__(self):
		self.chat_instance = OpenAIChat()
		self.conversation = Conversation() #FIXME: Do not use conversation as a class attribute as this does not ensure conversation integrity

	
	
	def completion(self, context):
		context = self.preprocess(context)

		self.conversation.messages = context.conversation.messages

		localization = get_localization(context.meta_data.language)

		self.conversation.messages = context.conversation.messages

		response = self.chat_instance.sendConversation(self.conversation, context)

		if not response.error:
			self.conversation.messages = response.result
		else:
			self.conversation.messages.append(ChatMessage(role="assistant", content="Ein Fehler ist aufgetreten."))
		return self.conversation.messages

	@staticmethod
	def preprocess(context):
			message = context.conversation.messages[-1].content
			if "notizen" in message.lower():
				print("Notizen")
				context.extra_functions.append({"type":"file_search"})
			return context