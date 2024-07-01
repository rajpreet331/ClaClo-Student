from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class CourseMaterial(BaseModel):
    materialID: int
    courseID: int
    teacherID: int
    materialData: bytes
    uploadDate: datetime = Field(default_factory=datetime.utcnow)

class MaterialUpdate(BaseModel):
    updateID: int
    materialID: int
    updatedFields: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
