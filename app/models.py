from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    date = Column(String)
    distance_km = Column(Float)
    duration_minutes = Column(Integer)
    run_type = Column(String)
    notes = Column(String, nullable=True)