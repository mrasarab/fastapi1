FROM python:3.8

ADD main.py .

RUN pip install fastapi uvicorn pymongo mysql.connector

CMD [ "uvicorn", "main:app" ,"--reload" ]