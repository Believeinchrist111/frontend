from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import models, schemas
from database.database import get_db
from database import utils

router = APIRouter(prefix="/signup")

@router.post("", status_code=status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# we can use this internally for our own debugs
@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No User Found")

    return user
