from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

#pydantic automatically validates posted data according to BaseModel


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # defaults to true

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    created_by: UserResponse

    class Config:
        from_attributes = True

class PostVote(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)


#this doesnt work properly currently
class Update(BaseModel):
    title: str = None
    content: str = None
    published: bool = True