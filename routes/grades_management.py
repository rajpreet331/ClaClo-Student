from fastapi import APIRouter, HTTPException, Query
from pymongo import MongoClient
from datetime import datetime

from models.grades_management import Grade, GradeUpdate
from schemas.grades_management import RecordGrade, UpdateGrade, RetrieveGrade, GradeResponse, GradeUpdateResponse

router = APIRouter()

client = MongoClient("mongodb+srv://preetr841:GyfWFDtJVoFldicc@cluster0.e9inxl5.mongodb.net/?appName=Cluster0")
db_grades = client["GradesManagementDatabase"]
grades_collection = db_grades["Grades"]
grade_updates_collection = db_grades["GradeUpdates"]

@router.post("/record", response_model=GradeResponse)
async def record_grade(grade: RecordGrade):
    grade_data = grade.dict()
    grade_data["gradeID"] = grades_collection.count_documents({}) + 1
    new_grade = Grade(**grade_data)
    result = grades_collection.insert_one(new_grade.dict())
    if result.inserted_id:
        return GradeResponse(**new_grade.dict())
    raise HTTPException(status_code=500, detail="Grade recording failed")

@router.put("/update", response_model=GradeUpdateResponse)
async def update_grade(grade_update: UpdateGrade):
    updated_fields = {
        "grade": grade_update.grade,
        "comments": grade_update.comments,
        "recordDate": datetime.utcnow()
    }

    existing_grade = grades_collection.find_one({"gradeID": grade_update.gradeID})
    if not existing_grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    result = grades_collection.update_one({"gradeID": grade_update.gradeID}, {"$set": updated_fields})
    if result.modified_count == 1:
        update_id = grade_updates_collection.count_documents({}) + 1
        update_record = GradeUpdate(
            updateID=update_id,
            gradeID=grade_update.gradeID,
            updatedFields=["grade", "comments"]
        )
        grade_updates_collection.insert_one(update_record.dict())
        return GradeUpdateResponse(**update_record.dict())
    raise HTTPException(status_code=500, detail="Failed to update grade")

@router.get("/retrieve", response_model=GradeResponse)
async def retrieve_grade(
    studentID: int = Query(..., description="Student ID"),
    assignmentID: int = Query(..., description="Assignment ID")
):
    query = {"studentID": studentID, "assignmentID": assignmentID}

    grade = grades_collection.find_one(query)
    if grade:
        return GradeResponse(**grade)
    
    raise HTTPException(status_code=404, detail="Grade not found")
