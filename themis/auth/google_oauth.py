import google.oauth2.credentials
import google_auth_oauthlib.flow
import webbrowser
import json
import sys
import os
from dotenv import load_dotenv, find_dotenv, set_key

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

cs = json.loads(os.getenv("client_secret_google"))
flow = google_auth_oauthlib.flow.Flow.from_client_config(
    cs,
    scopes=['https://www.googleapis.com/auth/dialogflow', "https://www.googleapis.com/auth/cloud-platform", 'https://www.googleapis.com/auth/calendar'],
    state='state'
)

flow.redirect_uri = 'https://google.com'

authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')
    

webbrowser.open(authorization_url)

url = input("Enter the url you were redirected to: ")

oauth_acess = flow.fetch_token(authorization_response=url)
credentials = flow.credentials

print(credentials.refresh_token)

json_credentials = {
    'token': credentials.token,
    'refresh_token': credentials.refresh_token,
    'token_uri': credentials.token_uri,
    'client_id': credentials.client_id,
    'client_secret': credentials.client_secret,
    'scopes': credentials.scopes
}


os.environ["oauth_google"] = json.dumps(json_credentials)
set_key(dotenv_file, "oauth_google", os.environ["oauth_google"])


