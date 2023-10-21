import pydantic
from .PersonFile import PersonFile

class PersonalStorage(pydantic.BaseModel):
    personal_interactons: list[PersonFile] = []

    def encode(self):
        return {"persons": [i.encode() for i in self.persons]}
    @staticmethod
    def decode(personal_storage_dict):
        return PersonalStorage(persons=[PersonFile.decode(i) for i in personal_storage_dict["persons"]])