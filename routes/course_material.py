from fastapi import APIRouter, HTTPException, Query
from pymongo import MongoClient
from datetime import datetime

from models.course_material import CourseMaterial, MaterialUpdate
from schemas.course_material import CourseMaterialUpload, CourseMaterialUpdate, CourseMaterialRetrieve, CourseMaterialResponse, MaterialUpdateResponse

router = APIRouter()

client = MongoClient("mongodb+srv://preetr841:GyfWFDtJVoFldicc@cluster0.e9inxl5.mongodb.net/?appName=Cluster0")
db_course_materials = client["CourseMaterialsDatabase"]
course_materials = db_course_materials["CourseMaterials"]
material_updates = db_course_materials["MaterialUpdates"]

db_student_profiles = client["StudentProfileDatabase"]
student_profiles = db_student_profiles["StudentProfiles"]

@router.post("/upload", response_model=CourseMaterialResponse)
async def upload_material(material: CourseMaterialUpload):
    material_data = material.dict()
    material_id = course_materials.count_documents({}) + 1
    material_data["materialID"] = material_id
    course_material = CourseMaterial(**material_data)
    result = course_materials.insert_one(course_material.dict())
    if result.inserted_id:
        return CourseMaterialResponse(**course_material.dict())
    raise HTTPException(status_code=500, detail="Material upload failed")

@router.put("/update", response_model=MaterialUpdateResponse)
async def update_material(material_update: CourseMaterialUpdate):
    updated_fields = {
        "materialData": material_update.materialData,
        "timestamp": datetime.utcnow()
    }

    result = course_materials.update_one({"materialID": material_update.materialID, "teacherID": material_update.teacherID}, {"$set": updated_fields})
    if result.modified_count == 1:
        update_id = material_updates.count_documents({}) + 1
        update_record = MaterialUpdate(
            updateID=update_id,
            materialID=material_update.materialID,
            updatedFields=["materialData"]
        )
        material_updates.insert_one(update_record.dict())
        return MaterialUpdateResponse(**update_record.dict())
    raise HTTPException(status_code=404, detail="Material not found or update not authorized")

@router.get("/retrieve", response_model=CourseMaterialResponse)
async def retrieve_material(
    courseID: int = Query(..., description="Course ID"),
    materialID: int = Query(None, description="Material ID"),
    studentID: int = Query(None, description="Student ID")
):
    query = {"courseID": courseID}
    if materialID:
        query["materialID"] = materialID

    material = course_materials.find_one(query)
    if material:
        
        if studentID is None and "teacherID" in material:
            student_profile = student_profiles.find_one({"studentID": material["teacherID"]})
            if student_profile:
                material["studentID"] = student_profile["studentID"]  

        return CourseMaterialResponse(**material)
    
    raise HTTPException(status_code=404, detail="Material not found")
