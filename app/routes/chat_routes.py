from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.controllers.chat_controller import process_chat_message

router = APIRouter()

class MessageDict(BaseModel):
    role: str
    content: str

class ChatContext(BaseModel):
    messages: List[MessageDict]

@router.post("/chat")
def chat_endpoint(data: ChatContext):
    return process_chat_message(data.messages)
