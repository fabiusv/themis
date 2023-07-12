import openai
import json
import functions
from ChatClass import ChatMessage, Conversation 
from ChatWrapper import OpenAIChat
from extensions import safe_list_get
#initialize openai api
openai.api_key = json.load(open("authentication/openai/openai_key.json"))["api_key"]
localization = json.load(open("localization/active.json"))


chat_instance = OpenAIChat(openai.api_key)
#Initialize chat conversation
conversation = Conversation()
conversation.messages = [ChatMessage("system", localization["default_conversation"])]

while True: #FIXME: Handle openai.error.RateLimitError 
	message = input("User: ")
	conversation.messages.append(ChatMessage("user", message))
	
	response = chat_instance.sendConversation(conversation)

	#function call required
	if response.result and response.result.get("function_call"):

		response = response.result
		arguments = json.loads(response["function_call"]["arguments"])
		name = response["function_call"]["name"]

		function_response = functions.function_dict[name](arguments)
		
		conversation.messages.append(ChatMessage("user", function_response, True))
		
		response = chat_instance.sendConversation(conversation, "none")
		response = response.result #FIXME: Change variable name to prevent confusion

		conversation.messages.append(ChatMessage("user", response["content"])) 
		print(response["content"])

	#no function call required:
	elif response.result:
		response = response.result
		conversation.messages.append(ChatMessage("user", response["content"]))
		print(response["content"])

	#Error handling
	else:
		#error_message has been definitly set
		
		print(response.error) #return to client 
		

