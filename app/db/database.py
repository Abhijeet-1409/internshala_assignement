from app.config.config import settings 
from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorDatabase,AsyncIOMotorCollection


client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_uri)
database: AsyncIOMotorDatabase = client.get_database()

user_collection: AsyncIOMotorCollection = database.get_collection("users")

# Create unique indexes on username and email
async def init_db() :
    await user_collection.create_index("username",unique=True)
    await user_collection.create_index("email",unique=True)