from datetime import datetime
from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    email: str
    grade: int


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    grade: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    
class StudentLogin(BaseModel):
    email: str
    password: str