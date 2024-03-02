from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    password_hash: str
    email: str