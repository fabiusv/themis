
from ...functions import summary
import requests
from ...functions import summary
import requests
from bs4 import BeautifulSoup
import json
from .fetchers import PageTextAPI, SnippetFetcher
from .helpers import web_formatter
from ...localization.localizer import get_localization

def get_website_text(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()


def performSearch(meta_data, arguments):

    localization = get_localization(meta_data.language)
    
    input_query = arguments["searchquery"]
    print(input_query)
    snippet = SnippetFetcher.searchSnippet(meta_data, input_query)

    if snippet:
        
        return localization["functions"]["search"]["snippet_instruction"] + snippet
    else:
        print("Fetching pages")
        pages = PageTextAPI.fetch_google_results(meta_data, input_query) #FIXME: Page Fetcher is not working
        print(pages[0])
        
        for page in pages[0:3]:
            return get_website_text(page.url)
            #print(summary.summarize_website(page.url, lang))
            return summary.summarize_website(page.url, lang)
            #quit()
            #return web_formatter.format_website(, input_query, lang)
            
            #return summary.summarize_website(page.url, lang)