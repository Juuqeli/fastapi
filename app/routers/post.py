from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute("""select * from posts """)
    #posts = cursor.fetchall()
    votes_on_posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all() #joins as inner by default
    if not votes_on_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts to show")
    return votes_on_posts # fastapi serializes this variable automatically to JSON

@router.get("/currentuser", response_model=List[schemas.PostVote])
def get_own_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.user_id == current_user.id).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {current_user.id} has not posted yet")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 # .model_dump converts BaseModel to python dictionary
    #cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning * """, (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(user_id=current_user.id, **post.model_dump())
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #same as SQL code "returning *"
    return new_post

@router.get("/{id}", response_model=schemas.PostVote) # path parameter
def get_post(id: int, db: Session = Depends(get_db)): # automatically validates/converts id as integer
    #cursor.execute("""select * from posts where id = %s""", (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""delete from posts where id = %s returning * """, (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_owner = post_query.first()

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    if post_owner.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) # returning any data or messages when sending delete requests might throw an exception

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning * """, (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()