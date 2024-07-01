from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StudentProfileCreate(BaseModel):
    name: str
    email: str
    password: str
    dateOfBirth: datetime

class StudentProfileUpdate(BaseModel):
    studentID: int
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    dateOfBirth: Optional[datetime] = None

class StudentProfileResponse(BaseModel):
    studentID: int
    name: str
    email: str
    password: str
    dateOfBirth: datetime

    class Config:
        orm_mode = True

class ProfileUpdateResponse(BaseModel):
    updateID: int
    studentID: int
    updatedFields: List[str]
    timestamp: datetime
