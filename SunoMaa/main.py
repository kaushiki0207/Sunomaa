from fastapi import FastAPI, Depends, Form
from sqlalchemy.orm import Session
import json
from database import engine, SessionLocal
import models
from gemini_service import analyze_symptoms
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request



app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Create tables
models.Base.metadata.create_all(bind=engine)

# ---------------- DB Dependency ---------------- #

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Home ---------------- #

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


# ---------------- Symptom Submission ---------------- #

@app.post("/submit-symptoms", response_class=HTMLResponse)
def submit_symptoms(
    request: Request,
    age: int = Form(...),
    hot_flashes: str = Form(...),
    mood_swings: str = Form(...),
    chest_pain: str = Form(...),
    sleep_issue: str = Form(...),
    irregular_period: str = Form(...),
    db: Session = Depends(get_db)
):

    symptom_data = {
        "age": age,
        "hot_flashes": hot_flashes.lower() == "true",
        "mood_swings": mood_swings.lower() == "true",
        "chest_pain": chest_pain.lower() == "true",
        "sleep_issue": sleep_issue.lower() == "true",
        "irregular_period": irregular_period.lower() == "true",
    }
    ai_result = analyze_symptoms(symptom_data)

    symptom = models.Symptom(
    age=age,
    hot_flashes=symptom_data["hot_flashes"],
    mood_swings=symptom_data["mood_swings"],
    chest_pain=symptom_data["chest_pain"],
    sleep_issue=symptom_data["sleep_issue"],
    irregular_period=symptom_data["irregular_period"],
    ai_advice=json.dumps(ai_result)   # store JSON properly
)

    db.add(symptom)
    db.commit()

    return templates.TemplateResponse(
        request,
        "index.html",
        {"result": ai_result},
    )


@app.get("/history", response_class=HTMLResponse)
def history_page(request: Request, db: Session = Depends(get_db)):
    records = db.query(models.Symptom).order_by(models.Symptom.id.desc()).all()

    return templates.TemplateResponse(
        request,
        "history.html",
        {"records": records},
    )

