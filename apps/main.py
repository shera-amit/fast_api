from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException, status, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import user, post, auth


app = FastAPI()

models.Base.metadata.create_all(bind=engine)
# Dependency


# post --> title: str, content: str

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="fastapi",
            user="postgres",
            password="amits",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Connected to database")
        break
    except Exception as error:
        print("Error while connecting to database", error)
        time.sleep(5)


# path operation


app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)


@app.get("/")
def root():  # name here doesn't matter but work accordingly!
    return {"message": "Welcome to my API."}
