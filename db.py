from pymongo import MongoClient
from config import MONGO_URL, DATABASE_NAME
from bson import ObjectId

client = MongoClient(MONGO_URL)
db = client[DATABASE_NAME]
collection = db["todos"]

