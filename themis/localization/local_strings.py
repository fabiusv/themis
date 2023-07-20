local_strings = { 
    "en":  {
      "language_identifiers": {
          "short":"en",
          "full":"en-US"
      },
      "common_words":{
          "and":"and",
          "is": "is"
      },
      "default_conversation": "The current date is: 15. June. The year is 2023. Perform a web-search on time sensitive topics that could have changed or you just dont know. Always perform a search, before claiming you dont know the answer",
      "functions": {

          "maps": {
              "sections": {
                  "section_instruction": "It consists of these section(s): ",
                  "departure":"Departure at: ",
                  "duration": "Duration: ",
                  "minutes": "Minuten"
              },
              "route": {
                  "total_duration": "Total time "
                  
              },
              "format_order": "Format this information in a flowing text that can be read out by a virtual assistant:"
          },

          "search":{
              "snippet_instruction": "Real-time websearch response:\n",
              "snippet_formatting": {
                  "stripped_strings": ["Wähle aus, wozu du Feedback geben möchtest Du kannst auch allgemeines Feedback geben Feedback geben", "Feedback geben", "Hervorgehobenes Snippet aus dem Web"] 
              },
              "snippet_target_identifiers": {
                  "snippet_locator_string": "Feedback geben",
                  "start": "Wird auch oft gesucht",
                  "stop": "Andere suchten auch nach",
                  "ip_message": "Laut deiner IP-Adresse",
                  "not_found_strings": ["Feedback geben", "Informationen zu hervorgehobenen Snippets•Feedback geben" ]
              }
          }
      }

}
}