from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class CreateNotification(BaseModel):
    studentID: int
    notificationType: str
    message: str

class UpdateNotification(BaseModel):
    notificationID: int
    message: str

class RetrieveNotification(BaseModel):
    studentID: int

class NotificationResponse(BaseModel):
    notificationID: int
    studentID: int
    notificationType: str
    message: str
    timestamp: datetime

class NotificationUpdateResponse(BaseModel):
    updateID: int
    notificationID: int
    updatedFields: List[str]
    timestamp: datetime
