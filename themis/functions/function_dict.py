from .web_search.search import performSearch
from .time.time import get_time
import datetime
from .maps.routes.routes import public_transport_route_fetching_handler

function_dict = {
    "realtime_websearch": performSearch,
    "get_time": get_time,
    "public_transport_information" : public_transport_route_fetching_handler,
    
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
                    "name": "get_weather",
                    "description": "Get the weather for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The location to get the weather for",
                            },
                            "time": {
                                "type": "string",
                                "description": "The ISO formatted date to get the weather for. The current ISO date is: " + str(datetime.datetime.now()),
                            },
                        },
                        "required": ["location"],
                    },
                },
                
                #Time
                {
                    "name": "get_time",
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
                {
                    "name": "public_transport_information",
                    "description": "Get the next train from A to B, including the time it takes to walk to the station",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "origin": {
                                "type": "string", 
                                "description": "The origin location",
                            },
                            "destination": {
                                "type": "string",
                                "description": "The destination location",
                            },
                            "en_departure_time": {
                                "type": "string",
                                "description": "The string date expression of the departure time. Allways translate to english",
                            },
                            "en_arrival_time": {
                                "type": "string",
                                "description": "The string date expression of the wished arrival time. Allways translate to english",
                            }

                        },
                       "required": ["destination"],
                    },
                },


			]