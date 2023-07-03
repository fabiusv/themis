import openai
import json
import functions
from ChatClass import ChatMessage, Conversation 

#initialize openai api
openai.api_key = json.load(open("authentication/openai/openai_key.json"))["api_key"]

#Initialize chat conversation
conversation = Conversation()
conversation.messages = [ChatMessage("system", "The current date is: 15. June. The year is 2023. Perform a web-search on time sensitive topics that could have changed or you just dont know. Always perform a search, before claiming you dont know the answer.,")]

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
		print(function_response)

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

	

