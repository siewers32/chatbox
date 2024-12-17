from pydantic import BaseModel

class ChatInput(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str