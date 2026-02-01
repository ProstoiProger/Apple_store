from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from pymongo.collection import Collection

load_dotenv()


MONGO_URI = os.getenv("MONGODB_URI") or os.getenv("MONGO_URI", "mongodb://localhost:27017")


class MongoDB:
    def __init__(self, uri: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client.apple_store 

    def get_collection(self, collection_name: str) -> Collection:
        return self.db[collection_name]
    

def get_db() -> MongoDB:
    return MongoDB(MONGO_URI)