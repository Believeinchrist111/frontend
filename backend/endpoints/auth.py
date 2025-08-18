from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette import status
from database.database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from database import models
from database import schemas
from utility import utils
from utility import oauth2


router = APIRouter(
    tags=["auth"]
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='sign-in')

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
@router.post("/sign-in")
async def login_for_access_token(
    db: Session = Depends(get_db),
    user_cred: OAuth2PasswordRequestForm = Depends()
):
    user = db.query(models.User).filter(
        or_(
            models.User.email == user_cred.username,
            models.User.username == user_cred.username
        )
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password")

    access_token = oauth2.create_access_token(
        data={'user_id': user.id},
    )
    
    print('the token in the sign in endpoint')
    print(access_token)
    print('the token in the sign in endpoint')
    
    response = JSONResponse(content={
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    })
    
    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        secure=False,  # Change to True in production
        samesite="lax",
        max_age= 30 * 60,
    )
    return response

    
@router.get("/verify-token")
async def verify_token(token: str = Depends(oauth2_bearer)):
    print("the token in the verify token endpoint")
    print(token)
    print("the token in the verify token endpoint")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = oauth2.verify_access_token(token, credentials_exception)
    return {"user_id": token_data.id}




@router.get("/login", response_model = schemas.UserCreate)
async def read_user(current_user: schemas.UserCreate = Depends(oauth2.get_current_user)):
    return current_user


# @router.get("/users/me/", response_model=schemas.UserCreate)
# async def read_users_me(current_user: schemas.UserCreate = Depends(oauth2.get_current_user)):
#     return current_user


