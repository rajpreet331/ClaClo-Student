from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class CreateExercise(BaseModel):
    courseID: int
    teacherID: int
    exerciseData: bytes

class UpdateExercise(BaseModel):
    exerciseID: int
    exerciseData: bytes

class RetrieveExercise(BaseModel):
    studentID: int
    courseID: int

class ExerciseResponse(BaseModel):
    exerciseID: int
    courseID: int
    teacherID: int
    exerciseData: bytes
    creationDate: datetime

class ExerciseUpdateResponse(BaseModel):
    updateID: int
    exerciseID: int
    updatedFields: List[str]
    timestamp: datetime
