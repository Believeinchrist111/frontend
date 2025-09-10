from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database import models, schemas
from utility import utils
from utility.oauth2 import get_current_user
from database.database import get_db

router = APIRouter(prefix="/users")

user_dependency = Annotated[Session, Depends(get_current_user)]

db_dependency = Annotated[Session, Depends(get_db)]



@router.get("", status_code = status.HTTP_200_OK, response_model=schemas.UserResponse)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return user




# we can use this internally for our own debugs

# @router.get("/{id}", response_model=schemas.UserResponse)
# def get_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No User Found")

#     return user