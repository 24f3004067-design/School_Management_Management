from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from config.db import Base, engine, get_db
from models import Student
from routes.students import router as students_router


app = FastAPI(title="School Management API")

# Student routes
app.include_router(students_router)


# Create database tables when app starts
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


# Check API
@app.get("/health")
def health():
    return {"status": "ok"}


# Check database connection
@app.get("/health/db")
def database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )

    return {
        "status": "ok",
        "database": "connected"
    }