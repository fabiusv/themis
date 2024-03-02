from pydantic import BaseModel 

class PersonFile(BaseModel):
    first_name: str
    last_name: str
    birthdate: int
    personal_interactions: str

    def encode(self):
        return {"first_name": self.first_name, "last_name": self.last_name, "birthdate": self.birthdate, "personal_interactons": self.personal_interactions}
    @staticmethod
    def decode(person_dict):
        return PersonFile(first_name=person_dict["first_name"], last_name=person_dict["last_name"], birthdate=person_dict["birthdate"], personal_interactions=person_dict["personal_interactons"])