import os
import sys
from .fetchers import PageTextAPI, SnippetFetcher
from .helpers import QueryGenerator


def searchHandler(input_query, lang="en"):
    
    input_query = QueryGenerator.generateQueries(input_query, lang)[0]
    snippet = SnippetFetcher.searchSnippet(input_query, lang)
    if snippet:
        pass
        #print(snippet)
        #return snippet
    firstPage = PageTextAPI.searchPageResult(input_quer, lang)
    if firstPage:
        print(firstPage[0].text)
        return firstPage[0].text
    return None


#print(searchHandler("Wie lange existierte die mainzer republik?"))
