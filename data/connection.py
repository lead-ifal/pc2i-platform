import os
from pymongo import MongoClient
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
database = client[str(os.getenv("DATABASE"))]