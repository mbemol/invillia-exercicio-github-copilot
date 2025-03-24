"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Atividades Esportivas
    "Swimming Team": {
        "description": "Competitive swimming training and meets",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["alice@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Basketball practice and school tournament preparation",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
    },
    # Atividades Artísticas
    "Art Studio": {
        "description": "Drawing, painting and sculpture workshops",
        "schedule": "Wednesdays, 2:00 PM - 4:00 PM",
        "max_participants": 15,
        "participants": ["maya@mergington.edu"]
    },
    "Theater Group": {
        "description": "Drama classes and school play production",
        "schedule": "Tuesdays and Thursdays, 3:00 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["peter@mergington.edu"]
    },
    # Atividades Intelectuais
    "Debate Team": {
        "description": "Learn argumentation and participate in debate competitions",
        "schedule": "Fridays, 2:30 PM - 4:00 PM",
        "max_participants": 12,
        "participants": ["sarah@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments and science fair projects",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["alex@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specificy activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Validate max participants limit
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity has reached maximum number of participants")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
