from .web_search.search import performSearch
function_dict = {
    "realtime_websearch": performSearch,
}

openai_function_documentation = [
                #Google Search
				{
					"name": "realtime_websearch",
					"description": "Search google for an answer to a question",
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
                
                #Time
                {
                    "name": "time",
                    "description": "Get the current time, only if the user specifically asks for it",
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


			]