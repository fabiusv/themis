from pydantic import BaseModel

class CompletionResponse(BaseModel):
    completion: str
    context_id: str
