from sqlalchemy import select

from config.db import Base, SessionLocal, engine
from models.student import Student

SAMPLE_STUDENTS = [
    {"name": "Aarav Sharma", "email": "aarav.sharma@example.com", "grade": 6},
    {"name": "Diya Patel", "email": "diya.patel@example.com", "grade": 8},
    {"name": "Noah Williams", "email": "noah.williams@example.com", "grade": 10},
    {"name": "Emma Johnson", "email": "emma.johnson@example.com", "grade": 12},
]


def seed_students() -> int:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        existing_emails = set(
            db.scalars(
                select(Student.email).where(
                    Student.email.in_(student["email"] for student in SAMPLE_STUDENTS)
                )
            )
        )
        new_students = [
            Student(**student)
            for student in SAMPLE_STUDENTS
            if student["email"] not in existing_emails
        ]
        db.add_all(new_students)
        db.commit()
        return len(new_students)


if __name__ == "__main__":
    inserted = seed_students()
    print(f"Inserted {inserted} sample student(s).")
