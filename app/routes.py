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

@router.get("/conversations")
async def get_all_conversations():
    """Get all unique wa_ids and their latest messages from MongoDB"""
    try:
        # MongoDB aggregation pipeline to get unique conversations efficiently
        pipeline = [
            # Match documents that have wa_id
            {"$match": {"wa_id": {"$exists": True}}},
            
            # Sort by insertion order (natural order) to get latest messages
            {"$sort": {"_id": 1}},
            
            # Group by wa_id to get unique conversations
            {
                "$group": {
                    "_id": "$wa_id",
                    "latest_doc": {"$last": "$$ROOT"},
                    "message_count": {"$sum": 1},
                    "first_message_time": {"$first": "$timestamp"},
                    "latest_message_time": {"$last": "$timestamp"}
                }
            },
            
            # Sort by latest message time (most recent first)
            {"$sort": {"latest_message_time": -1}}
        ]
        
        conversations = []
        async for result in db.messages.aggregate(pipeline):
            latest_doc = result["latest_doc"]
            
            # Extract message and timestamp from the document
            latest_message = "No message"
            latest_timestamp = ""
            
            # Handle webhook payload format
            if latest_doc.get("messages") and len(latest_doc["messages"]) > 0:
                latest_message = latest_doc["messages"][-1]["message"]
                latest_timestamp = latest_doc["messages"][-1].get("timestamp", "")
            # Handle direct message format
            elif latest_doc.get("message"):
                latest_message = latest_doc["message"]
                latest_timestamp = latest_doc.get("timestamp", "")
                
            conversations.append({
                "wa_id": result["_id"],
                "name": f"Customer {result['_id']}",
                "lastMessage": latest_message,
                "lastMessageTime": latest_timestamp,
                "unreadCount": 0,
                "message_count": result["message_count"]
            })
        
        return conversations
        
    except Exception as e:
        print(f"Error getting conversations: {e}")
        return []