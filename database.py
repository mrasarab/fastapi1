import gridfs
from pymongo import MongoClient
import json
client = MongoClient(
    "mongodb+srv://pooyaarab:zJMzoHr1fMhOnnHk@cluster0.vwrrya4.mongodb.net/?retryWrites=true&w=majority")
db = client.test
fs = gridfs.GridFS(db)
                

