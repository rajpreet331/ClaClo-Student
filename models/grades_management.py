from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Grade(BaseModel):
    gradeID: int
    assignmentID: int
    studentID: int
    grade: float
    comments: str
    recordDate: datetime = Field(default_factory=datetime.utcnow)

class GradeUpdate(BaseModel):
    updateID: int
    gradeID: int
    updatedFields: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
