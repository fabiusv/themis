import requests
from bs4 import BeautifulSoup
import re
import json
import os
from ....localization.localizer import get_localization

#print current path


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
    #with open("test.html", "w") as file:
    #   file.write(str(soup))

    # Find the deepest class that contains the text "Hervorgehobenes Snippet aus dem Web"
    target_class = None
    deepest_class_level = 0
    for div in soup.find_all("div"):
        this_class = []
        if div.get("class"):
            this_class = div.get("class")

        if localization["functions"]["search"]["snippet_target_identifiers"]["snippet_locator_string"] in div.text or "Z0LcW t2b5Cf" in this_class:
            class_list = div.get("class")
            if class_list:
                class_levels = len(class_list)
                if class_levels > deepest_class_level:
                    deepest_class_level = class_levels
                    target_class = class_list[-1]

    if target_class:
        target_element = soup.find("div", {"class": target_class})
        target_text = target_element.text.strip() # type: ignore
        #print(target_text)
        target_text = target_text.split(localization["functions"]["search"]["snippet_target_identifiers"]["start"])[0]
        target_text = target_text.split(localization["functions"]["search"]["snippet_target_identifiers"]["stop"])[0]
        if target_text in localization["functions"]["search"]["snippet_target_identifiers"]["not_found_strings"] or localization["functions"]["search"]["snippet_target_identifiers"]["ip_message"] in target_text:
            return None
        #print("unformatted snippet: " + target_text)
        return formatSnippet(meta_data, target_text)
    else:
        return None


#print(searchSnippet("Super Bowl 2023 winner", lang="en"))

