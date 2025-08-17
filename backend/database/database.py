from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated


DATABASE_URL = "sqlite:///./test.db"
#DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/believe"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

<<<<<<< HEAD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
=======
Base = declarative_base()

>>>>>>> b9885e6 (application loads without the homepage showing if not signed in)


