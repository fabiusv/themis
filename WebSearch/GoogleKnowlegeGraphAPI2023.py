
def searchKnowlegeGraph(
    search_query,
    project_id = "llm-assistant-1679252411498",
    location = "global",
    languages = None,
    types = None,
    limit: int = 20,
):

    class Result:
        def __init__(self, result):
            self.name = result.get('name')
            self.description = result.get('description')
            self.types = result.get('@type')
            
            detailed_description = result.get("detailedDescription")
            if detailed_description:
                self.article_body = detailed_description.get('articleBody')
                self.url = detailed_description.get('url')
                self.license = detailed_description.get('license')
            else:
                self.article_body = None
                self.url = None
                self.license = None
                
            self.cloud_mid = result.get('@id')
            self.identifiers = result.get("identifier")

    from typing import Sequence

    from google.cloud import enterpriseknowledgegraph as ekg
    # Create a client
    client = ekg.EnterpriseKnowledgeGraphServiceClient()
    
    # The full resource name of the location
    # e.g. projects/{project_id}/locations/{location}
    parent = client.common_location_path(project=project_id, location=location)
    
    # Initialize request argument(s)
    request = ekg.SearchRequest(
        parent=parent,
        query=search_query,
        languages=languages,
        types=types,
        limit=limit,
    )
    
    # Make the request
    response = client.search(request=request)
        
    # Extract and print date from response
    return [Result(item.get("result")) for item in response.item_list_element]
        
        

results = searchKnowlegeGraph("Apple")
