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

		localization = get_localization(context.meta_data.language)

		self.conversation.messages = context.conversation.messages
		initial_response = self.chat_instance.sendConversation(self.conversation)
		

		if initial_response.result and initial_response.result.finish_reason=="function_call":
			
			arguments = initial_response.result.message.function_call.arguments
			arguments = json.loads(arguments)

			name = initial_response.result.message.function_call.name

			function_response = function_dict[name](context.meta_data, arguments)
			
			self.conversation.messages.append(ChatMessage(role="user", content=function_response, is_insert=True))
			
			response = self.chat_instance.sendConversation(self.conversation, "none")

			self.conversation.messages.append(ChatMessage(role="assistant", content=response.result.message.content)) #type: ignore

			return self.conversation.messages
			

	#no function call required:
		elif initial_response.result:
			response = initial_response.result.message.content
			self.conversation.messages.append(ChatMessage(role="assistant", content=response))
			return self.conversation.messages

	#Error handling
		else:
			print(initial_response)		
			print(initial_response.error)
			raise Exception("Error in completion function")
		


if __name__ == "__main__":
	localization = localization = get_localization("de")

	chat_instance = OpenAIChat()

	print("chat instance created")
	#Initialize chat conversation
	conversation = Conversation()
	conversation.messages = [ChatMessage(role="system", content=localization["default_conversation"])]

	while True: #FIXME: Handle openai.error.RateLimitError 
		message = input("User: ")
		conversation.messages.append(ChatMessage(role="user", content=message))
		
		response = chat_instance.sendConversation(conversation)

		#function call required
		if response.result and response.result.get("function_call"):

			response = response.result
			arguments = json.loads(response["function_call"]["arguments"])
			name = response["function_call"]["name"]

			function_response = function_dict[name](arguments)
			
			conversation.messages.append(ChatMessage(role="user", content=function_response, is_insert=True))
			
			response = chat_instance.sendConversation(conversation, "none")
			response = response.result #FIXME: Change variable name to prevent confusion

			conversation.messages.append(Dataclasses.ChatMessage(role="user", content=response["content"]))  #type: ignore

		#no function call required:
		elif response.result:
			response = response.result
			conversation.messages.append(ChatMessage(role="user", content=response["content"]))
			print(response["content"])

		#Error handling
		else:
			#error_message has been definitly set
			
			print(response.error) #return to client 
