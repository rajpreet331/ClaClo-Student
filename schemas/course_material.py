from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CourseMaterialUpload(BaseModel):
    teacherID: int
    courseID: int
    materialData: bytes

class CourseMaterialUpdate(BaseModel):
    materialID: int
    teacherID: int
    materialData: bytes

class CourseMaterialRetrieve(BaseModel):
    studentID: int
    courseID: int
    materialID: Optional[int] = None

class CourseMaterialResponse(BaseModel):
    materialID: int
    courseID: int
    teacherID: int
    materialData: bytes
    uploadDate: datetime

    class Config:
        orm_mode = True

class MaterialUpdateResponse(BaseModel):
    updateID: int
    materialID: int
    updatedFields: List[str]
    timestamp: datetime
