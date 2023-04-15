def searchHandler(input_query):
    import SnippetFetcher
    import PageTextAPI
    import QueryGenerator
    input_query = QueryGenerator.generateQueries(input_query)[0]
    snippet = SnippetFetcher.searchSnippet(input_query)
    if snippet:
        print(snippet)
        return snippet
    firstPage = PageTextAPI.searchPageResult(input_query)
    if firstPage:
        print(firstPage[0].text)
        return firstPage[0].text
    return "No results found"


searchHandler("Apple Lineup")