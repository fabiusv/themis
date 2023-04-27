def format_snippet(snippet, orignial_query, lang="en"):
    insert = ""
    insert += f"\nUp to date Snippet:\n"
    insert += snippet
    if lang == "en":     
        insert += f"\nAnswer the following question, if needed use the above text to respond: '{orignial_query}' -- if the question cannot be answered using the text, answer in your own words. Its up to you to decide if you rely on it.\n"
    elif lang == "de":
        insert += f"\nBeantworte die folgende Frage, wenn nötig nehme den Text oben zum antworten: '{orignial_query}' -- wenn die Frage nicht mit dem Text beantwortet werden kann, beantworte sie in deinen eigenen Worten. \n"
    return insert
def format_website(summary, orignial_query, lang="en"):
    insert = ""
    insert += f"\nUp to date Inserted web result:\n "
    insert += summary
    if lang == "en":     
        insert += f"\nAnswer the following question, if needed use the above text to respond: '{orignial_query}' -- if the question cannot be answered using the text, answer yourself. Its up to you to decide if you rely on it.\n"
    elif lang == "de":
        insert += f"\nBeantworte die folgende Frage, wenn nötig nehme den Text oben zum antworten: '{orignial_query}' -- wenn die Frage nicht mit dem Text beantwortet werden kann, beantworte sie in deinen eigenen Worten. \n"
    return insert