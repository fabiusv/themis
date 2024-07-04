import openai
from openai import OpenAI
from .functions import *
from .Dataclasses import ChatMessage
import json
import os
from dotenv import load_dotenv
import datetime#

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
        print("Inititated new run")
        while run.status != "completed" and run.status != "requires_action" and run.status != "failed":
            print(run.status)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=run.thread_id,
                run_id=run.id,
            )

        if run.status == 'completed': 
            messages = list(self.client.beta.threads.messages.list(thread_id=run.thread_id))
            print(messages)
            print("MESSAGE")
            serialized_messages = []
            for message in messages:
                #error handling until openai fixes the wrong serialization of the content
                try:
                    new_message = ChatMessage(role=message.role, content=message.content[0].text["value"], id=message.id, created_at=message.created_at)
                except: 
                    new_message = ChatMessage(role=message.role, content=message.content[0].text.value, id=message.id, created_at=message.created_at)
                serialized_messages.append(new_message)
            print(serialized_messages)
            return serialized_messages[::-1]
        elif run.status == "requires_action":
            tool_outputs = []
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                
                submit_id = tool.id #TODO: loop over all tools
                print(run.required_action.submit_tool_outputs.tool_calls)
                function_name = tool.function.name
                function_arguments = json.loads(tool.function.arguments)
                print("Function name")
                print(function_name)
                print(function_arguments)
                print(context.meta_data)
                function_response = function_dict[function_name](context.meta_data, function_arguments)
                tool_outputs.append({"tool_call_id": submit_id, "output": function_response})
            

            run = self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=run.thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
                    
            )
            
            print("Submitting tool outputs")
            print(function_response)

            return self.run_handler(run, context)
        else:
            print("It failed")
            print(run.status)
            print(run.error)

    def sendConversation(self, conversation, context, function_call="auto"):
        from .functions.function_dict import function_dict

        try:
            messages=conversation.convert_openai_assistants()
            print(messages)
            thread = self.client.beta.threads.create(messages=messages)
            function_doc = openai_function_documentation.copy()
            
            for i in context.extra_functions:
                function_doc.append(i)
                print("documented function")
                
            additional_instructions =  "Das aktuelle Datum und die Zeit sind: " + str(datetime.datetime.now()) + "\n Da du ein Sprachassistent bist werden deine Antworten auch vorgelesen. Formuliere deine Antworten also so dass sie gut vorgelesen werden können (Fließtext) statt auf Formatierung zu setzen "

            if not {"type":"file_search"} in context.extra_functions:
                    additional_instructions += "Du hast gerade keinen Zugriff auf die Notizen und Dateien des Benutzers."


            run = self.client.beta.threads.runs.create_and_poll(
                additional_instructions=additional_instructions,
                thread_id=thread.id,
                assistant_id="asst_EJBV4oI54JxQ64YYALeR83Qz",
                model="gpt-4o",
                
                #additional_messages=messages, # TODO: Add Metadata here with metadata_argument
                instructions="",
                tools=function_doc,
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
        except Exception as e:
            print(e)
            error_message = e
            response = Response(None, error_message)
        print("The response is:")
        print(response.result)
        return response 
    def upload_files(self, vector_store_id, file_paths):
        
        vector_store = self.client.beta.vector_stores.retrieve(vector_store_id=vector_store_id)

        file_list = list(self.client.beta.vector_stores.files.list(vector_store_id=vector_store_id))
        id_list = [file.id for file in file_list]
        for file_id in id_list:
            self.client.files.delete(file_id)

        
        print(file_paths)
        file_streams = [open(path, "rb") for path in file_paths]
        
        
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id, files=file_streams
        )