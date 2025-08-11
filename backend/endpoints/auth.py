from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette import status
from database.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer



from database import models
from database import schemas
from utility import utils
from utility.config import Settings
from utility import oauth2

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

settings = Settings()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


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
@router.post("/login", status_code= status.HTTP_201_CREATED)
async def login(user_cred: schemas.LoginRequest, db: db_dependency):

    user = db.query(models.User).filter(
        or_(
            models.User.email == user_cred.username,
            models.User.username == user_cred.username
        )).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data = {'user_id': user.id})
    return {"access_token" : access_token, "token_type": "bearer"}






# from fastapi import APIRouter, Depends, status, HTTPException, Response
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from database import database, models, utils, schemas

# router = APIRouter(tags=['Authentication'])



# @router.post('/login')
# def login(user_cred: schemas.LoginRequest, db: Session = Depends(database.get_db)):

#     user = db.query(models.User).filter(
#         or_(
#             models.User.email == user_cred.username,
#             models.User.username == user_cred.username
#         )).first()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
#     if not utils.verify(user_cred.password,user.password):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

#     access_token = oauth2.create_access_token(data = {'user_id': user.id})
#     return {"access_token" : access_token, "token_type": "bearer"}
