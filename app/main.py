from fastapi import FastAPI, Depends, HTTPException
from app.database import engine
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models,schemas
from datetime import datetime

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_age_group(age: int) -> tuple[int, int]:
    if age <= 19:
        return (16, 19)
    elif age <= 24:
        return (20, 24)
    elif age <= 29:
        return (25, 29)
    elif age <= 34:
        return (30, 34)
    elif age <= 39:
        return (35, 39)
    else:
        return (40, 100)

def time_to_seconds(time_str: str) -> float:
    parts = time_str.split(":")
    if len(parts) == 3:
        hours = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    return 0.0


def get_event_from_distance(distance_km: float) -> str | None:
    if abs(distance_km - 0.8) < 0.05:
        return "800 m"
    elif abs(distance_km - 1.5) < 0.1:
        return "1500 m"
    elif abs(distance_km - 5.0) < 0.2:
        return "5000 m"
    elif abs(distance_km - 10.0) < 0.3:
        return "10000 m"
    return None


@app.get("/")
def serve_homepage():
    return FileResponse("static/index.html")

@app.post("/runs", response_model=schemas.RunResponse)
def create_run(run: schemas.RunCreate, db: Session = Depends(get_db)):
    db_run = models.Run(
        title=run.title,
        date=run.date,
        distance_km=run.distance_km,
        duration_minutes=run.duration_minutes,
        run_type=run.run_type,
        notes=run.notes,
        gender=run.gender,
        age=run.age
    )
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run

@app.get("/runs", response_model=list[schemas.RunResponse])
def get_runs(db: Session = Depends(get_db)):
    return db.query(models.Run).all()

@app.get("/runs/{run_id}", response_model=schemas.RunResponse)
def get_run(run_id: int, db: Session = Depends(get_db)):
    run = db.query(models.Run).filter(models.Run.id == run_id).first()
    
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    
    return run

@app.delete("/runs/{run_id}")
def delete_run(run_id: int, db: Session = Depends(get_db)):
    run = db.query(models.Run).filter(models.Run.id == run_id).first()

    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    db.delete(run)
    db.commit()

    return {"message": "Run deleted successfully"}

@app.put("/runs/{run_id}", response_model=schemas.RunResponse)
def update_run(run_id: int, updated_run: schemas.RunUpdate, db: Session = Depends(get_db)):
    run = db.query(models.Run).filter(models.Run.id == run_id).first()

    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    run.title = updated_run.title
    run.date = updated_run.date
    run.distance_km = updated_run.distance_km
    run.duration_minutes = updated_run.duration_minutes
    run.run_type = updated_run.run_type
    run.notes = updated_run.notes

    db.commit()
    db.refresh(run)

    return run

@app.get("/performances")
def get_performances(db: Session = Depends(get_db)):
    return db.query(models.Performance).all()

# REFERANCES: Code adapted from ChatGPT to compare runs
# https://chatgpt.com/share/69b55fd5-74fc-8002-a205-bf1b40a41d48
@app.get("/compare/{run_id}")
def compare_run(run_id: int, db: Session = Depends(get_db)):
    run = db.query(models.Run).filter(models.Run.id == run_id).first()

    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    if run.age is None or run.gender is None:
        raise HTTPException(status_code=400, detail="Run must include age and gender")

    matched_event = get_event_from_distance(run.distance_km)
    if matched_event is None:
        raise HTTPException(status_code=400, detail="No matching event for this run distance")

    min_age, max_age = get_age_group(run.age)

    performances = db.query(models.Performance).filter(
        models.Performance.gender == run.gender,
        models.Performance.event == matched_event
    ).all()

    matching_performances = []

    for performance in performances:
        try:
            dob = datetime.strptime(performance.date_of_birth, "%Y-%m-%d")
            perf_date = datetime.strptime(performance.date, "%Y-%m-%d")
            athlete_age = perf_date.year - dob.year - ((perf_date.month, perf_date.day) < (dob.month, dob.day))

            if min_age <= athlete_age <= max_age:
                matching_performances.append(performance)
        except:
            continue

    if not matching_performances:
        raise HTTPException(status_code=404, detail="No matching elite performance found")

    best_performance = min(matching_performances, key=lambda p: time_to_seconds(p.time))

    user_time_seconds = run.duration_minutes * 60
    elite_time_seconds = time_to_seconds(best_performance.time)
    percentage_of_elite = round((elite_time_seconds / user_time_seconds) * 100, 2)

    return {
        "run_id": run.id,
        "run_title": run.title,
        "user_gender": run.gender,
        "user_age": run.age,
        "age_group": f"{min_age}-{max_age}",
        "matched_event": matched_event,
        "user_time_seconds": user_time_seconds,
        "elite_time_seconds": elite_time_seconds,
        "elite_time_original": best_performance.time,
        "elite_name": best_performance.name,
        "elite_country": best_performance.country,
        "elite_city": best_performance.city,
        "elite_date": best_performance.date,
        "percentage_of_elite": percentage_of_elite
    }
