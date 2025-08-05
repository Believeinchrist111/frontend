# database.py
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

#idk but my database name is Jesus, so if you want to test locally,
# create your database server with Jesus as dbname or feel free to change on test branch
DATABASE_URL = " however we decide to do. if we deiced to work on one databse, i share the URL of my server to you"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "Connected to MySQL successfully"}