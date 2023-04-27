#!/usr/bin/env python3
import openai
import web_search
import json
#print(web_search.searchHandler("Wer hat den letzten Superbowl gewonnen?"))
#quit()

openai.api_key = json.load(open("authentication/openai/openai_key.json"))["api_key"]

#interactive version of the assistant
chatHistory = [{"role": "system", "content": "Today is the 15. of April 2023. Your training data cuts off on December 9. 2021."}, {"role": "user", "content": "You are a sarcastic virtual assistant with your own opinions like Jarvis in Ironman. \n When required, the results of a up to date search will be inserted right after the prompt. \n The current username is Fabius."}, {"role": "assistant", "content": "Okay, im ready."}]

while True:
	input_str = input("You: ")
	
	search_insert = web_search.searchHandler(input_str)

	if search_insert != None:
		print("Not None")
		chatHistory.append({"role": "user", "content": search_insert})

	chatHistory.append({"role": "user", "content": input_str})
	#chatHistory.append({"role": "user", "content": input_str}) #implement custom chat history with id here to replace inserted text with the question only

	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=chatHistory,
	)

	chatHistory.append({"role": (response["choices"][0]["message"]["role"]), "content": response["choices"][0]["message"]["content"]})
	print(chatHistory[-1]["role"], ":", chatHistory[-1]["content"])
