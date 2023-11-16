import requests
import urllib.parse
import json
import os
from dotenv import load_dotenv


def fetch_places_json(meta_data, query, isOpen=False, radius=None):

    load_dotenv()

    #query, isOpen, radius, location
    query = query

    key = os.getenv("gcloud_api_key")


    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+ urllib.parse.quote(query) + "&inputtype=textquery&fields=plus_code%2Cname%2Crating%2Copening_hours%2Cgeometry" + "&key=" + key

    payload={}
    headers = {}

    response = requests.get(url)
    print(response.json())
    #serialize response ?
    if response.status_code == 200:
        return response.json()
    else:
        return None


#print(fetch_places_json(None, "restaurant"))

def place_search(meta_data, query, num_places=3):

    if num_places > 10:
        num_places = 10 #FIXME: Make failsafe is num places is higher than list length

    load_dotenv()

    key = os.getenv("gcloud_api_key")

    url = 'https://places.googleapis.com/v1/places:searchText'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': key,
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel,places.regularOpeningHours,places.rating,places.plusCode'#TODO: Calculate rating with 3B1B method
    }
    print("Lat", meta_data.location.lat)
    print("Lng", meta_data.location.lng)

    data = {
        "textQuery": query,
        "locationBias": {
        "circle": {
            "center": {
            "latitude": meta_data.location.lat,
            "longitude": meta_data.location.lng
            },
            "radius": 4000.0 #in meters
        }
}
    }
    print(data)
    response = requests.post(url, json=data, headers=headers)
    print("-"*50)
    print(response.json())
    places = response.json()["places"][0:num_places]
    print(places)
    return places
    


#DEBUGGING
import pydantic # type: ignore

class Location(pydantic.BaseModel):
    lat: float
    lng: float


class MetaData(pydantic.BaseModel):
  location: Location
  timezone: str
  language: str

#print(place_search(MetaData(location=Location(lat=52.520008, lng=13.404954), timezone="UTC", language="en"), "asiatisches essen wachenheim an der weinstraße"))


def place_search_handler(meta_data, arguments):

    query = arguments.get("query")
    num_places = arguments.get("num_places")
    

    places = place_search(meta_data, query, num_places)

    formatted_string = ""

    for place in places:
         
        name = place["displayName"]["text"]
        formatted_address = place["formattedAddress"]
        try:
            is_open = place["regularOpeningHours"]["openNow"]
            opening_hours = place["regularOpeningHours"]["weekdayDescriptions"]
            rating = place["rating"]

        except:
            continue
        

        formatted_string += name + ":\nAddress: " + formatted_address + "\nIs Open: " + str(is_open) + "\nOpening hours: " + str(opening_hours) + "\nRating: " + str(rating) + "\n\n"

    return formatted_string

