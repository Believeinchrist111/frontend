from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# DATABASE_URL = "sqlite:///./test.db"
DATABASE_URL =  "mysql+pymysql://root:password@localhost:3306/believe"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


