from pydantic import BaseModel 
class PersonFile(BaseModel):
    first_name: str
    last_name: str
    birthdate: int
    personal_interactons: str