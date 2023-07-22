from bs4 import BeautifulSoup
import os
import json
import requests
from ....localization.localizer import get_localization
import os

class Page():
    def __init__(self, title, url, text=""):
        self.title = title
        self.text = text
        self.url = url
    
    

def fetch_google_results(meta_data, query, lang="en"):
    localization = get_localization(meta_data.language)

    
    key = os.getenv("gcloud_api_key")
    url = 'https://customsearch.googleapis.com/customsearch/v1'
    
    if localization["language_identifiers"]["short"] == "en":
        cx = "c4415157c33794318"
        #print("English")
    else:
        cx = "6597a0405f56c4d3e"
        #print("Deutsch")

    params = {
        'cx': cx,
        'q':query,
        'key': key
    }

    print(params)
    headers = {'Accept': 'application/json'}
    response = requests.get(url, params=params, headers=headers)
    print(response.json())
    pages = []
    for item in response.json()["items"]:
        pages.append(Page(item["title"], item["link"]))
    
    return pages

