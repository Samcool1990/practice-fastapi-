from fastapi import FastAPI,Response,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine,SessionLocal


models.Base.metadata.create_all(bind=engine)
################################################################################################################

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
############# MODEL #####################################################################################
class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating : Optional[int] = None
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


# @app.get("/posts")
# def get_posts():
#     return {"data": "this is your posts"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    #print(posts)
    return {"data": posts}

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
def create_posts(post: Post):  
    cursor.execute("""INSERT INTO posts (title,content,published)
                    values (%s,%s,%s) RETURNING * """,
                    (post.title, post.content, post.published)) ##recommended to prevent SQL injection
    new_post = cursor.fetchone()

    conn.commit()
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,1000000000000000)
    # my_posts.append(post_dict)
    return {"data": new_post} 


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))## this , is need or it will face error
    post = cursor.fetchone()
    print(post)
    # print(test_post)
    # post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return {"data": post }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))## this , is need or it will face error
    deleted_post = cursor.fetchone()

    conn.commit()
    #look for the id to be deleted
    # index = find_index_post(id)

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")

    # my_posts.pop(deleted_post)
    #return {'message': f"post {index} was successfully deleted" }
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING *""",
                   (post.title,post.content,post.published,(str(id),)) )## this , is need or it will face error
    updated_post = cursor.fetchone()
    conn.commit()
    # index = find_index_post(id)

    if updated_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")

    
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] =  post_dict
    return {"data": updated_post}


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
    