from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class StudentProfile(BaseModel):
    studentID: int
    name: str
    email: str
    password: str
    dateOfBirth: datetime

class ProfileUpdate(BaseModel):
    updateID: int
    studentID: int
    updatedFields: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
