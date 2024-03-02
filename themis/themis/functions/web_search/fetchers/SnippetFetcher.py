import requests
from bs4 import BeautifulSoup
import re
import json
import os

import pydantic # type: ignore

class MetaData(pydantic.BaseModel):
  timezone: str
  language: str

from ....localization.localizer import get_localization

#print current path
localization = {
      "language_identifiers": {
          "short":"en",
          "full":"en-US"
      },
      "common_words":{
          "and":"and",
          "is": "is"
      },
      "default_conversation": "The current date is: 15. June. The year is 2023. Perform a web-search on time sensitive topics that could have changed or you just dont know. Always perform a search, before claiming you dont know the answer",
      "grounding": {
            "meta_data": {
                "location": "You are located in: ",
                "timezone": "Your timezone is: ",
                "language": "Your language is: "
            },
      },
      
      "functions": {

          "maps": {
              "sections": {
                  "section_instruction": "It consists of these section(s): ",
                  "departure":"Departure at: ",
                  "duration": "Duration: ",
                  "minutes": "Minuten"
              },
              "route": {
                  "total_duration": "Total time "
                  
              },
              "format_order": "Format this information in a flowing text that can be read out by a virtual assistant:"
          },

          "search":{
              "snippet_instruction": "Real-time websearch response:\n",
              "snippet_formatting": {
                  "stripped_strings": ["Wähle aus, wozu du Feedback geben möchtest Du kannst auch allgemeines Feedback geben Feedback geben", "Feedback geben", "Hervorgehobenes Snippet aus dem Web"] 
              },
              "snippet_target_identifiers": {
                  "snippet_locator_string": "Feedback geben",
                  "start": "Wird auch oft gesucht",
                  "stop": "Andere suchten auch nach",
                  "ip_message": "Laut deiner IP-Adresse",
                  "not_found_strings": ["Feedback geben", "Informationen zu hervorgehobenen Snippets•Feedback geben" ]
              }
          }
      }

}

def formatSnippet(meta_data, string):
        
        localization = get_localization(meta_data.language)
        
        
        fixed_string = re.sub(r'([a-z])([A-Z])', r'\1 \2', string)
        fixed_string = re.sub(r'(\D)(\d)', r'\1 \2', fixed_string)

        #Get strings that dont add any value and remove them
        for stripping_instruction in localization["functions"]["search"]["snippet_formatting"]["stripped_strings"]:
            fixed_string = fixed_string.replace(stripping_instruction, "")

        try:
            fixed_string = fixed_string.split("https")[0]
        except:
            pass
        try:

            fixed_string = fixed_string.split("Andere suchten")[0]
        except:
            pass

        try:
            #fixed_string = fixed_string.replace(".", ".\n")
            pass
        except:
            pass
        #print("formatted snippet: " + fixed_string)
        return fixed_string

def formatURL(meta_data, searchterm):
        
        localization = get_localization(meta_data.language)

        lang = localization["language_identifiers"]["short"]

        inquiry = ""
        
        if inquiry == "":
            query = searchterm
        else:
            query = searchterm + "" + inquiry
            
        query = query.replace('ä', '%C3%A4')#ä in unicode
        query = query.replace('ö', '%D%B6')#ö in unicode
        query = query.replace('ü', '%C3%BC')#ü in unicode
        url = query.split(" ")
        
        #url = [url.replace('+', '%2B') for i in url] # alle anderen rechenzeichhen wie *, / usw erstzung wie hier machen
        
        url = '+'.join(url)
        if lang == "en":
            url = "https://www.google.com/search?q=" + url
            #print("Englisch")
        elif lang == "de":
            url = "https://www.google.de/search?q=" + url
        else:
            raise ValueError("Language not supported")

        return url

def searchSnippet(meta_data, term):

    localization = get_localization(meta_data.language)


    lang = localization["language_identifiers"]["short"]



    if lang == "en":
        accept_lang = "en-US,en;q=0.5"
    elif lang == "de":
        accept_lang = "de-DE,de;q=0.5"
    else:
        raise ValueError("Language not supported")
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
        "Accept-Language": accept_lang,
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
        "TE": "Trailers",
    }

    url = formatURL(meta_data, term)

    response = requests.get(url, headers=headers)


    soup = BeautifulSoup(response.content, "html.parser")
    
    #save html file
    with open("test.html", "w") as file:
       file.write(str(soup))

    # Find the deepest class that contains the text "Hervorgehobenes Snippet aus dem Web"
    target_class = None

    result_list= []
    for div in soup.find_all("div"):
        if div.get("class"):
            #get lowest class level
            while div.find("div"):
                div = div.find("div")

            if div.text != "" and not len(div.text)>1000:
                result_list.append(div.text.strip())
            #remove duplicates
            result_list = list(dict.fromkeys(result_list))
    
    #print(result_list)
    try:
        start_index = result_list.index("News")+3
    except:
        return None

    backup_stop_index = 8

    try:
        stop_index = result_list.index("Wird auch oft gesucht") 
    except:
        try:
            stop_index = result_list.index("Andere suchten auch nach")
        except:
            stop_index = start_index + backup_stop_index

    if stop_index < backup_stop_index:
        stop_index = start_index + backup_stop_index
    

    return "\n".join(result_list[start_index:stop_index])

#print(searchSnippet( MetaData(timezone="utc", language="en"), "What age is the queen of england"))



        

