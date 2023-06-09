from fastapi import FastAPI,Response,status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session  
from ..database import  get_db
from .. import models, schemas, utils, oauth2
from typing import Optional,List
from sqlalchemy import func

router = APIRouter(
    prefix="/posts", # + /posts/id
    tags=["Posts"]
)
##########Post############

    

# @app.get("/posts")
# def get_posts():
#     return {"data": "this is your posts"}


@router.get("/",response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user),
                  limit: int = 10, skip: int = 0, search: Optional[str] = ""): #%20 in postman for space
    
    # posts= db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all() # type: ignore #.filter(models.Post.user_id == current_user.id)
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
         models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    return posts  #{"data": posts})

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

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):  
    # cursor.execute("""INSERT INTO posts (title,content,published)
    #                 values (%s,%s,%s) RETURNING * """,
    #                 (post.title, post.content, post.published)) ##recommended to prevent SQL injection
    # new_post = cursor.fetchone()

    # conn.commit()
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,1000000000000000)
    # my_posts.append(post_dict)
    
    new_post = models.Post(user_id = current_user.id, **post.dict()) #(title = post.title, content = post.content, published = post.published)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post#{"data": new_post} 


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int,db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):# response: Response):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))## this , is need or it will face error
    # post = cursor.fetchone()
    # print(post)
    # print(test_post)
    # post = find_post(id)
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
         models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    #print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    
    # if post.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                         detail= "Not authorized to perform request action") 
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return post#{"data": post }


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))## this , is need or it will face error
    # deleted_post = cursor.fetchone()

    # conn.commit()
    #look for the id to be deleted
    # index = find_index_post(id)
    deleted_query = db.query(models.Post).filter(models.Post.id == id)    

    deleted_post = deleted_query.first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")
    if deleted_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= "Not authorized to perform request action")    
    
    deleted_query.delete(synchronize_session=False)
    db.commit()
    
    # my_posts.pop(deleted_post)
    #return {'message': f"post {index} was successfully deleted" }
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
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
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= "Not authorized to perform request action") 

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
