import requests
import datetime
from ...time.time import get_ISO_8601_formatted_datetime, nlp_time_parser



def fetch_routes(start_location, end_location, travel_mode, departure_time=None):
  headers = {
      'Content-Type': 'application/json',
      'X-Goog-Api-Key': 'AIzaSyCAElPq9PZ7LffK77cxj_Aa5AryJT0r-Ko',
      'X-Goog-FieldMask': '*',
  }

  json_data = {
      'origin': {
          "address": start_location,
      },
      'destination': {
          "address": end_location,
          
          
      },
      'travelMode': travel_mode,
      #'routingPreference': 'TRAFFIC_AWARE',
      'departureTime': departure_time or "",
      'computeAlternativeRoutes': False,
      'routeModifiers': {
          'avoidTolls': False,
          'avoidHighways': False,
          'avoidFerries': False,
      },
      'languageCode': 'de-DE',
      'units': 'METRIC',
  }

  response = requests.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, json=json_data)
  print("Response: #############")

  print(response.json())
  
  print("#############")
  return response.json()["routes"][0]

class Section:
    def __init__(self, travel_mode, instructions, start_index, stop_index, all_steps) -> None:
        
        self.steps = all_steps[start_index:stop_index + 1]
        self.travel_mode = travel_mode
        self.navigation_instruction = instructions
    def get_travel_time(self):
        counter = 0
        for step in self.steps:
          staticDuration = int(step["staticDuration"][0:-1])
          counter += staticDuration
        return counter


def generate_sections(steps, segments):
  sections = []
  for segment in segments:
      try:
        section = Section(segment["travelMode"], segment["navigationInstruction"]["instructions"], segment["stepStartIndex"], segment["stepEndIndex"], steps)
      except:
        section = Section(segment["travelMode"], "None", segment["stepStartIndex"], segment["stepEndIndex"], steps)
      sections.append(section)
  return sections



#Processing

def get_formatted_sections(sections):
  counter = 1
  final_string = ""
  for section in sections:
      
      #      temp = "Der " + str(counter) + ". Abschnitt hat die Reisemethode: " + section.travel_mode + " und die Anweisung: "  + section.navigation_instruction
      if section.steps[0]["travelMode"] == "TRANSIT":
        temp = str(counter) +". "+ section.navigation_instruction + ". Abfahrt um: " + section.steps[0]["transitDetails"]["localizedValues"]["departureTime"]["time"]["text"]  + ". Dauer: " + str(section.get_travel_time()//60) + " Minuten. "
      else:
        temp = str(counter) +". "+ section.travel_mode + section.navigation_instruction + ". Dauer: " + str(section.get_travel_time()//60) 
      counter += 1
      final_string += temp
    
  return final_string



def public_transport_route_fetching_handler(arguments, lang="en"):
  format_order = "Format this information in a flowing text that can be read out by a virtual assistant:\n"
  start_location = arguments.get("origin") or "Wachenheim" #TODO: Use current user supplied location
  print(start_location)
  end_location = arguments["destination"]
  print(end_location)
  
  departure_time = nlp_time_parser(arguments.get("departure_time"))
  print(departure_time)
  #current date string:
  datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
  route = fetch_routes(start_location, end_location, "TRANSIT", departure_time)
  duration_text = route["localizedValues"]["duration"]["text"]
  distance_text = route["localizedValues"]["distance"]["text"]
  steps = route["legs"][0]["steps"]
  segments = route["legs"][0]["stepsOverview"]["multiModalSegments"]
  sections = generate_sections(steps, segments)
  formatted_sections = get_formatted_sections(sections)
  formatted_route = format_order +  "Die Route dauert " + duration_text + " und ist " + distance_text + " lang. \n" + "Sie besteht aus den folgenden Abschnitten:\n" + formatted_sections
  return formatted_route


