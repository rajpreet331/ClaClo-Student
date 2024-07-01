from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from routes import student_profile, course_material, assignment_submission, grades_management, notifications, exercise

app = FastAPI()

# Include routers
app.include_router(student_profile.router, prefix="/student", tags=["Student Profile Management"])
app.include_router(course_material.router, prefix="/course_materials", tags=["Course Materials"])
app.include_router(assignment_submission.router, prefix="/assignments", tags=["Assignment Submission"])
app.include_router(grades_management.router, prefix="/grades", tags=["Grades Management"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
app.include_router(exercise.router, prefix="/exercises", tags=["Exercises Management"])

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
