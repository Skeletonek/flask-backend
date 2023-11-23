from pymongo import MongoClient

conn = MongoClient("mongodb://127.0.0.1/27017")
db = conn["rainbow"]