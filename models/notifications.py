from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Notification(BaseModel):
    notificationID: int = Field(..., alias="_id")
    studentID: int
    notificationType: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class NotificationUpdate(BaseModel):
    updateID: int = Field(..., alias="_id")
    notificationID: int
    updatedFields: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CreateNotification(BaseModel):
    studentID: int
    notificationType: str
    message: str

class UpdateNotification(BaseModel):
    notificationID: int
    message: str

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
