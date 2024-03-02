
from ...functions import summary
import requests
from ...functions import summary
import requests
from bs4 import BeautifulSoup
import json
from .fetchers import PageTextAPI, SnippetFetcher
from .helpers import web_formatter
from ...localization.localizer import get_localization

#Replace with Langchain Google Tool if it ever breaks
def get_website_text(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()


def performSearch(meta_data, arguments, is_routine=False):
    #TODO: Do all of this concurrently in order to reduce latency

    localization = get_localization(meta_data.language)
    
    input_query = arguments["searchquery"]
    print(input_query)

    if not is_routine:
        serpapi = None
        #serpapi = SnippetFetcher.search_serapi(meta_data, input_query)
        print("SERPAPI:")
        print(serpapi)

        if serpapi:
            return localization["functions"]["search"]["snippet_instruction"] + serpapi

    snippet = SnippetFetcher.searchSnippet(meta_data, input_query)


    if snippet:
        
        snippet = localization["functions"]["search"]["snippet_instruction"] + snippet
        pages = PageTextAPI.fetch_google_results(meta_data, input_query) #FIXME: fetch hole website rather than the snippet onl
        page_0_request = requests.get(pages[0].url)

        soup = BeautifulSoup(page_0_request.text, 'html.parser')

            # Extract text content
        text_content = soup.get_text()

            # Print the text content

        cleaned_text = '\n'.join(line.strip() for line in text_content.splitlines() if line.strip())
        
        try:
            cleaned_text = cleaned_text[2000:-4000]
        except:
            pass
        print(cleaned_text)

        return snippet + "\n" + pages[0].title+  ": " + pages[0].text

    else: 
        pages = PageTextAPI.fetch_google_results(meta_data, input_query) 
        return pages[0].title+ ": " + pages[0].text
    return ""
    
def search_pages_only():

    pages = PageTextAPI.fetch_google_results(meta_data, input_query) #FIXME: Page Fetcher is not working
    print(pages[0])
    
    for page in pages[0:3]:
        return get_website_text(page.url)
        #print(summary.summarize_website(page.url, lang))
        return summary.summarize_website(page.url, lang)
        #quit()
        #return web_formatter.format_website(, input_query, lang)
        
        #return summary.summarize_website(page.url, lang)