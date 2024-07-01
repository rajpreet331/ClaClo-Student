from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Exercise(BaseModel):
    exerciseID: int
    courseID: int
    teacherID: int
    exerciseData: bytes
    creationDate: datetime = Field(default_factory=datetime.utcnow)

class ExerciseUpdate(BaseModel):
    updateID: int
    exerciseID: int
    updatedFields: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ExerciseSubmission(BaseModel):
    submissionID: int
    exerciseID: int
    studentID: int
    submissionData: bytes
    submissionDate: datetime = Field(default_factory=datetime.utcnow)

class ExerciseSubmissionUpdate(BaseModel):
    updateID: int
    submissionID: int
    updatedFields: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
