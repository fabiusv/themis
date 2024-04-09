import openai
from openai import OpenAI

from .functions import *
from .Dataclasses import ChatMessage
import json
import os
from dotenv import load_dotenv
import datetime


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

        
    def run_handler(self, run, context):


        if run.status == 'completed': 
            messages = list(self.client.beta.threads.messages.list(thread_id=run.thread_id))
            serialized_messages = [ChatMessage(role=message.role, content=message.content[0].text.value, id=message.id, created_at=message.created_at) for message in messages]
            return serialized_messages
        elif run.status == "requires_action":

            submit_id = run.required_action.submit_tool_outputs.tool_calls[0].id #TODO: loop over all tools
            function_name = run.required_action.submit_tool_outputs.tool_calls[0].name
            function_arguments = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].arguments)

            function_response = function_dict[function_name](context.meta_data, function_arguments)
            

            run = self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=run.thread_id,
                run_id=run.id,
                tool_outputs=[
                    {
                        "tool_call_id": submit_id,
                        "output": function_response,
                    }
                    ]
            )
            
            return self.run_handler(run)
        
    def sendConversation(self, conversation, context, function_call="auto"):
        from .functions.function_dict import function_dict

        try:
            messages=conversation.convert_openai_assistants()
            print(messages)
            thread = self.client.beta.threads.create(messages=messages)

            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id="asst_kibZn8oZdGDrWtcfJl9kJOVt",
                model="gpt-4-turbo-preview",
                #additional_messages=messages, # TODO: Add Metadata here with metadata_argument
                instructions="",
                tools=openai_function_documentation
                #tools=[{"type": "code_interpreter"}, {"type": "retrieval"}]
            )

            #TODO: serialize messages into ChatMessage Objects beforre returning
            response = Response(self.run_handler(run, context), None)
            
        except openai.RateLimitError:
            print(response)
            error_message = "Du hast zu viele anfragen geschickt, bitte warte einen moment."
            print(error_message)
            response = Response(None, error_message)

        except IncompleteResponseError:
            error_message = "Die antwort vom Server war fehlerhaft, bitte versuche es später erneut."
            print(error_messsage)
            response = Response(None, error_message)
        except openai.APIConnectionError: 
            error_messsage = "Der Server konnte keine Verbindung mit dem OpenAI Server herstellen."
            print(error_messsage)
            response = Response(None, error_messsage)

        print("The response is:")
        print(response.result)
        return response 