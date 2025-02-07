from typing import Any
from app.config.config import settings 
from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorDatabase,AsyncIOMotorCollection

class Database:
    def __init__(self):
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_uri)
        self.database: AsyncIOMotorDatabase = self.client.get_database(settings.mongodb_name)  # Specify the database name
        self.user_collection: AsyncIOMotorCollection = self.database.get_collection("users")

    async def init_db(self) :
        await self.user_collection.create_index([("username", 1)], unique=True)
        await self.user_collection.create_index([("email", 1)], unique=True)

        return Any

    def close_db(self) :
        self.client.close()    
