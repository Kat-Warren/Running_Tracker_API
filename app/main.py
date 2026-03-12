from fastapi import FastAPI, Depends, HTTPException
from app.database import engine
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models,schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        notes=run.notes
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