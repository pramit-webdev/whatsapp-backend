from fastapi import APIRouter
from app.db import db
from app.models import WebhookPayload, MessageCreate
from app.utils import current_timestamp
from bson import ObjectId

router = APIRouter()

@router.post("/webhook")
async def receive_webhook(payload: WebhookPayload):
    # Save the full webhook
    data = payload.dict()
    result = await db.messages.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return {"status": "received", "data": data}

@router.get("/messages/{wa_id}")
async def get_messages(wa_id: str):
    messages_cursor = db.messages.find({"wa_id": wa_id})
    messages = []
    async for msg in messages_cursor:
        msg["_id"] = str(msg["_id"])  # Convert ObjectId to string
        messages.append(msg)
    return messages

@router.post("/messages/send")
async def send_message(payload: MessageCreate):
    message_doc = {
        "wa_id": payload.wa_id,
        "message": payload.message,
        "sender": payload.sender,
        "timestamp": current_timestamp(),
    }
    result = await db.messages.insert_one(message_doc)
    message_doc["_id"] = str(result.inserted_id)
    return {"status": "sent", "data": message_doc}
