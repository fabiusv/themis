import requests
import urllib.parse
import json
import os

def fetch_places_json(meta_data, query, isOpen=False, radius=None):

    #query, isOpen, radius, location
    query = query

    key = os.getenv("gcloud_api_key")


    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+ urllib.parse.quote(query) + "&inputtype=textquery&fields=plus_code%2Cname%2Crating%2Copening_hours%2Cgeometry" + "&key=" + key

    payload={}
    headers = {}

    response = requests.get(url)
    #serialize response ?
    if response.status_code == 200:
        return response.json()
    else:
        return None


#print(fetch_places_json(None, "restaurant"))