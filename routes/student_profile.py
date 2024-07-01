from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from datetime import datetime

from models.student_profile import StudentProfile, ProfileUpdate
from schemas.student_profile import StudentProfileCreate, StudentProfileUpdate, StudentProfileResponse, ProfileUpdateResponse

router = APIRouter()

client = MongoClient("mongodb+srv://preetr841:GyfWFDtJVoFldicc@cluster0.e9inxl5.mongodb.net/?appName=Cluster0")
db = client["StudentProfileDatabase"]
student_profiles = db["StudentProfiles"]
profile_updates = db["ProfileUpdates"]

@router.post("/create", response_model=StudentProfileResponse)
async def create_profile(profile: StudentProfileCreate):
    profile_data = profile.dict()
    profile_data["dateOfBirth"] = datetime.combine(profile_data["dateOfBirth"], datetime.min.time())
    student_id = student_profiles.count_documents({}) + 1
    profile_data["studentID"] = student_id

    student_profile = StudentProfile(**profile_data)
    result = student_profiles.insert_one(student_profile.dict())
    if result.inserted_id:
        return StudentProfileResponse(**student_profile.dict())
    raise HTTPException(status_code=500, detail="Profile creation failed")

@router.put("/update", response_model=ProfileUpdateResponse)
async def update_profile(profile_update: StudentProfileUpdate):
    updated_fields = {}
    for field, value in profile_update.dict(exclude_unset=True).items():
        if field == "dateOfBirth" and value is not None:
            value = datetime.combine(value, datetime.min.time())
        if field != "studentID":
            updated_fields[field] = value

    result = student_profiles.update_one({"studentID": profile_update.studentID}, {"$set": updated_fields})
    if result.modified_count == 1:
        update_id = profile_updates.count_documents({}) + 1
        profile_update_record = ProfileUpdate(
            updateID=update_id,
            studentID=profile_update.studentID,
            updatedFields=list(updated_fields.keys())
        )
        profile_updates.insert_one(profile_update_record.dict())
        return ProfileUpdateResponse(**profile_update_record.dict())
    raise HTTPException(status_code=404, detail="Profile not found")

@router.get("/retrieve/{studentID}", response_model=StudentProfileResponse)
async def retrieve_profile(studentID: int):
    profile = student_profiles.find_one({"studentID": studentID})
    if profile:
        return StudentProfileResponse(**profile)
    raise HTTPException(status_code=404, detail="Profile not found")
