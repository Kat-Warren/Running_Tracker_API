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
    gender = Column(String, nullable=True)
    age = Column(Integer, nullable=True)

# REFERANCE: CHAT GPT adapted code 
# https://chatgpt.com/share/69b54fb1-2280-8002-a596-48be67cd2803
class Performance(Base):
    __tablename__ = "performances"

    id = Column(Integer, primary_key=True, index=True)
    rank = Column(Integer)
    time = Column(String, nullable=False)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False)
    place = Column(Integer)
    city = Column(String)
    date = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    event = Column(String, nullable=False)