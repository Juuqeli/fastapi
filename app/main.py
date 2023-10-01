from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine) <- this is for sqlalchemy to first create all db tables

app = FastAPI()

#CORS allows you to make requests from a web browser on one domain to a server on a different domain
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#finds path operations from router folder
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#request GET method to "URL/", order matters if the path is the same
@app.get("/")
def root():
    return {"message": "Welcome to my fastAPI project, check /docs for more info"}