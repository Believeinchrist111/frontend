from fastapi import APIRouter, Depends, Response, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional, Annotated
import os
from datetime import datetime, timezone
from fastapi.responses import JSONResponse



from database import schemas, models
from utility import oauth2
from database.database import SessionLocal, get_db


# Create an APIRouter for posts with a common prefix and tag
posts_router = APIRouter(prefix="/posts", tags=['Posts'])
upload_media_router = APIRouter(prefix="/upload-media", tags=['Media'])

db_dependency = Annotated[Session, Depends(get_db)]


# This accepts multiple files, save them, and return their URLs.
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@upload_media_router.post("")
async def upload_media(files: List[UploadFile] = File(...)):
    file_urls = []
    for file in files:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        file_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{file.filename}")
        
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # In production, we may use CDN/S3/Cloudinary instead of local paths
        file_url = f"http://127.0.0.1:8000/{file_path}"
        file_urls.append({"file_url": file_url, "type": file.content_type.split("/")[0]})
    
    return JSONResponse(content={"media_items": file_urls})


# Route to create a new post
@posts_router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate, 
    db: db_dependency, 
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # Create the post object
    new_post = models.Post(
        content=post.content,
        reply_to_post_id=post.reply_to_post_id,
        repost_of_post_id=post.repost_of_post_id,
        is_repost=post.is_repost,
        owner_id=current_user.id,
        created_at=datetime.now(timezone.utc)
    )

    # If media_items are provided, add them
    if post.media_items:
        new_post.media_items = [
            models.Media(file_url=media.file_url, type=media.type)
            for media in post.media_items
        ]
    

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    db.refresh(new_post, attribute_names=["owner", "media_items"])
    return new_post





# this is what gets displayed on the timeline
@posts_router.get("", response_model=List[schemas.Post])
def get_posts(db: db_dependency, current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    posts = ( db.query(models.Post)
        .options(joinedload(models.Post.owner))  # fetches user info with post
        .filter(models.Post.content.contains(search))
        .order_by(models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return posts




# only a user can delete his own post
@posts_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: db_dependency, current_user: int = Depends(oauth2.get_current_user)):
    query_post = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = query_post.first()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {id} was not found'
        )
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to delete post")

    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Route to update a post by ID
@posts_router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: db_dependency, current_user: int = Depends(oauth2.get_current_user)):
    query_post = db.query(models.Post).filter(models.Post.id == id)
    filtered_post = query_post.first()
    if filtered_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID:{id} does not exist"
        )
    if filtered_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to edit post")

    data = post.model_dump(exclude_unset=True)
    query_post.update(data, synchronize_session=False)
    db.commit()

    # Fetch the updated post from the database
    updated_post = query_post.first()

    return updated_post

