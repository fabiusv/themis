import openai
import json

openai.api_key = json.load(open("authentication/openai/openai_key.json"))["api_key"]

response = openai.ChatCompletion.create(
			model="gpt-3.5-turbo-0613",

			messages=[{"role": "system", "content": "The current date is: 15. June. The year is 2023!"}, {"role": "user", "content": "Who won the superbowl in 2020?"}],

			functions=[
                #Google Search
				{
					"name": "google_search",
					"description": "Search google for a answer to a question",
					"parameters": {
						"type": "object",
						"properties": {
							"searchquery": {
								"type": "string",
								"description": "The unambiguous search query generated from the conversation history",
							},

						},
						"required": ["searchquery"],
					},
				}, 
                #Weather
                {
                    "name": "weather",
                    "description": "Get the weather for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The location to get the weather for",
                            },
                        },
                        "required": ["location"],
                    },
                },
                #Wikipedia
                {
                    "name": "wikipedia",
                    "description": "Get a summary of a wikipedia article",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "The topic to get the wikipedia article for",
                            },
                        },
                        "required": ["topic"],
                    },
                },
                #Time
                {
                    "name": "time",
                    "description": "Get the current time",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The location to get the time for",
                            },
                        },
                       # "required": ["location"],
                    },
                },


			],
			function_call="auto",
		)
print(response)