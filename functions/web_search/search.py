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
        pages = PageTextAPI.fetch_google_results(input_query, lang)#FIXME: Page Fetcher is not working
        #print(pages)
        for page in pages[0:3]:
            return web_formatter.format_website(summary.summarize_website(page.url, lang), input_query, lang)
            
            
            #return summary.summarize_website(page.url, lang)
            