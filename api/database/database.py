from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MyMongoDB:
    def __init__(self):
        self.mongodb_uri = os.environ.get('MONGODB_DATABASE_URL')
        self.database_name = os.environ.get('DATABASE_NAME')

        if not self.database_name:
            raise ValueError("MongoDB URI沒有設置成功")

        try:
            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client[self.database_name]
        except Exception as e:
            raise ConnectionError(f"無法連接到 MongoDB: {str(e)}")

    def connect_to_collection(self, collection_name):
        return self.db[collection_name]