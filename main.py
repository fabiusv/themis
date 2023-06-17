import openai
import json
import functions
from ChatClass import ChatMessage, Conversation 

#initialize openai api
openai.api_key = json.load(open("authentication/openai/openai_key.json"))["api_key"]

#Initialize chat conversation
conversation = Conversation()
conversation.messages = [ChatMessage("system", "The current date is: 15. June. The year is 2023. If you require real time information on a topic that could have changed since your training stoped, fallback to the realtime_websearch function. This can be used multiple times throughout the conversation.")]

while True:
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

		conversation.messages.append(ChatMessage("user", function_response, True))
		
		response = openai.ChatCompletion.create(
				model="gpt-3.5-turbo-0613",
				messages=conversation.convertToOpenAI(),
				functions= functions.openai_function_documentation,
				function_call="auto",
		)
		
		conversation.messages.append(ChatMessage("user", response["choices"][0]["message"]["content"]))
		print(response["choices"][0]["message"]["content"])
	else:
		conversation.messages.append(ChatMessage("user", response["choices"][0]["message"]["content"]))
		print(response["choices"][0]["message"]["content"])

	

