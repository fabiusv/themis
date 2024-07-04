from pymstodo import ToDoConnection
from dotenv import load_dotenv, find_dotenv, set_key
import json
import os

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)


client_id = os.getenv("client_id_ms_graph")
client_secret = os.getenv("client_secret_ms_graph")

auth_url = ToDoConnection.get_auth_url(client_id)
redirect_resp = input(f'Go here and authorize:\n{auth_url}\n\nPaste the full redirect URL below:\n')
token = ToDoConnection.get_token(client_id, client_secret, redirect_resp)  # you have to save it somewhere
os.environ["ms_graph_oauth"] = json.dumps(token)
set_key(dotenv_file, "ms_graph_oauth", os.environ["ms_graph_oauth"])
