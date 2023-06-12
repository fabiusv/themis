from google.cloud import dialogflow_v2beta1 as dialogflow
import json
import requests
from features import intent_function_dict as ifd

class DialogflowIntentResponse:
    def __init__(self, intent, parameters):
        self.intent_function =  intent
        self.parameters = parameters
    def __str__(self):
        return "Intent:\n" + self.intent + "\nParameters:\n" + str(self.parameters)
bearer_token = json.load(open("authentication/gcloud/oauth/oauth.json"))["token"]
#get key from credentials/gcloud_api.json
key = json.load(open("authentication/gcloud/client_api_key.json"))["api_key"]

def detect_intent_texts(session_id, texts, lang="en"):
    print("intent detector called")
    #en-US
    project_id = "llm-assistant-1679252411498"

    url = 'https://dialogflow.googleapis.com/v2/projects/llm-assistant-1679252411498/agent/environments/draft/users/1/sessions/12:detectIntent?key=' + key

    headers = {
        'Authorization': 'Bearer ' + bearer_token,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        'queryInput': {
            'text': {
                'text': texts,
                'languageCode': lang
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    print("intent request finished")
    
    
    function_ref = ifd.translation[response.json()["queryResult"]["intent"]["displayName"]]

    return DialogflowIntentResponse(function_ref, response.json()["queryResult"]["parameters"])
    



