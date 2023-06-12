#!/usr/bin/env python3
import openai
import web_search
import json
from classification import dialogflow
#print(web_search.searchHandler("Wer hat den letzten Superbowl gewonnen?"))
#quit()

class ChatMessage:
	def __init__(self, role, content, is_insert = False, id=None):
		self.role = role
		self.content = content
		self.id = id
		self.is_insert = is_insert

class ChatHistory:
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
	

openai.api_key = json.load(open("authentication/openai/openai_key.json"))["api_key"]

#interactive version of the assistant
chatHistory = ChatHistory([ ChatMessage("system", "You are a virtual assistant like Jarvis in Ironman"), ChatMessage("user", "Today is the 18. of May. The year is 2023. At times you will recieve a snippet with the required Information to respond to the user question.\n The current username is Fabius.", 1), ChatMessage("assistant", "Okay, im ready.", 2)])
while True:
	input_str = input("You: ")
	#dialogflow_response = dialogflow.detect_intent_texts(1, input_str)

	chatHistory.messages.append(ChatMessage("user", input_str, False))

	search_insert = web_search.searchHandler(chatHistory)
	

	if search_insert != None:
		print("Not None")
		
		chatHistory.messages.append(ChatMessage("user", "Use this Information to respond: \n" + search_insert, True))
		
	#chatHistory.messages.append(ChatMessage("user", input_str, False))
	print(chatHistory.convertToOpenAI())
	#chatHistory.append(ChatMessage("user", input_str, False))
	#chatHistory.append({"role": "user", "content": input_str}) #implement custom chat history with id here to replace inserted text with the question only
	
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=chatHistory.convertToOpenAI(),
	)
	print(chatHistory.messages)
	print(chatHistory.convertToOpenAI())
	chatHistory.append(ChatMessage("assistant", response["choices"][0]["message"]["content"], False))
	print(response["choices"][0]["message"]["content"])

