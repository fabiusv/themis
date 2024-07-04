import datetime
import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

class Calendar():
    def __init__(self) -> None:
        
        creds = None

        load_dotenv()

        cs = json.loads(os.getenv("oauth_google"))
        print(cs)
        creds = Credentials(
            cs["token"],
            refresh_token=cs["refresh_token"],
            token_uri=cs["token_uri"],
            client_id=cs["client_id"],
            client_secret=cs["client_secret"],
            scopes=cs["scopes"]
        )

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                raise ValueError("No valid credentials found")

        try:
            self.service = build("calendar", "v3", credentials=creds)
        except HttpError as error:
            print(f"An error occurred: {error}")


    def fetch_calendar(self, max_results, start_time):
        
        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=start_time,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            
            return "No upcoming events found."

        # Prints the start and name of the next 10 events
        event_summary = "ID und Name | Startzeit in ISO Format\n"
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            event_summary += f"ID von '{event['summary']}': {event['id']}, {start}\n"
        return event_summary
        
    def search(self, text_query, end_time=None, start_time=datetime.datetime.utcnow().isoformat() + "Z", maxResults=10):
        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=start_time,
                timeMax=end_time,
                q=text_query,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        event_summary = ""
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            event_summary += f"{start} - {event['summary']} - {event["id"]}\n"
        return event_summary
    
    def edit_event(self, event_id, start=None, end=None, title=None):
        #Edit only the given parameters
        event = self.service.events().get(calendarId="primary", eventId=event_id).execute()
        if start is not None:
            event["start"]["dateTime"] = start
        if end is not None:
            event["end"]["dateTime"] = end
        if title is not None:
            event["summary"] = title
        event = self.service.events().update(calendarId="primary", eventId=event_id, body=event).execute()
        return "Das Event " + event["summary"] + " wurde erfolgreich bearbeitet und hat nun die ID: " + event["id"] + " und startet um " + event["start"]["dateTime"] + " und endet um " + event["end"]["dateTime"] + "."

    def create_event(self, start, end, title=None):
        event = {
            "summary": title,
            "start": {"dateTime": start, "timeZone": "Europe/Berlin"},
            "end": {"dateTime": end, "timeZone": "Europe/Berlin"},
        }
        event = self.service.events().insert(calendarId="primary", body=event).execute()
        print(event)
        return "Die ID von " + event["summary"] + " ist: " + event["id"] + " Bedenke dass dieses Event jetzt existiert und wenn es bearbeit werden soll du diese ID benötigst statt ein neues zu erstellen."

    def move_event(self, event_id, start, end):
        event = self.service.events().get(calendarId="primary", eventId=event_id).execute()
        event["start"]["dateTime"] = start
        event["end"]["dateTime"] = end
        event = self.service.events().update(
            calendarId="primary", eventId=event_id, body=event
        ).execute()
        return "Das Event " + event["summary"] + " wurde erfolgreich verschoben und hat nun die ID: " + event["id"]# + " und startet um " + event["start"]["dateTime"] + " und endet um " + event["end"]["dateTime"] + ".

    def delete_event(self, event_id):
        self.service.events().delete(calendarId="primary", eventId=event_id).execute()
        return "Das Event wurde erfolgreich gelöscht. "

class CalendarHandler():
    @staticmethod
    def fetch_calendar(meta_data, arguments):
        max_results = arguments.get("max_results") 
        if max_results is None:
            max_results = 40
        start_time = arguments.get("start_time")
        if start_time is None:
            start_time = datetime.datetime.utcnow().isoformat() + "Z"

        cal = Calendar()
        return cal.fetch_calendar(max_results, start_time)
    @staticmethod
    def search(meta_data, arguments):
        text_query = arguments.get("text_query")
        start_time = arguments.get("start_time")
        if start_time is None:
            start_time = datetime.datetime.utcnow().isoformat() + "Z"
        end_time = arguments.get("end_time")
        cal = Calendar()
        return cal.search(text_query, end_time, start_time)
    @staticmethod
    def create_event(meta_data, arguments):
        start = arguments.get("start")
        end = arguments.get("end")
        title = arguments.get("title")
        cal = Calendar()
        return cal.create_event(start, end, title)
    @staticmethod
    def move_event(meta_data, arguments):
        event_id = arguments.get("event_id")
        start = arguments.get("start")
        end = arguments.get("end")
        cal = Calendar()
        return cal.move_event(event_id, start, end)
    @staticmethod
    def delete_event(meta_data, arguments):
        event_id = arguments.get("event_id")
        cal = Calendar()
        return cal.delete_event(event_id)
    @staticmethod
    def edit_event(meta_data, arguments):
        event_id = arguments.get("event_id")
        start = arguments.get("start")
        end = arguments.get("end")
        title = arguments.get("title")
        cal = Calendar()
        return cal.edit_event(event_id, start, end, title)
