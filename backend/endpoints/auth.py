from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette import status
from database.database import SessionLocal
from database.database import db_dependency
from fastapi.security import OAuth2PasswordRequestForm

from database import models
from database import schemas
from utility import utils
from utility import oauth2

router = APIRouter(
    # prefix="/auth",
    tags=["auth"]
)

# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

# Endpoint for signing up or creating an account
@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def sign_up(user: schemas.UserCreate, db: db_dependency):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


# Endpoint for signing in or logging into an account
@router.post("/token", response_model = schemas.Token)
async def login_for_access_token(db: db_dependency, user_cred: OAuth2PasswordRequestForm = Depends()):

    user = db.query(models.User).filter(
        or_(
            models.User.email == user_cred.username,
            models.User.username == user_cred.username
        )).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not found")

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password")

    access_token = oauth2.create_access_token(data = {'user_id': user.id})
    return {"access_token" : access_token, "token_type": "bearer"}

@router.get("/login", response_model = schemas.UserCreate)
async def read_user(current_user: schemas.UserCreate = Depends(oauth2.get_current_user)):
    return current_user


# @router.get("/users/me/", response_model=schemas.UserCreate)
# async def read_users_me(current_user: schemas.UserCreate = Depends(oauth2.get_current_user)):
#     return current_user


