
def format_meta_data(metadata):
    from ..localization.localizer import local_strings
    return local_strings["grounding"]["meta_data"]["location"] + metadata.location.encode() + "\n" + local_strings["grounding"]["meta_data"]["timezone"] + metadata.timezone + "\n" + local_strings["grounding"]["meta_data"]["language"] + metadata.language + "\n"

def get_person_storage(query):
    persons = []#load from user account in db
    mentioned_persons = []
    for person in persons:
        if person.first_name in query:
            mentione_persons.append(person)

    result = "This is what you know about" + mentioned_persons[0].first_name + ":\n"
    for i in mentioned_persons:
        result += i.first_name + "\n" + i.personal_interactons + "\n"

    return result