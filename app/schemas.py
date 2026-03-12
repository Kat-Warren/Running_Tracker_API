from pydantic import BaseModel

class RunCreate(BaseModel):
    title: str
    date: str
    distance_km: float
    duration_minutes: int
    run_type: str
    notes: str | None = None

class RunResponse(RunCreate):
    id: int

    class Config:
        from_attributes = True

class RunUpdate(BaseModel):
    title: str
    date: str
    distance_km: float
    duration_minutes: int
    run_type: str
    notes: str | None = None