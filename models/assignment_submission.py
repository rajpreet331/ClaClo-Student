from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Assignment(BaseModel):
    assignmentID: int
    courseID: int
    teacherID: int
    description: str
    dueDate: datetime

class Submission(BaseModel):
    submissionID: int
    assignmentID: int
    studentID: int
    submissionData: bytes
    submissionDate: datetime = Field(default_factory=datetime.utcnow)

class SubmissionUpdate(BaseModel):
    updateID: int
    submissionID: int
    updatedFields: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
