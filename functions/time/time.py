import pytz
import datetime
from dateutil.relativedelta import relativedelta
import time
from geopy.geocoders import Nominatim
from tzwhere import tzwhere



def get_timezone(parameters):
    
    timezone_finder = tzwhere.tzwhere()

    geolocator = Nominatim(user_agent="edith_country")
    location = geolocator.geocode(parameters)
    timezone = str(timezone_finder.tzNameAt(location.latitude, location.longitude))
    return timezone

def get_time(parameters):
    print(parameters)
    if parameters.get("location"):
        place = parameters["location"]
    else:
        now = datetime.datetime.now()
        return "Use this to respond to the question: " + now.strftime("%H:%M")
    timezone_name = get_timezone(place)
    timezone = pytz.timezone(timezone_name)
    now = datetime.datetime.now(timezone)
    current_time = now.strftime("%H:%M")
    return  "Use this to respond to the question: " + current_time


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


