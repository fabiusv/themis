#!/usr/bin/env python3
import os
import openai
import re
import json

#TODO 1: Return None if there is no need to search
def generateQueries(input_conversation, lang="en"):

	#main_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ".."))

	if lang == "en":
		prompt = lambda input: "Generate search queries for the last user message of a conversation. Make sure it is not ambigous by including all context.\nPut the one you believe to bring the best results to the top, prefer full questions. \nIf the question doesnt need a web search, respond with 'None'\n###\nConversation:\nUser: What is Apples current phone lineup?\nSearch: What is Apples current phone lineup?\nApple phone lineup\nCurrent apple Phone\n###\nPrevious Conversation:\nUser: When is Google IO\nAssistant: July 12\nUser: Will Sundar Pichar speak at the conference?\nSearch: \nWill Sundar Pichar speak at Google IO?\nSundar Pichai Google IO\n###\nPrevious Conversation:\nUser: Write an essay on a ban on cars in cities\nSearch:\nNone\n###\nConversation:\nUser: Repeat the last message\nSearch:\nNone\n###\nConversation:\nWho won the last super Bowl?\nSearch:\nLast super Bowl winner\nWho won the last Superbowl\n###\nConversation:\n" + input + "\nSearch:\n"
	elif lang == "de":
		prompt = lambda input: "Generate search queries for the last user message of a conversation if a search is required. Make sure it is not ambigous by including all context.\nPut the one you believe to bring the best results to the top, prefer full questions. If the user prompt doesnt need a web search, respond with 'None'\n###\nConversation:\nUser: What is Apples current phone lineup?\nSearch:\nWhat is Apples current phone lineup?\nApple phone lineup\nCurrent apple Phone\n###\nConversation:\nUser: Who founded Space X\nAssistant: SpaceX was founded by Elon Musk in 2004\nUser: How many children does he have?\nSearch:\nHow many children does Elon Musk have?\nchildren Elon Musk\n###\nConversation:\n" + input + "\nSearch:\n"
	else:
		raise ValueError("Language not supported") 

	openai.api_key = json.load(open("authentication/openai/openai_key.json"))["api_key"]
	
	response = openai.Completion.create(
	  model="text-babbage-001",
	  prompt= prompt(input_conversation),
	  temperature=0.7,
	  max_tokens=256,
	  top_p=1,
	  frequency_penalty=0,
	  presence_penalty=0,
	  stop=["###"]
	)
	
	response = response.choices[0].text
	queries = [x for x in response.split("\n") if x != '']
	if "None" in queries:
		return None
	return queries

print(generateQueries("Whats IBMs current Quantum Computer Called?"))
def generateQueriesNew(input_conversation, lang="en"):

	#main_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ".."))

	if lang == "en":
		prompt = lambda input: "Generate search queries for the last user message of a conversation. Make sure it is not ambigous by including all context.\nPut the one you believe to bring the best results to the top, prefer full questions.\n###\nConversation:\nUser: What is Apples current phone lineup?\nSearch:\nWhat is Apples current phone lineup?\nApple phone lineup\nCurrent apple Phone\n###\nConversation:\nUser: Who founded Space X\nAssistant: SpaceX was founded by Elon Musk in 2004\nUser: How many children does he have?\nSearch:\nHow many children does Elon Musk have?\nchildren Elon Musk\n###\nConversation:\n" + input + "\nSearch:\n}"
	elif lang == "de":
		prompt = lambda input: "Generate search queries for the last user message of a conversation. Make sure it is not ambigous by including all context.\nPut the one you believe to bring the best results to the top, prefer full questions.\n###\nConversation:\nUser: What is Apples current phone lineup?\nSearch:\nWhat is Apples current phone lineup?\nApple phone lineup\nCurrent apple Phone\n###\nConversation:\nUser: Who founded Space X\nAssistant: SpaceX was founded by Elon Musk in 2004\nUser: How many children does he have?\nSearch:\nHow many children does Elon Musk have?\nchildren Elon Musk\n###\nConversation:\n" + input + "\nSearch:\n}"
	else:
		raise ValueError("Language not supported") 

	openai.api_key = json.load(open("authentication/openai/openai_key.json"))["api_key"]
	
	response = openai.Completion.create(
	  model="text-babbage-001",
	  prompt= prompt(input_conversation),
	  temperature=0.7,
	  max_tokens=256,
	  top_p=1,
	  frequency_penalty=0,
	  presence_penalty=0,
	  stop=["###"]
	)
	
	response = response.choices[0].text
	queries = [x for x in response.split("\n") if x != '']
	
	return queries
#test call
#result = generateQueries("User: What is Apples current phone lineup?\nAssistant: Apple has the iPhone 12, 12 Pro and 12 Pro Max\nUser: What is the difference between the 12 and the 12 Pro?\nAssistant: The 12 Pro has a better camera and a better display\nUser: What is the difference between the 12 Pro and the 12 Pro Max?\nAssistant: The 12 Pro Max has a bigger display and a bigger battery\nUser: What is the difference between the 12 and the 12 Pro Max?\nAssistant: The 12 Pro Max has a bigger display and a bigger battery\nUser: What is the difference between the 12 and the 12 Pro Max?\nAssistant: The 12 Pro Max has a bigger display and a bigger battery\nUser: What is the difference between the 12 and the 12 Pro Max?\nAssistant: The 12 Pro Max has a bigger display and a bigger battery\nUser: What is the difference between the 12 and the 12 Pro Max?\nAssistant: The 12 Pro Max has a bigger display and a bigger battery\nUser: What is the difference between the 12 and the 12 Pro Max?\nAssistant: The 12 Pro Max has a bigger display and a bigger battery\nUser: What is the difference between the 12 and the 12 Pro Max?\nAssistant: The 12 Pro Max has a bigger display and a bigger battery\nUser: What is the difference between the 12 and the 12 Pro Max?\nAssistant: The 12 Pro Max has a bigger display and a bigger battery\nUser: What is the difference between the 12 and the 12 Pro Max?\nAssistant: The 12 Pro Max has a bigger display and a bigger battery\nUser: What is the difference between the 12 and the 12 Pro Max?\nAssistant: The 12 Pro Max has a bigger display and a bigger battery\nUser: What is the difference between the 12 and the 12 Pro Max?\nAssistant: The 12 Pro Max has a bigger display and a bigger battery\nUser: What is the difference between the 12 and the 12 Pro Max?\nAssistant: The 12 Pro Max has a bigger display and a bigger battery\nUser: What is the difference between the 12 and the 12 Pro Max?\nAssistant: The 12 Pro Max has a bigger display")
#print(result)