from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from database.database import db_dependency
from database.database import get_db


from database import models
from endpoints import auth
from endpoints import user
from endpoints import post
from utility.oauth2 import get_current_user
from fastapi.middleware.cors import CORSMiddleware

origins = [ "*" ]

app = FastAPI()

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

models.Base.metadata.create_all(bind=engine)

user_dependency = Annotated[Session, Depends(get_current_user)]

@app.get("/", status_code = status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user}
