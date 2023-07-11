import openai
import json
import functions
from ChatClass import ChatMessage, Conversation 

#initialize openai api
openai.api_key = json.load(open("authentication/openai/openai_key.json"))["api_key"]
localization = json.load(open("localization/active"))


#Initialize chat conversation
conversation = Conversation()
conversation.messages = [ChatMessage("system", localization["default_conversation"])]

while True: #FIXME: Handle openai.error.RateLimitError 
	message = input("User: ")
	conversation.messages.append(ChatMessage("user", message))

	response = openai.ChatCompletion.create(
				model="gpt-3.5-turbo-0613",
				messages=conversation.convertToOpenAI(),
				functions= functions.openai_function_documentation,
				function_call="auto",
			)
	if response["choices"][0]["message"].get("function_call"):
		arguments = json.loads(response["choices"][0]["message"]["function_call"]["arguments"])
		name = response["choices"][0]["message"]["function_call"]["name"]


		function_response = functions.function_dict[name](arguments)
		print("reponse")
		
		conversation.messages.append(ChatMessage("user", function_response, True)) #TODO: Change system to user if required
		
		response = openai.ChatCompletion.create(
				model="gpt-3.5-turbo-0613",
				messages=conversation.convertToOpenAI(),
				functions= functions.openai_function_documentation,
				function_call="none",
		)
		
		conversation.messages.append(ChatMessage("user", response["choices"][0]["message"]["content"])) 
		print(response)
		print("Response: ")
		print(response["choices"][0]["message"]["content"])
	else:
		conversation.messages.append(ChatMessage("user", response["choices"][0]["message"]["content"]))
		print(response["choices"][0]["message"]["content"])

	

