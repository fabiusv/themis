import google.oauth2.credentials
import google_auth_oauthlib.flow
import webbrowser
import json
import sys
import os


# Get the parent directory of the current script
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

client_secret_path = parent_dir + '/client_secret.json'
# Use the client_secret.json file to identify the application requesting
# authorization. The client ID (from that file) and access scopes are required.

print(sys.path)
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    client_secret_path,
    scopes=['https://www.googleapis.com/auth/dialogflow', "https://www.googleapis.com/auth/cloud-platform"])

# Indicate where the API server will redirect the user after the user completes
# the authorization flow. The redirect URI is required. The value must exactly
# match one of the authorized redirect URIs for the OAuth 2.0 client, which you
# configured in the API Console. If this value doesn't match an authorized URI,
# you will get a 'redirect_uri_mismatch' error.
flow.redirect_uri = 'https://google.com'

# Generate URL for request to Google's OAuth 2.0 server.
# Use kwargs to set optional request parameters.
authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')
    
#open browser
#print(authorization_url)
webbrowser.open(authorization_url)

url = input("Enter the url you were redirected to: ")


flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    client_secret_path,
    scopes=['https://www.googleapis.com/auth/dialogflow', "https://www.googleapis.com/auth/cloud-platform"],
    state=state)
flow.redirect_uri = "https://google.com"

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

#save credentials to file
with open(f"{parent_dir}/oauth/oauth.json", "w") as f:
    json.dump(json_credentials, f, indent=4)





##Load credentials from file
#google.oauth2.credentials.Credentials(json_credentials)