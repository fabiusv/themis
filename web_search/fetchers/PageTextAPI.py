import requests
from bs4 import BeautifulSoup
import os

def searchPageResult(query, lang="en"):

    class Response():

        def __init__(self, title, snippet, link):
            self.title = title
            self.snippet = snippet
            self.link = link
            self.text = self.fetchWebsiteText(link)
        def fetchWebsiteText(self, url):
            
            response = requests.get(url)
            
            # Parse the HTML content of the response using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove header and footer tags or class names from the parsed HTML content
            header = soup.find('header')
            if header:
                header.extract()
                
            footer = soup.find('footer')
            if footer:
                footer.extract()
                
            header_class = soup.find(class_='header-class')
            if header_class:
                header_class.extract()
                
            footer_class = soup.find(class_='footer-class')
            if footer_class:
                footer_class.extract()
            # Extract the plain text from the HTML content
            plain_text = soup.get_text()
            
            # Print the plain text
            return plain_text.replace("\n", "") #TODO Remove this


    # define the endpoint URL
    url = "https://www.googleapis.com/customsearch/v1"


    # define the parameters to be passed to the endpoint

    #load api key from openai.key file
    if lang == "en":
        cx = "c4415157c33794318"
    elif lang == "de":
        cx = "6597a0405f56c4d3e"
    else:
        raise ValueError("Language not supported")


    with open("google_cloud.key", "r") as f:
       key = f.read()
    
    params = {
        "key": key,
        "cx": cx,
        "q": query,
    }

    # make the request and print the response

    response = requests.get(url, params=params)
    print(response.json()["items"][0]["link"])
    quit()
    #print(response.json()['items'][0:1])
    return [Response(item['title'], item['snippet'], item['link']) for item in response.json()['items'][0:1]] #set amount of fetched websites based on length / token estimation

#print(searchPageResult("What is Apples current phone lineup?")[0].text)