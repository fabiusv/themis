import requests
import json
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
client_secret_path = parent_dir + '/client_secret.json'

#load client_id from client_secret.json
client_id = json.load(open(client_secret_path))["web"]["client_id"]
#load client_secret from client_secret.json
client_secret = json.load(open(client_secret_path))["web"]["client_secret"]
#load refresh_token from oauth.json
refresh_token = json.load(open(f"{parent_dir}/oauth/oauth.json"))["refresh_token"]
print(refresh_token)

url = 'https://www.googleapis.com/oauth2/v4/token'
headers = {'Content-Type': 'application/json'}

data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'refresh_token': refresh_token,
    'grant_type': 'refresh_token'
}

response = requests.post(url, headers=headers, json=data)


response = response.json()



json_credentials = {
    'token': response["access_token"],
    'refresh_token': refresh_token,
    'token_uri': "https://oauth2.googleapis.com/token",
    'client_id': client_id,
    'client_secret': client_secret,
    'scopes': response["scope"].split(" ")
}


with open(parent_dir + "/oauth/oauth.json", "w") as f:
    json.dump(json_credentials, f, indent=4)