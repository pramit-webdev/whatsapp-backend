from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise Exception("MONGODB_URI not set in .env")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[os.getenv("DB_NAME", "whatsapp")]
