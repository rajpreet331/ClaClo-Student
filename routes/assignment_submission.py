from fastapi import APIRouter, HTTPException, Query
from pymongo import MongoClient
from datetime import datetime

from models.assignment_submission import Assignment, Submission, SubmissionUpdate
from schemas.assignment_submission import AssignmentSubmission, AssignmentSubmissionUpdate, AssignmentSubmissionRetrieve, AssignmentResponse, SubmissionResponse, SubmissionUpdateResponse

router = APIRouter()

client = MongoClient("mongodb+srv://preetr841:GyfWFDtJVoFldicc@cluster0.e9inxl5.mongodb.net/?appName=Cluster0")
db_assignments = client["AssignmentSubmissionDatabase"]
assignments = db_assignments["Assignments"]
submissions = db_assignments["Submissions"]
submission_updates = db_assignments["SubmissionUpdates"]

@router.post("/submit", response_model=SubmissionResponse)
async def submit_assignment(submission: AssignmentSubmission):
    submission_data = submission.dict()
    submission_data["submissionID"] = submissions.count_documents({}) + 1
    new_submission = Submission(**submission_data)
    result = submissions.insert_one(new_submission.dict())
    if result.inserted_id:
        return SubmissionResponse(**new_submission.dict())
    raise HTTPException(status_code=500, detail="Assignment submission failed")

@router.put("/update", response_model=SubmissionUpdateResponse)
async def update_submission(submission_update: AssignmentSubmissionUpdate):
    updated_fields = {
        "submissionData": submission_update.submissionData,
        "submissionDate": datetime.utcnow()
    }

    result = submissions.update_one({"submissionID": submission_update.submissionID, "studentID": submission_update.studentID}, {"$set": updated_fields})
    if result.modified_count == 1:
        update_id = submission_updates.count_documents({}) + 1
        update_record = SubmissionUpdate(
            updateID=update_id,
            submissionID=submission_update.submissionID,
            updatedFields=["submissionData"]
        )
        submission_updates.insert_one(update_record.dict())
        return SubmissionUpdateResponse(**update_record.dict())
    raise HTTPException(status_code=404, detail="Submission not found or update not authorized")

@router.get("/retrieve", response_model=SubmissionResponse)
async def retrieve_submission(
    studentID: int = Query(None, description="Student ID"),
    assignmentID: int = Query(None, description="Assignment ID")
):
    query = {}
    if studentID is not None:
        query["studentID"] = studentID
    if assignmentID is not None:
        query["assignmentID"] = assignmentID

    submission = submissions.find_one(query)
    if submission:
        return SubmissionResponse(**submission)
    
    raise HTTPException(status_code=404, detail="Submission not found")
