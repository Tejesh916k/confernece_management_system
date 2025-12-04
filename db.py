import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongodb_uri = os.getenv('MONGODB_URI')
database_name = os.getenv('DATABASE_NAME', 'conference_db')

client = MongoClient(mongodb_uri)
db = client[database_name]  # Use explicit database name
