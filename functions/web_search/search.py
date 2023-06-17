from .fetchers import PageTextAPI, SnippetFetcher
from .helpers import web_formatter
from tools import summary
import requests
from tools import summary
#TODO: Implement yielding of results

def performSearch(arguments, lang="en"):
    input_query = arguments["searchquery"]
    print(input_query)
    snippet = SnippetFetcher.searchSnippet(input_query, lang)

    if snippet:
        return "Real-time websearch response:\n" + snippet
    else:
        print("Fetching pages")
        pages = PageTextAPI.fetch_google_results(input_query, lang)#FIXME: Page Fetcher is not working
        print(pages[0])
        
        for page in pages[0:3]:
            #print(summary.summarize_website(page.url, lang))
            return summary.summarize_website(page.url, lang)
            #quit()
            #return web_formatter.format_website(, input_query, lang)
            
            
            #return summary.summarize_website(page.url, lang)
            