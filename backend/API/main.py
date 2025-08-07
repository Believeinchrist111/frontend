from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, auth, post
from database import utils
from database.models import Base
from database.database import engine

Base.metadata.create_all(bind=engine)

origins = [ "*" ]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(post.router)

@app.get('/')
def root():
    return {"message": "Hello!"}
