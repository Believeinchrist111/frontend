from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
from database.database import engine

from database import models
from endpoints import auth
from endpoints import user
from endpoints import post
from endpoints import message
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [ 
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(message.router)

models.Base.metadata.create_all(bind=engine)


