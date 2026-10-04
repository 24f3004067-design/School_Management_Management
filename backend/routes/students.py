from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.db import get_db
from models.user import User, UserRole
from routes.auth import get_current_user, require_roles
from models.student import Student
from schemas.student import StudentCreate, StudentResponse


router = APIRouter(
    prefix="/students",
    tags=["students"]
)


# Create student
@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN, UserRole.TEACHER)),
):
    student = Student(
        **student_data.model_dump()
    )

    db.add(student)

    try:
        db.commit()
        db.refresh(student)

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student with this email already exists",
        ) from exc

    return student


# Get active students
@router.get("",response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    students = (
        db.query(Student)
        .filter(Student.is_active == True)
        .order_by(Student.name)
        .all()
    )

    return students