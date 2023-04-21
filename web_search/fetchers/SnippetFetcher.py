import requests
from bs4 import BeautifulSoup

def searchSnippet(term, lang="en"):
    

    def formatURL(searchterm, lang="en"):
        inquiry = ""
        #eventuell auch einfach ganze frage als query nehmen  https://www.google.com/search?q=1%2B1
        
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
        elif lang == "de":
            url = "https://www.google.de/search?q=" + url
        else:
            raise ValueError("Language not supported")

        return url

    # Define the headers for the request
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

    # Send a request to the website with the specified headers
    url = formatURL(term)

    response = requests.get(url, headers=headers)

    # Parse the HTML content with BeautifulSoup
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
        target_text = target_text.split("Wird auch oft gesucht")[0]
        if target_text == "Feedback geben":
            return None
        return target_text
    #    print(f"The text of the element with class '{target_class}': '{target_text}'")
    else:
        print("Could not find the class that contains 'Hervorgehobenes Snippet aus dem Web'")
        return None
#
#print(searchSnippet("What is Apples current phone lineup?"))