from fastapi import APIRouter, HTTPException, Query
from pymongo import MongoClient
from datetime import datetime
from typing import List

from models.exercise import Exercise, ExerciseUpdate
from schemas.exercise import CreateExercise, UpdateExercise, RetrieveExercise, ExerciseResponse, ExerciseUpdateResponse

router = APIRouter()

client = MongoClient("mongodb+srv://preetr841:GyfWFDtJVoFldicc@cluster0.e9inxl5.mongodb.net/?appName=Cluster0")
db_exercises = client["ExerciseManagementDatabase"]
exercises_collection = db_exercises["Exercises"]
exercise_updates_collection = db_exercises["ExerciseUpdates"]

@router.post("/create", response_model=ExerciseResponse)
async def create_exercise(exercise: CreateExercise):
    exercise_data = exercise.dict()
    exercise_id = exercises_collection.count_documents({}) + 1
    exercise_data['exerciseID'] = exercise_id
    exercise_data['creationDate'] = datetime.utcnow()
    result = exercises_collection.insert_one(exercise_data)
    if result.inserted_id:
        return ExerciseResponse(**exercise_data)
    raise HTTPException(status_code=500, detail="Exercise creation failed")

@router.put("/update", response_model=ExerciseUpdateResponse)
async def update_exercise(exercise_update: UpdateExercise):
    updated_fields = {
        "exerciseData": exercise_update.exerciseData,
        "creationDate": datetime.utcnow()
    }

    existing_exercise = exercises_collection.find_one({"exerciseID": exercise_update.exerciseID})
    if not existing_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    result = exercises_collection.update_one({"exerciseID": exercise_update.exerciseID}, {"$set": updated_fields})
    if result.modified_count == 1:
        update_id = exercise_updates_collection.count_documents({}) + 1
        update_record = ExerciseUpdate(
            updateID=update_id,
            exerciseID=exercise_update.exerciseID,
            updatedFields=["exerciseData"],
            timestamp=datetime.utcnow()
        )
        exercise_updates_collection.insert_one(update_record.dict())
        return ExerciseUpdateResponse(**update_record.dict())
    raise HTTPException(status_code=500, detail="Failed to update exercise")

@router.get("/retrieve", response_model=List[ExerciseResponse])
async def retrieve_exercise(studentID: int, courseID: int):
    query = {"courseID": courseID}

    exercises = exercises_collection.find(query)
    exercise_list = []
    for exercise in exercises:
        exercise_list.append(ExerciseResponse(
            exerciseID=exercise["exerciseID"],
            courseID=exercise["courseID"],
            teacherID=exercise["teacherID"],
            exerciseData=exercise["exerciseData"],
            creationDate=exercise["creationDate"]
        ))

    if exercise_list:
        return exercise_list
    raise HTTPException(status_code=404, detail="Exercises not found")
