from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str
    grade: int = Field(ge=1, le=12)


class StudentResponse(StudentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime