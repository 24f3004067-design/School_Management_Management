import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL is missing in .env")

# PostgreSQL connection
engine = create_engine(DATABASE_URL)

# Database session
SessionLocal = sessionmaker(bind=engine)


# Base class for database models
class Base(DeclarativeBase):
    pass


# Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()