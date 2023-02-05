from fastapi import FastAPI, Request, Form, Response, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import hashlib
import json
from pymongo import MongoClient
import gridfs
client = MongoClient(
        "mongodb+srv://pooyaarab:zJMzoHr1fMhOnnHk@cluster0.vwrrya4.mongodb.net/?retryWrites=true&w=majority")
db = client.test
fs = gridfs.GridFS(db)
items = db.items
item = items.find_one({"title": "first time"})
title = item["title"]
description = item["description"]
image_id = item["image"]
print(title)
print(description)
print(image_id)