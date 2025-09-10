from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from database.database import engine
from database import models
from endpoints.auth import login
from endpoints.auth import signup
from endpoints import user
from endpoints import post
from endpoints import message
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploads folder at /uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(login.router)
app.include_router(signup.router)
app.include_router(user.router)
app.include_router(post.posts_router)
app.include_router(post.upload_media_router)
app.include_router(message.router)

models.Base.metadata.create_all(bind=engine)


