from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#AI used to setup the database connection
DATABASE_URL = "sqlite:///./runs.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()