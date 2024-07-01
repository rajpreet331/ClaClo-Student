from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RecordGrade(BaseModel):
    teacherID: int
    studentID: int
    assignmentID: int
    grade: float
    comments: Optional[str] = ""

class UpdateGrade(BaseModel):
    gradeID: int
    teacherID: int
    grade: float
    comments: Optional[str] = ""

class RetrieveGrade(BaseModel):
    studentID: int
    assignmentID: int

class GradeResponse(BaseModel):
    gradeID: int
    assignmentID: int
    studentID: int
    grade: float
    comments: str
    recordDate: datetime

    class Config:
        orm_mode = True

class GradeUpdateResponse(BaseModel):
    updateID: int
    gradeID: int
    updatedFields: List[str]
    timestamp: datetime

    class Config:
        orm_mode = True
