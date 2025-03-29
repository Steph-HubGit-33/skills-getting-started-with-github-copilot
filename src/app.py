"""
Système de gestion du lycée

Une application FastAPI très simple qui permet aux étudiants de consulter et de s'inscrire
à des activités extrascolaires au lycée de Mergington.
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
    "Club d'échecs": {
        "description": "Apprenez des stratégies et participez à des tournois d'échecs",
        "horaire": "Vendredis, 15h30 - 17h00",
        "max_participants": 12,
        "participants": ["michael@lesiris.edu", "daniel@lesiris.edu"]
    },
    "Cours de programmation": {
        "description": "Apprenez les bases de la programmation et créez des projets logiciels",
        "horaire": "Mardis et jeudis, 15h30 - 16h30",
        "max_participants": 20,
        "participants": ["emma@lesiris.edu", "sophia@lesiris.edu"]
    },
    "Cours de gym": {
        "description": "Éducation physique et activités sportives",
        "horaire": "Lundis, mercredis, vendredis, 14h00 - 15h00",
        "max_participants": 30,
        "participants": ["john@lesiris.edu", "olivia@lesiris.edu"]
    },
    "Équipe de football": {
        "description": "Rejoignez l'équipe de football de l'école et participez à des matchs",
        "horaire": "Mardis et jeudis, 16h00 - 17h30",
        "max_participants": 22,
        "participants": ["liam@lesiris.edu", "noah@lesiris.edu"]
    },
    "Équipe de basketball": {
        "description": "Entraînez-vous et participez à des tournois de basketball",
        "horaire": "Mercredis et vendredis, 15h30 - 17h00",
        "max_participants": 15,
        "participants": ["ava@lesiris.edu", "mia@lesiris.edu"]
    },
    "Club d'art": {
        "description": "Explorez diverses techniques artistiques et créez des chefs-d'œuvre",
        "horaire": "Jeudis, 15h30 - 17h00",
        "max_participants": 15,
        "participants": ["amelia@lesiris.edu", "harper@lesiris.edu"]
    },
    "Club de théâtre": {
        "description": "Jouez, mettez en scène et produisez des pièces et des spectacles",
        "horaire": "Lundis et mercredis, 16h00 - 17h30",
        "max_participants": 20,
        "participants": ["elijah@lesiris.edu", "isabella@lesiris.edu"]
    },
    "Club de mathématiques": {
        "description": "Résolvez des problèmes complexes et participez à des compétitions de mathématiques",
        "horaire": "Mardis, 15h30 - 16h30",
        "max_participants": 10,
        "participants": ["lucas@lesiris.edu", "charlotte@lesiris.edu"]
    },
    "Club de sciences": {
        "description": "Réalisez des expériences et explorez des concepts scientifiques",
        "horaire": "Vendredis, 15h30 - 17h00",
        "max_participants": 12,
        "participants": ["henry@lesiris.edu", "evelyn@lesiris.edu"]
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
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}", "participants": activity["participants"]}

