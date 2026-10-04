import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Prefer a backend-local .env, then support starting the API from the
# repository root.
load_dotenv()
if not os.getenv("DATABASE_URL"):
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing. Set it in .env or the environment.")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine_options = {
    "pool_pre_ping": True,
    "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
    "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10")),
    "connect_args": {
        "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", "5")),
    },
}

sslmode = os.getenv("DB_SSLMODE")
if sslmode:
    engine_options["connect_args"]["sslmode"] = sslmode

engine = create_engine(DATABASE_URL, **engine_options)

# Database session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

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