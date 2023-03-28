from fastapi import FastAPI,Response,status, HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
################################################################################################################

app = FastAPI()

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
##########URLs############
@app.get("/") ### root path/router
async def root():
    return {"message":"Welcome to Suman Pathak's API project"}

# @app.get("/sqlalchemy")
# def tes_posts(db: Session = Depends(get_db)):
#     posts= db.query(models.Post).all()
#     #print(posts)
#     return {"data": posts}
    #return  {"status": "success"}
    

# @app.get("/posts")
# def get_posts():
#     return {"data": "this is your posts"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts= db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    #print(posts)
    return posts#{"data": posts}

# @app.post("/posts")
# #def create_posts(payload: dict = Body(...)):
# def create_posts(new_post: Post):
#     #print (payload)
#     print (new_post.rating)
#     #in order to convert pydantic model below
#     print(new_post.dict())
#     #return {"message": "successfully created post"}
#     #return {"new_post": f"title: {payload['title']} content: {payload['content']}"}
#     return {"data": new_post} #"new_post created"

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db)):  
    # cursor.execute("""INSERT INTO posts (title,content,published)
    #                 values (%s,%s,%s) RETURNING * """,
    #                 (post.title, post.content, post.published)) ##recommended to prevent SQL injection
    # new_post = cursor.fetchone()

    # conn.commit()
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,1000000000000000)
    # my_posts.append(post_dict)
    new_post = models.Post(**post.dict())#(title = post.title, content = post.content, published = post.published)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post#{"data": new_post} 


@app.get("/posts/{id}")
def get_post(id: int,db: Session = Depends(get_db)):# response: Response):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))## this , is need or it will face error
    # post = cursor.fetchone()
    # print(post)
    # print(test_post)
    # post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    #print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return post#{"data": post }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))## this , is need or it will face error
    # deleted_post = cursor.fetchone()

    # conn.commit()
    #look for the id to be deleted
    # index = find_index_post(id)
    deleted_post = db.query(models.Post).filter(models.Post.id == id)    

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    
    # my_posts.pop(deleted_post)
    #return {'message': f"post {index} was successfully deleted" }
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING *""",
    #                (post.title,post.content,post.published,(str(id),)) )## this , is need or it will face error
    # updated_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)    
    post = post_query.first()    

    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")

    post_query.update(updated_post.dict(),synchronize_session=False)
    
    db.commit()
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] =  post_dict
    return post_query.first()#{"data": post_query.first()}


# @app.get("/DATA/{ID}")
# DEF GET_DATA_FROM_DB(ID:INT):
     
#     RETURN GET_DATA_RECORDS(ID)

# def get_data_records(param):
#     id = param.get("id")
#     message = dict()
#     if id:
#         id == "4"
#         message["data"] = "Success in getting response"
#     return message
    