from pydantic import BaseModel
class RegistrationResponse(BaseModel):
    user_id: str
    api_key: str
