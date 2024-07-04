from .web_search.search import performSearch
from .time.time import get_time
import datetime
from .maps.routes.routes import public_transport_route_fetching_handler
from .maps.places.places import place_search_handler
from .calendar.gcal import CalendarHandler
function_dict = {
    "internet_suche": performSearch,
    "zeit_abrufen": get_time,
    "public_transport_abrufen" : public_transport_route_fetching_handler,
    "search_place_information": place_search_handler,
    "kalender_abrufen": CalendarHandler.fetch_calendar,
    "search": CalendarHandler.search,
    "kalender_ereignis_erstellen": CalendarHandler.create_event,
    "kalender_ereignis_verschieben": CalendarHandler.move_event,
    "kalender_ereignis_loeschen": CalendarHandler.delete_event,
    "kalender_ereignis_bearbeiten": CalendarHandler.edit_event
}

openai_function_documentation = [
    {
        
        "type": "function",
        "function": {
            "name": "internet_suche",
            "description": "Suche bei Google nach einer Antwort auf eine Frage",
            "parameters": {
                "type": "object",
                "properties": {
                    "searchquery": {
                        "type": "string",
                        "description": "Die eindeutige Suchanfrage als ganze Frage (nicht als Stichpunkte) die aus dem Gesprächsverlauf generiert wurde"
                    }
                },
                "required": ["searchquery"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "wetter_abrufen",
            "description": "Rufe das Wetter für einen Ort ab",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Der Ort, für den du das Wetter wissen möchtest"
                    },
                    "time": {
                        "type": "string",
                        "description": "Das ISO-formatierte Datum, für das du das Wetter wissen möchtest. Das aktuelle ISO-Datum ist: " + str(datetime.datetime.now())
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "zeit_abrufen",
            "description": "Rufe die aktuelle Uhrzeit ab, nur wenn du speziell danach fragst",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Der Ort, für den du die Uhrzeit wissen möchtest"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "public_transport_abrufen",
            "description": "Rufe die nächste Zugverbindung von A nach B ab, inklusive der Gehzeit zur Station",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "Der Ort, von dem du starten möchtest. LEER LASSEN, UM DEN AKTUELLEN STANDORT ZU VERWENDEN"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Der Zielort"
                    },
                    "en_departure_time": {
                        "type": "string",
                        "description": "Der Datumausdruck für die Abfahrtszeit. Immer ins Englische übersetzen"
                    },
                    "en_arrival_time": {
                        "type": "string",
                        "description": "Der Datumausdruck für die gewünschte Ankunftszeit. Immer ins Englische übersetzen"
                    }
                },
                "required": ["destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "kalender_abrufen",
            "description": "Rufe alle Ereignisse aus dem Kalender ab. Finde das zum Prompt passende Ereignis und nutze es, um mit den Aufgaben fortzufahren oder stelle weitere Fragen, um die Aufgabe zu klären",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "string",
                        "description": "Die Startzeit des ersten Ereignisses der Liste im ISO-Format. Wenn nicht anders verlangt nicht angeben um alle Ereignisse abzurufen"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "kalender_ereignis_erstellen",
            "description": "Erstellt ein neues Ereignis im Kalender",
            "parameters": {
                "type": "object",
                "properties": {
                    "start": {
                        "type": "string",
                        "description": "Die Startzeit des Ereignisses im ISO-Format"
                    },
                    "end": {
                        "type": "string",
                        "description": "Die Endzeit des Ereignisses im ISO-Format"
                    },
                    "title": {
                        "type": "string",
                        "description": "Der Titel des Ereignisses"
                    }
                },
                "required": ["start", "end"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "kalender_ereignis_verschieben",
            "description": "Verschiebt ein Ereignis im Kalender",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "Die über die 'kalender_abrufen' Funktion erlangte ID des Ereignisses"
                    },
                    "start": {
                        "type": "string",
                        "description": "Die neue Startzeit des Ereignisses im ISO-Format"
                    },
                    "end": {
                        "type": "string",
                        "description": "Die neue Endzeit des Ereignisses im ISO-Format"
                    }
                },
                "required": ["event_id", "start", "end"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "kalender_ereignis_loeschen",
            "description": "Löscht ein Ereignis aus dem Kalender",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "Die über die 'kalender_abrufen' Funktion erlangte ID des Ereignisses"
                    }
                },
                "required": ["event_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "kalender_ereignis_bearbeiten",
            "description": "Bearbeitet ein Ereignis im Kalender",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "Die über die 'kalender_abrufen' Funktion erlangte ID des Ereignisses"
                    },
                    "start": {
                        "type": "string",
                        "description": "Die neue Startzeit des Ereignisses im ISO-Format"
                    },
                    "end": {
                        "type": "string",
                        "description": "Die neue Endzeit des Ereignisses im ISO-Format"
                    },
                    "title": {
                        "type": "string",
                        "description": "Der neue Titel des Ereignisses"
                    }
                },
                "required": ["event_id"]
            }
        }
    
    }
]