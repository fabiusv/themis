import requests
import urllib.parse
import json


def fetch_places_json(query, isOpen=False, radius=None, location=None):

    #query, isOpen, radius, location
    query = query

    key = json.load(open("authentication/maps_platform/maps_platform_key.json"))["api_key"]


    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+ urllib.parse.quote(query) + "&inputtype=textquery&fields=plus_code%2Cname%2Crating%2Copening_hours%2Cgeometry" + "&key=" + key

    payload={}
    headers = {}

    response = requests.get(url)
    #serialize response ?
    if response.status_code == 200:
        return response.json()
    else:
        return None

