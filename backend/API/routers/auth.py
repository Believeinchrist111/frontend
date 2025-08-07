from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import database, models, utils, schemas
from . import oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_cred: schemas.LoginRequest, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        or_(
            models.User.email == user_cred.username,
            models.User.username == user_cred.username
        )).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify(user_cred.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data = {'user_id': user.id})
    return {"access_token" : access_token, "token_type": "bearer"}
