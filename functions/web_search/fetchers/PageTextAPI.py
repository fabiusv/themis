import requests
from bs4 import BeautifulSoup
import os
import json



class Page():
    def __init__(self, title, url, text=""):
        self.title = title
        self.text = text
        self.url = url
    

def fetch_google_results(query, lang="en"):
    import requests
    
    key = json.load(open("authentication/gcloud/client_api_key.json"))["api_key"]
    url = 'https://customsearch.googleapis.com/customsearch/v1'
    
    if lang == "en":
        cx = "c4415157c33794318"
        #print("English")
    elif lang == "de":
        cx = "6597a0405f56c4d3e"
        #print("Deutsch")

    params = {
        'cx': cx,
        'q':query,
        'key': key
    }
    headers = {'Accept': 'application/json'}
    response = requests.get(url, params=params, headers=headers)
    
    pages = []
    for item in response.json()["items"]:
        #print(item["description"])
        print(item)
        pages.append(Page(item["title"], item["link"]))
    
    return pages

