#!/usr/bin/env python3
import openai
import web_search

openai.api_key_path = "credentials/openai.key"

#interactive version of the assistant
chatHistory = [{"role": "system", "content": "Today is the 15. of April 2023. Your training data cuts off on December 9. 2021."}, {"role": "user", "content": "You are a rude and sarcastic virtual assistant with your own opinions like Jarvis in Ironman. \n When required, the results of a up to date search will be inserted right after the prompt. \n The current username is Fabius."}, {"role": "assistant", "content": "Okay, im ready."}]

while True:
	input_str = input("You: ")
	#input_str2 = input("SearchPrompt: ")
	chatHistory.append({"role": "user", "content": input_str + "\n" + web_search.searchHandler(input_str) +"\n Use this search result to respond to the original question.\n"})
	#chatHistory.append({"role": "system", "content": })
	
	#chatHistory.append({"role": "assistant", "content": input_str + "\n Use the results of the search to continue the conversation. "})
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=chatHistory,
	)
	#print(response)
	chatHistory.append({"role": (response["choices"][0]["message"]["role"]), "content": response["choices"][0]["message"]["content"]})
	print(chatHistory[-1]["role"], ":", chatHistory[-1]["content"])
		
	
def insertedResultFormatter(result):
	return "\nThis result has been inserted and taken from the web\n+"



	#TODO: Remove inserted Tex



	