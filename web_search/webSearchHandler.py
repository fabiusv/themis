from .fetchers import PageTextAPI, SnippetFetcher
from .helpers import QueryGenerator, web_formatter
from tools import summary


def searchHandler(input_query, lang="en"):
    
    input_query = QueryGenerator.generateQueries("User: " + input_query, lang)
    if input_query == None:
        return None
    input_query = input_query[0]
    snippet = SnippetFetcher.searchSnippet(input_query, lang)
    

    if snippet:
        return web_formatter.format_snippet(snippet, input_query, lang)
    else:
        pages = PageTextAPI.fetch_google_results(input_query, lang)
        
        for page in pages[0:3]:
            return web_formatter.format_website(summary.summarize_website(page.url, lang), input_query, lang)
    
        #return firstPage[0].text
    #return None


#print(searchHandler("Wie lange existierte die mainzer republik?"))