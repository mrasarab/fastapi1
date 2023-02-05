from fastapi import FastAPI, Request, Form, Response, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import hashlib
import base64
import json

from pymongo import MongoClient
import gridfs
# mysql part
import mysql.connector
db = mysql.connector.connect(
    host="localhost")
mycusor = db.cursor()
####
# fastapi part html get and post response
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


##########
@app.get("/")
def root(request: Request):
    client = MongoClient(host="localhost"")
    db = client.test
    fs = gridfs.GridFS(db)
    items = db.items
    item = items.find_one({"title": "first time"})
    title = item["title"]
    description = item["description"]
    image_id = item["image"]
    image = fs.get(image_id)
    image_string = base64.b64encode(image.read()).decode("utf-8")
    return templates.TemplateResponse("home.html", {"request": request, "title": title, "description": description, "image": image_string})

# registration


@app.get("/registration")
def registration(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


# @app.get("/registration/", response_class=HTMLResponse)
# def get_registration_form(request: Request):
 #   return templates.TemplateResponse("registration.html", {"request": request})

@app.post("/registration", response_class=HTMLResponse)
def post_registration_form(request: Request, email: str = Form(...), pswd: str = Form(...), repswd: str = Form(...)):
    if pswd == repswd:
        user1 = email
        pass1 = hashlib.sha1(pswd.encode()).hexdigest()
        mycusor.execute("USE userinfos;")
        mycusor.execute(
            "SELECT COUNT(*) FROM user WHERE username=%s", (user1,))
        for user in mycusor:
            if user[0] == 0:
                mycusor.execute("USE userinfos;")
                mycusor.execute(
                    "INSERT INTO user (username, password) VALUES (%s, %s)", (user1, pass1))
                db.commit()
                return templates.TemplateResponse("home.html", {"request": request})
            else:
                return {"message": "register not successfully"}
# registration end


# login
@app.get("/login")
def get_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login/", response_class=HTMLResponse)
def post_login_form(request: Request, response: Response, email: str = Form(...), pswd: str = Form(...)):
    passhash = hashlib.sha1(pswd.encode()).hexdigest()
    mycusor.execute("USE userinfos;")
    mycusor.execute("SELECT * FROM user WHERE username =%s", (email,))
    for user in mycusor:
        if user[1] == passhash:
            return templates.TemplateResponse("home.html", {"request": request})
        else:
            return {"message": "Login not successfully"}
 # login end

# items


@app.get("/items")
def get_login_form(request: Request):
    return templates.TemplateResponse("items.html", {"request": request})


@app.post("/items")
async def post_items_form(request: Request, title: str = Form(...), description: str = Form(...), image: UploadFile = File(...)):
    img = await image.read()
    # MOngo db connection
    client = MongoClient(
        "mongodb+srv://pooyaarab:zJMzoHr1fMhOnnHk@cluster0.vwrrya4.mongodb.net/?retryWrites=true&w=majority")
    db = client.test
    fs = gridfs.GridFS(db)

    with fs.new_file() as fp:
        fp.write(img)

    item = {
        "title": title,
        "description": description,
        "image": fp._id
    }
    items = db.items
    result = items.insert_one(item)
    return {"message": "Image was uploaded successfully"}
  # items end
