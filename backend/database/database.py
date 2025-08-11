from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()










# import os
# from fastapi import FastAPI, Depends
# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker, Session

# #DATABASE_URL = "link will be shared "
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# app = FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/")
# def root(db: Session = Depends(get_db)):
#     return {"message": "Connected to MySQL successfully"}