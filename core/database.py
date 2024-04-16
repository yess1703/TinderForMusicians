import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from core.settings import settings

mongo_client = AsyncIOMotorClient(settings.bots.database)
mongo_client.get_io_loop = asyncio.get_running_loop
users_collection = mongo_client["TinderForMusicians"]["users"]
partner_collection = mongo_client["TinderForMusicians"]["partner"]

