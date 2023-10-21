from pydantic import BaseModel 

class PersonFileRequest(BaseModel):
    first_name: str
    last_name: str
    birthdate: int
    personal_interactions: str