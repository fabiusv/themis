from .fetchers import PageTextAPI, SnippetFetcher
from .helpers import QueryGenerator, web_formatter
from tools import summary


def searchHandler(chatHistory, lang="en"):
    input_query = QueryGenerator.generateQueries(chatHistory, lang)
    print("result")
    print(input_query)
    if input_query == None:
        return None
    input_query = input_query[0]
    
    #input_query = chatHistory.messages[-1].content

    snippet = SnippetFetcher.searchSnippet(input_query, lang)

    if snippet:
        return web_formatter.format_snippet(snippet, input_query, lang)
    else:
        pages = PageTextAPI.fetch_google_results(input_query, lang)
        #print(pages)
        
        for page in pages[0:3]:
            return web_formatter.format_website(summary.summarize_website(page.url, lang), input_query, lang)
            print(page.title)
            print(pages.url)
            print("\n")
        
        

        #return firstPage[0].text
    #return None


#print(searchHandler("Wie lange existierte die mainzer republik?"))