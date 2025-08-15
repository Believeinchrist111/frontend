from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from database import schemas, models
from datetime import datetime, timezone
from database.database import get_db
from utility.oauth2 import get_current_user
from typing import List, Optional, Annotated

# Create an APIRouter for posts with a common prefix and tag
router = APIRouter(
    prefix="/messages",
    tags=['messages']
)

user_dependency = Annotated[Session, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("", response_model=List[schemas.MessageResponse])
def get_messages(db: db_dependency, current_user: user_dependency, search: Optional[str] = ""):

    messages = ( db.query(models.Message)
        .filter(
            (models.Message.sender_id == current_user) |
            (models.Message.receiver_id == current_user) )
    )

    query = db.query(models.Message).filter(
        (models.Message.sender_id == current_user.id) |
        (models.Message.receiver_id == current_user.id)
    )

    if receiver_id:
        query = query.filter(
            (models.Message.sender_id == receiver_id) |
            (models.Message.receiver_id == receiver_id)
        )

    if search:
        query = query.filter(models.Message.content.ilike(f"%{search}%"))

    return query.order_by(models.Message.created_at.asc()).all()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.MessageResponse)
def create_message(message: schemas.MessageCreate, db: db_dependency, current_user_id: user_dependency):
    new_message = models.Message(
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        content=message.content,
        media_id=message.media_id,
    )

    #print(new_message.sender_id)
    print(current_user_id)

    if new_message.sender_id != current_user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to send message")

    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return schemas.MessageResponse.model_validate(new_message)

@router.put("/{message_id}", response_model=schemas.MessageResponse)
def update_message(message_id: int, message: schemas.MessageCreate, db: db_dependency, current_user: user_dependency):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    if message.sender_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to update messaage")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(message, field, value)

    db.commit()
    db.refresh(message)
    return message

@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(message_id: int, db: db_dependency, current_user: user_dependency):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    if message.sender_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to delete message")

    db.delete(message)
    db.commit()
    return {"detail": "Message deleted"}
