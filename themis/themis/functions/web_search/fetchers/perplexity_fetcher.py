#!/usr/bin/env python3

import requests
from dotenv import load_dotenv
import os

def fetch_perplexity(searchquery):
	
    load_dotenv()

    api_key = os.getenv("perplexity_api_key")
    url = "https://api.perplexity.ai/chat/completions"
	
    payload = {
		"model": "llama-3-sonar-small-32k-online", #"llama-3-sonar-large-32k-online"
		"messages": [
			{
				"role": "system",
				"content": "Sei so genau wie möglich"
			},
			{
				"role": "user",
				"content": searchquery
			}
		]
	}
    headers = {
		"accept": "application/json",
		"content-type": "application/json",
		"authorization": "Bearer " + api_key
	}
	
    response = requests.post(url, json=payload, headers=headers)
    print("perplexity response")
    print(response.json())
	
    return "Übersetze dies in die Sprache der Frage, bevor du diese Information verwendest, um auf die ursprüngliche Frage zu antworten:"  + response.json()["choices"][0]["message"]["content"]
