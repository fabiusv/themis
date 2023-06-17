import wikipediaapi
#from tools import summary
# Create a Wikipedia API object


# Define a function to retrieve a summary of a search term
def searchWikiSummary(search_term, lang="en"):

    

    wiki = wikipediaapi.Wikipedia(lang)
    # Use the Wikipedia API to retrieve the page corresponding to the search term
    page = wiki.page(search_term)

    # Check if the page exists
    if page.exists():
        # Return the summary of the page
        #result = summarize_text(page.text, lang)

        return page.summary 
        #return page.summary
        
    else:
        # If the page does not exist, return an error message
        return f"Sorry, '{search_term}' could not be found on Wikipedia."
        

#summary = get_summary(search_term)
#
#print(searchWikiSummary("Elon Musk"))