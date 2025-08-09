from pydantic import BaseModel, Field
from typing import Dict, Any, List


class Message(BaseModel):
    message: str
    sender: str
    timestamp: str


class WebhookPayload(BaseModel):
    payload_type: str
    id: str = Field(..., alias="_id")  # MongoDB ObjectId alias
    metaData: Dict[str, Any]
    wa_id: str
    messages: List[Message]  # <--- corrected this to be a list


class MessageCreate(BaseModel):
    wa_id: str
    message: str
    sender: str
