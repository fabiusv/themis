import requests
from bs4 import BeautifulSoup
import re

def searchSnippet(term, lang="en"):
    #print("snippet fetcher started for term: " + term)
    def formatSnippet(string):
        fixed_string = re.sub(r'([a-z])([A-Z])', r'\1 \2', string)
        fixed_string = fixed_string.replace("Wähle aus, wozu du Feedback geben möchtest Du kannst auch allgemeines Feedback geben Feedback geben", "")
        fixed_string = re.sub(r'(\D)(\d)', r'\1 \2', fixed_string)
        fixed_string = fixed_string.replace("Feedback geben", "")
        fixed_string = fixed_string.replace("Hervorgehobenes Snippet aus dem Web", "")

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

    def formatURL(searchterm, lang="en"):
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

    url = formatURL(term, lang)

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

        if "Feedback geben" in div.text or "Z0LcW t2b5Cf" in this_class:
            class_list = div.get("class")
            if class_list:
                class_levels = len(class_list)
                if class_levels > deepest_class_level:
                    deepest_class_level = class_levels
                    target_class = class_list[-1]

    if target_class:
        target_element = soup.find("div", {"class": target_class})
        target_text = target_element.text.strip()
        #print(target_text)
        target_text = target_text.split("Wird auch oft gesucht")[0]
        target_text = target_text.split("Andere suchten auch nach")[0]
        if target_text == "Feedback geben" or target_text == "Informationen zu hervorgehobenen Snippets•Feedback geben" or "Laut deiner IP-Adresse" in target_text:
            print("Could not find a snippet")
            return None
        #print("unformatted snippet: " + target_text)
        return formatSnippet(target_text)
    else:
        print("Could not find the class that contains 'Hervorgehobenes Snippet aus dem Web'")
        return None


#print(searchSnippet("Super Bowl 2023 winner", lang="en"))

