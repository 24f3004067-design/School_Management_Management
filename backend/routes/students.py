from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.db import get_db
from models.student import Student
from schemas.student import StudentCreate, StudentResponse

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)) -> Student:
    student = Student(**payload.model_dump())
    db.add(student)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists",
        ) from exc
    db.refresh(student)
    return student


@router.get("", response_model=list[StudentResponse])
def list_active_students(db: Session = Depends(get_db)) -> list[Student]:
    return list(
        db.scalars(
            select(Student)
            .where(Student.is_active.is_(True))
            .order_by(Student.name)
        )
    )
