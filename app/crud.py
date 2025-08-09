from app.db import messages_collection
from bson import ObjectId

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

async def save_webhook_message(payload: dict):
    wa_id = payload.get("wa_id", "unknown")
    messages = payload.get("messages", [])

    doc = {
        "wa_id": wa_id,
        "messages": messages
    }
    return await messages_collection.insert_one(doc)

async def get_all_messages():
    cursor = messages_collection.find({})
    return [serialize_doc(doc) async for doc in cursor]
