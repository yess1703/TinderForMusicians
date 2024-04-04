import asyncio

import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from core.settings import settings

# cluster = motor.motor_asyncio.AsyncIOMotorClient(settings.bots.database)
# collection = cluster.TinderForMusicians.TinderForMusicians

mongo_client = AsyncIOMotorClient(settings.bots.database)
mongo_client.get_io_loop = asyncio.get_running_loop
client = mongo_client["TinderForMusicians"]["users"]
