from fastapi import FastAPI#,#Response,status, HTTPException,Depends
# from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Optional,List
# from random import randrange
from .config import settings
# from . import models#,schemas,utils
# from sqlalchemy.orm import Session  

from .routers import post, user, auth, vote

##alembic
#11:34:40
#after alembic we really do not needs this below
# models.Base.metadata.create_all(bind=engine)

 #fetch("http://localhost:8000").then(res => res.json()).then(console.log)
################################################################################################################
print(settings.database_name)

app = FastAPI()

origins = ["*"] # you can specify domains to acces APIs. Like origins = ["https://www.google.com",""https://www.youtube.com""]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/") ### root path/router
async def root():
    return {"message":"Welcome to Suman Pathak's API project"}


# class UpdatePost(BaseModel):
#     id: int
#     title: str
#     content: str
###ARBITRARY ARRAY ############
# my_posts = [{"title": "title for latest post", "content": "content for latest post","id": 1},
#             {"title": "title for second post", "content": "content for second post","id": 2}]

# ###functions#############
# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p
        
# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#        if p['id'] == id: 
#             return i





# @app.get("/sqlalchemy")
# def tes_posts(db: Session = Depends(get_db)):
#     posts= db.query(models.Post).all()
#     #print(posts)
#     return {"data": posts}
    #return  {"status": "success"}