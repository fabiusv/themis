import openai
from openai import OpenAI

from .functions import *
import json
import os
from dotenv import load_dotenv



class IncompleteResponseError(Exception):
    pass

class Response():
    def __init__(self, result, error):
        self.result = result
        self.error = error

class OpenAIChat:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("openai_api_key"))

        #print("key: \n \n \n \n")
        #
        # print(os.getenv("openai_api_key"))
        
    def sendConversation(self, conversation, function_call="auto"):
        try:
            response = self.client.chat.completions.create(model="gpt-3.5-turbo-0613",  #
            messages=conversation.convertToOpenAI(),
            functions= openai_function_documentation,
            function_call=function_call)
            
            try:
                print("Response:")
                print(response.choices[0])
            
                response = Response(response.choices[0], None)
            except:
                raise IncompleteResponseError
        except openai.RateLimitError:
            error_message = "Du hast zu viele anfragen geschickt, bitte warte einen moment."
            response = Response(None, error_message)

        except IncompleteResponseError:
            error_message = "Die antwort vom Server war fehlerhaft, bitte versuche es später erneut."
            response = Response(None, error_message)
        except openai.APIConnectionError: 
            error_messsage = "Der Server konnte keine Verbindung mit dem OpenAI Server herstellen."
            response = Response(None, error_messsage)
        #except:
            
          #  error_message = "Es ist ein Fehler aufgetreten, bitte versuche es später erneut."
         #   response = Response(None, error_message)
            
        return response