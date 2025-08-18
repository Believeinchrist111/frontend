from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette import status
from database.database import SessionLocal, get_db
from fastapi.security import OAuth2PasswordRequestForm

from database import models
from database import schemas
from utility import utils
from utility import oauth2

router = APIRouter(
    # prefix="/auth",
    tags=["auth"]
)

db_dependency = Annotated[Session, Depends(get_db)]

# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

# Endpoint for signing up or creating an account
@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def sign_up(user: schemas.UserCreate, db: db_dependency):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)

    token = oauth2.create_verification_token(new_user.email)

    if token is None:
        return {"message": "token cannot be created"}

    # token sent to new email created. user clicks on link to trigger /verify endpoint
    await oauth2.send_verification_email(new_user.email, token)

    db.commit()
    db.refresh(new_user)
    return new_user

# this is triggered when the user clicks on the token to verify
@router.get("/verify")
def verify_email(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        return {"message": "Email verified successfully"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired")


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


