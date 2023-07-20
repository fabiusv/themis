from pydantic import BaseModel
from themis.Dataclasses import Location

class ChatResponseRequest(BaseModel):

    user_id: str
    context_id: str | None = None

    message: str

    location: Location | None = None
    timezone: str | None = None
    language: str | None = None




    