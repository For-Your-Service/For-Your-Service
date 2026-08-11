"""SQLAlchemy models."""
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True)
    candidate_id = Column(String, unique=True, nullable=False)
    resume_text = Column(String)
    skills = Column(JSON)
    embedding = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True)
    job_id = Column(String, unique=True, nullable=False)
    title = Column(String)
    description = Column(String)
    required_skills = Column(JSON)
    embedding = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True)
    candidate_id = Column(String, nullable=False)
    job_id = Column(String, nullable=False)
    score = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
