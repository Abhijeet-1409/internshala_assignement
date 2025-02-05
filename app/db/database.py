from app.config.config import settings 
from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorDatabase,AsyncIOMotorCollection

class Database:
    def __init__(self):
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_uri)
        self.database: AsyncIOMotorDatabase = self.client.get_database(settings.mongodb_name)  # Specify the database name
        self.user_collection: AsyncIOMotorCollection = self.database.get_collection("users")

    async def init_db(self):
        """Initialize the database and create indexes."""
        await self.user_collection.create_index("username", unique=True)
        await self.user_collection.create_index("email", unique=True)

    async def close(self):
        """Close the MongoDB client."""
        await self.client.close()

# Create a global instance of the Database class
db = Database()