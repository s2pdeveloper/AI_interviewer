from pymongo import MongoClient
import threading

class MongoDBClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        self.client = MongoClient("mongodb+srv://poojadabi:pooja123@cluster0.7jt1dvk.mongodb.net")
        self.db = self.client["AI_Interview"]

    def get_database(self):
        return self.db

# Usage
mongo_client = MongoDBClient()
