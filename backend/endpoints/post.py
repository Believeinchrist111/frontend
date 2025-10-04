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
@posts_router.post("/create_post", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(
    post: schemas.CreatePostRequest, 
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



# Route to create a new reply
@posts_router.post("/create_reply/{post_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_reply(
    post_id: int,
    reply: schemas.CreateReplyRequest, 
    db: db_dependency, 
    current_user: models.User = Depends(oauth2.get_current_user)
):
    parent_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not parent_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Create the reply object
    new_reply = models.Post(
        content=reply.content,
        reply_to_post_id=reply.reply_to_post_id,
        repost_of_post_id=reply.repost_of_post_id,
        is_repost=reply.is_repost,
        owner_id=current_user.id,
        created_at=datetime.now(timezone.utc)
    )

    # If media_items are provided, add them
    if reply.media_items:
        new_reply.media_items = [
            models.Media(file_url=media.file_url, type=media.type)
            for media in reply.media_items
        ]
    

    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    db.refresh(new_reply, attribute_names=["owner", "media_items"])
    return new_reply



# this is what gets displayed on the timeline
@posts_router.get("", response_model=List[schemas.PostResponse])
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



# Endpoint for getting a post
@posts_router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: db_dependency):
    # Using joinedload so owner and media_items load eagerly
    post = (
        db.query(models.Post)
        .options(
            joinedload(models.Post.owner),
            joinedload(models.Post.media_items),
            joinedload(models.Post.replies),
            joinedload(models.Post.repost)
        )
        .filter(models.Post.id == post_id)
        .first()
    )

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post
    # Serializing the post manually into JSON-compatible dict
    # return {
    #     "id": post.id,
    #     "content": post.content,
    #     "created_at": post.created_at,
    #     "reply_to_post_id": post.reply_to_post_id,
    #     "is_repost": post.is_repost,
    #     "repost_of_post_id": post.repost_of_post_id,
    #     "owner": {
    #         "id": post.owner.id,
    #         "firstname": post.owner.firstname,
    #         "lastname": post.owner.lastname,
    #         "email": post.owner.email,
    #         "date_of_birth": post.owner.date_of_birth,
    #     } if post.owner else None,
    #     "media_items": [
    #         {
    #             "file_url": media.file_url,
    #             "type": media.type,
    #         }
    #         for media in post.media_items
    #     ],
    #     "replies": [
    #         {
    #             "id": reply.id,
    #             "content": reply.content,
    #             "created_at": reply.created_at,
    #             "owner_id": reply.owner_id,
    #         }
    #         for reply in post.replies
    #     ],
    #     "repost": {
    #         "id": post.repost.id,
    #         "content": post.repost.content,
    #         "owner_id": post.repost.owner_id,
    #     } if post.repost else None,
    # }





# only a user can delete his own post
@posts_router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
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
@posts_router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.CreatePostRequest, db: db_dependency, current_user: int = Depends(oauth2.get_current_user)):
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

