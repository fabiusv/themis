from google.cloud import dialogflow_v2beta1 as dialogflow
import json
import requests


bearer_token = json.load(open("authentication/gcloud/oauth/oauth.json"))["token"]
#get key from credentials/gcloud_api.json
key = json.load(open("authentication/gcloud/client_api_key.json"))["api_key"]

def detect_intent_texts(session_id, texts, lang):
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
    print(response.json()["queryResult"]["parameters"])

print(detect_intent_texts("1", "When will WWDC take place?", "en"))