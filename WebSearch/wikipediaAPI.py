

# Create a Wikipedia API object


# Define a function to retrieve a summary of a search term
def searchWikiSummary(search_term):

    import wikipediaapi

    wiki = wikipediaapi.Wikipedia('en')
    # Use the Wikipedia API to retrieve the page corresponding to the search term
    page = wiki.page(search_term)

    # Check if the page exists
    if page.exists():
        # Return the summary of the page
        print(page.text)
        return page.summary
        
    else:
        # If the page does not exist, return an error message
        return f"Sorry, '{search_term}' could not be found on Wikipedia."


#summary = get_summary(search_term)
