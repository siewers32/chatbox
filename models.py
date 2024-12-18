from pydantic import BaseModel, Field

class ChatInput(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class ResponseModel(BaseModel):
    """Structured response with metadata."""

    response: str
    needs_escalation: bool
    follow_up_required: bool
    sentiment: str = Field(description="Customer sentiment analysis")
