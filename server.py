from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import datetime

import uuid

from DatabaseHandlers.ContextDBHandler import ContextDatabaseManager
from DatabaseHandlers.UserDBHandler import UserDatabaseManager

import themis

app = FastAPI()
handler = themis.ThemisHandler()

def validate(user_id: str, api_key):
    print(user_id)
    user_manager = UserDatabaseManager()
    user = user_manager.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User ID not found")
    if user.api_key != api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return True

class RegistrationResponse(BaseModel):
    user_id: str
    api_key: str


class ChatResponseRequest(BaseModel):

    user_id: str
    context_id: str | None = None

    message: str

    location: themis.Location | None = None
    timezone: str | None = None
    language: str | None = None


class FunctionCalling(BaseModel):
    function_name: str
    parameters: str

class CompletionResponse(BaseModel):
    completion: str
    context_id: str

    

class RegisterRequest(BaseModel):
    username: str
    password_hash: str
    email: str
    


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/complete_chat/user/{user_id}/key/{api_key}")
async def complete(user_id:str, api_key: str, chatResponse: ChatResponseRequest):
    if validate(user_id, api_key):
        context_manager = ContextDatabaseManager()
        

        if chatResponse.context_id is None:
            context_id = str(uuid.uuid4())
            context = themis.Context(user_id=user_id, context_id=context_id, creation=datetime.datetime.now(), last_modification=datetime.datetime.now(), conversation=themis.Conversation(messages=[]), meta_data=themis.MetaData(location=themis.Location(lat=chatResponse.location.lat, lng=chatResponse.location.lng), timezone=chatResponse.timezone, language=chatResponse.language))
            context.conversation.messages.append(themis.ChatMessage(role="user", content=chatResponse.message))
            
            
            #douplicated code to reduce database operations in order to decrease latency
            response = handler.completion(context)

            context.last_modification = datetime.datetime.now()
            
            context_manager.insert(context)
            #check if old context fits
        else:
            context_id = chatResponse.context_id
            context = context_manager.find_by_id(chatResponse.context_id)
            
            #print(context)

            if context is None:
                raise HTTPException(status_code=404, detail="Context ID not found")
            context = themis.Context.decode(context)
            context.conversation.messages.append(themis.ChatMessage(role="user", content=chatResponse.message))
            if context.user_id != user_id:
                raise HTTPException(status_code=401, detail="Invalid User ID")

            
            
            #call Themis Handler with context
            response = handler.completion(context)
            context.conversation.messages = response

            context.last_modification = datetime.datetime.now()
            
            context_manager.edit(context)

        return context
            


@app.get("/function_calling/user/{user_id}/key/{api_key}")
async def function_calling(user_id: str, api_key: str, function_calling_object: FunctionCalling):
    if validate(user_id, api_key):
        #call function
        return {"success": True}





@app.post("/register")
async def register(user: RegisterRequest):

    user_manager = UserDatabaseManager()
    if user_manager.find_by_email(user.email) is not None:
        raise HTTPException(status_code=409, detail="Email already in use")
    if user_manager.find_by_username(user.username) is not None:
        raise HTTPException(status_code=409, detail="Username already taken")
    

    temp_user = themis.User(user_id=str(uuid.uuid4()), username=user.username, api_key=str(uuid.uuid4()), email=user.email, password_hash=user.password_hash)

    user_manager.insert(temp_user)

    return RegistrationResponse(user_id=temp_user.user_id, api_key=temp_user.api_key)



@app.post("/get_api_key")
async def get_api_key(user: RegisterRequest):
    #return api key if correct
    if validate(user.username, user.password_hash):
        user_manager = UserDatabaseManager()
        temp_user = user_manager.find_by_username(user.username)
        return {"api_key": temp_user.api_key} # type: ignore
    else:
        raise HTTPException(status_code=401, detail="Invalid Credentials")