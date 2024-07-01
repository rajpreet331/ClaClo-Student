from fastapi import APIRouter, HTTPException, Query
from pymongo import MongoClient
from datetime import datetime
from typing import List

from models.notifications import Notification, NotificationUpdate
from schemas.notifications import CreateNotification, UpdateNotification, NotificationResponse, NotificationUpdateResponse

router = APIRouter()

client = MongoClient("mongodb+srv://preetr841:GyfWFDtJVoFldicc@cluster0.e9inxl5.mongodb.net/?appName=Cluster0")
db_notifications = client["NotificationsDatabase"]
notifications_collection = db_notifications["Notifications"]
notification_updates_collection = db_notifications["NotificationUpdates"]

def get_next_id(collection, id_field):
    last_item = collection.find_one(sort=[(id_field, -1)])
    if last_item:
        return last_item[id_field] + 1
    return 1

@router.post("/create", response_model=NotificationResponse)
async def create_notification(notification: CreateNotification):
    notification_id = get_next_id(notifications_collection, "_id")
    notification_data = notification.dict()
    notification_data["_id"] = notification_id
    new_notification = Notification(**notification_data)
    result = notifications_collection.insert_one(new_notification.dict(by_alias=True))
    if result.inserted_id:
        return NotificationResponse(
            notificationID=new_notification.notificationID,
            studentID=new_notification.studentID,
            notificationType=new_notification.notificationType,
            message=new_notification.message,
            timestamp=new_notification.timestamp
        )
    raise HTTPException(status_code=500, detail="Notification creation failed")

@router.put("/update", response_model=NotificationUpdateResponse)
async def update_notification(notification_update: UpdateNotification):
    updated_fields = {
        "message": notification_update.message,
        "timestamp": datetime.utcnow()
    }

    # Check if the notification exists before updating
    existing_notification = notifications_collection.find_one({"_id": notification_update.notificationID})
    if not existing_notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    result = notifications_collection.update_one({"_id": notification_update.notificationID}, {"$set": updated_fields})
    if result.modified_count == 1:
        update_id = get_next_id(notification_updates_collection, "_id")
        update_record = NotificationUpdate(
            _id=update_id,
            notificationID=notification_update.notificationID,
            updatedFields=["message"],
            timestamp=datetime.utcnow()
        )
        notification_updates_collection.insert_one(update_record.dict(by_alias=True))
        return NotificationUpdateResponse(
            updateID=update_record.updateID,
            notificationID=update_record.notificationID,
            updatedFields=update_record.updatedFields,
            timestamp=update_record.timestamp
        )
    raise HTTPException(status_code=500, detail="Failed to update notification")

@router.get("/retrieve", response_model=List[NotificationResponse])
async def retrieve_notification(studentID: int):
    query = {"studentID": studentID}

    notifications = notifications_collection.find(query)
    notification_list = []
    for notification in notifications:
        notification["notificationID"] = notification["_id"]
        notification_list.append(NotificationResponse(
            notificationID=notification["_id"],
            studentID=notification["studentID"],
            notificationType=notification["notificationType"],
            message=notification["message"],
            timestamp=notification["timestamp"]
        ))

    if notification_list:
        return notification_list
    raise HTTPException(status_code=404, detail="Notifications not found")
