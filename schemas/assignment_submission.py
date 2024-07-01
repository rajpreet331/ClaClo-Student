from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AssignmentSubmission(BaseModel):
    studentID: int
    assignmentID: int
    submissionData: bytes

class AssignmentSubmissionUpdate(BaseModel):
    submissionID: int
    studentID: int
    submissionData: bytes

class AssignmentSubmissionRetrieve(BaseModel):
    studentID: Optional[int] = None
    assignmentID: Optional[int] = None

class AssignmentResponse(BaseModel):
    assignmentID: int
    courseID: int
    teacherID: int
    description: str
    dueDate: datetime

    class Config:
        orm_mode = True

class SubmissionResponse(BaseModel):
    submissionID: int
    assignmentID: int
    studentID: int
    submissionData: bytes
    submissionDate: datetime

    class Config:
        orm_mode = True

class SubmissionUpdateResponse(BaseModel):
    updateID: int
    submissionID: int
    updatedFields: List[str]
    timestamp: datetime
