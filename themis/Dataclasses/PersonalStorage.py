import pydantic
from .PersonFile import PersonFile

class PersonalStorage(pydantic.BaseModel):
    personal_interactons: list[PersonFile] = []

    def encode(self):
        return {"persons": [i.encode() for i in self.personal_interactons]}
    @staticmethod
    def decode(personal_storage_dict):
        return PersonalStorage(personal_interactons=[PersonFile.decode(i) for i in personal_storage_dict["persons"]])