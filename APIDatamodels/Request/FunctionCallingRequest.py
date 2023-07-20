from pydantic import BaseModel

class FunctionCallingRequest(BaseModel):
    function_name: str
    parameters: str