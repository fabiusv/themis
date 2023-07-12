import openai
import functions
import json

class IncompleteResponseError(Exception):
    pass

class Response():
    def __init__(self, result, error):
        self.result = result
        self.error = error

class OpenAIChat:
    def __init__(self, api_key):
        openai.api_key = json.load(open("authentication/openai/openai_key.json"))["api_key"]
    def sendConversation(self, conversation, function_call="auto"):
        try:
            response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo-0613",
                        messages=conversation.convertToOpenAI(),
                        functions= functions.openai_function_documentation,
                        function_call=function_call,
                    )
            
            try:
                response["choices"][0]["message"]
            except:
                raise IncompleteResponseError
            response = Response(response["choices"][0]["message"], None)

        except openai.error.RateLimitError:
            error_message = "Du hast zu viele anfragen geschickt, bitte warte einen moment."
            response = Response(None, error_message)

        except IncompleteResponseError:
            error_message = "Die antwort vom Server war fehlerhaft, bitte versuche es später erneut."
            response = Response(None, error_message)
        except openai.error.APIConnectionError: 
            error_messsage = "Der Server konnte keine Verbindung mit dem OpenAI Server herstellen."
            response = Response(None, error_messsage)
        except:
            error_message = "Es ist ein Fehler aufgetreten, bitte versuche es später erneut."
            response = Response(None, error_message)
            
        return response