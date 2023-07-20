import pytz
import datetime
from dateutil.relativedelta import relativedelta
import time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import parsedatetime as pdt # $ pip install parsedatetime


def nlp_time_parser_utc(date_string):
    print(date_string)
    try:
        cal = pdt.Calendar()
        # now in utc
        now = datetime.datetime.now()
        print(now)
        result = cal.parseDT(date_string, now)[0] 
        #result to utc
        result = result.astimezone(pytz.utc)
        print(result)
        formatted_time = result.strftime("%Y-%m-%dT%H:%M:%S.%f")
        formatted_time += 'Z'
        return formatted_time
    except:
        return None

    
def get_ISO_8601_formatted_datetime(location) -> str:
    if not location: #TODO: Or location is in germany
        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
        formatted_datetime += 'Z'
    else:
        timezone_name = get_timezone(location)
        timezone = pytz.timezone(timezone_name)
        now = datetime.datetime.now(timezone)
        formatted_datetime = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
    return formatted_datetime


def get_timezone(parameters):
    
    timezone_finder = TimezoneFinder()

    geolocator = Nominatim(user_agent="edith_country")
    location = geolocator.geocode(parameters)
    timezone = str(timezone_finder.timezone_at(lat=location.latitude, lng=location.longitude))
    return timezone

def get_time(meta_data, parameters):
    print(parameters)
    if parameters.get("location"):
        place = parameters["location"]
        timezone_name = get_timezone(place)
        timezone = pytz.timezone(timezone_name)
    else:
        
        if meta_data.timezone:
            timezone_name = meta_data.timezone
            timezone = pytz.timezone(timezone_name)
        elif meta_data.location:

            timezone_name = get_timezone(TimezoneFinder.timezone_at(lat=meta_data.location.latitude, lng=meta_data.location.longitude))
            timezone = pytz.timezone(timezone_name)
        else:
            now = datetime.datetime.now()
            return "Use this to respond to the question: " + now.strftime("%H:%M")  
        
    now = datetime.datetime.now(timezone)
    current_time = now.strftime("%H:%M")
    return  "The current time there is: " + current_time


def calculate_delta(parameters):
    today = datetime.datetime.now().date()
    futdate = datetime.datetime.strptime(parameters["date-time"], "%Y-%m-%dT%H:%M:%S%z").date()

    delta = (futdate - today).days
    if delta >= 0:
        if delta == 1:
            return "Das ist morgen."
        return "Use this to respond to the question: " + str(delta) + "Tage."
    else:
        return "Use this to respond to the question: Das war vor " + str(delta * -1) + "Tagen."


