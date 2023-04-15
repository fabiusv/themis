#!/usr/bin/env python3


def generateQueries(input_conversation):
	import os
	import openai
	import re

	openai.api_key_path = "openai.key"
	
	response = openai.Completion.create(
	  model="text-babbage-001",
	  prompt="Generate search queries for the last user message of a conversation. Make sure it is not ambigous by including all context.\nPut the one you believe to bring the best results to the top, prefer full questions.\n###\nConversation:\nUser: What is Apples current phone lineup?\nSearch:\nWhat is Apples current phone lineup?\nApple phone lineup\nCurrent apple Phone\n###\nConversation:\nUser: Who founded Space X\nAssistant: SpaceX was founded by Elon Musk in 2004\nUser: How many children does he have?\nSearch:\nHow many children does Elon Musk have?\nchildren Elon Musk\n###\nConversation:\n" + input_conversation + "\nSearch:\n}",
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



