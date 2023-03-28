from fastapi import FastAPI,Response,status, HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas,utils
from .database import engine, get_db
from sqlalchemy.orm import Session  

from .routers import post, user,auth


models.Base.metadata.create_all(bind=engine)

##6:33:36
################################################################################################################

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
############DB CONNECTION####################
while True:
    try: 
        conn = psycopg2.connect(host='localhost',
                            database='My FASTAPI DATABSE local',
                            user='postgres',
                            password='321456',
                            cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print("Database connection was succesfull!!")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("error", error)
        time.sleep(2)



# class UpdatePost(BaseModel):
#     id: int
#     title: str
#     content: str
###ARBITRARY ARRAY ############
my_posts = [{"title": "title for latest post", "content": "content for latest post","id": 1},
            {"title": "title for second post", "content": "content for second post","id": 2}]

###functions#############
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
       if p['id'] == id: 
            return i



@app.get("/") ### root path/router
async def root():
    return {"message":"Welcome to Suman Pathak's API project"}

# @app.get("/sqlalchemy")
# def tes_posts(db: Session = Depends(get_db)):
#     posts= db.query(models.Post).all()
#     #print(posts)
#     return {"data": posts}
    #return  {"status": "success"}