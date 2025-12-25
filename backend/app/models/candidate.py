"""Candidate models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class Candidate(Base):
    """Candidate database model."""

    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    resume_text = Column(Text, nullable=True)
    skills = Column(JSON, default=list)
    experience_years = Column(Integer, default=0)
    education = Column(JSON, default=list)
    work_history = Column(JSON, default=list)
    parsed_data = Column(JSON, default=dict)
    status = Column(String(50), default="new")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class CandidateCreate(BaseModel):
    """Candidate creation schema."""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = None
    resume_text: Optional[str] = None


class CandidateResponse(BaseModel):
    """Candidate response schema."""
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    skills: List[str] = []
    experience_years: int = 0
    education: List[Dict[str, Any]] = []
    work_history: List[Dict[str, Any]] = []
    status: str = "new"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CandidateMatch(BaseModel):
    """Candidate-job match result."""
    candidate_id: int
    job_id: int
    overall_score: float = Field(..., ge=0, le=100)
    skill_match: float = Field(..., ge=0, le=100)
    experience_match: float = Field(..., ge=0, le=100)
    education_match: float = Field(..., ge=0, le=100)
    reasoning: str
    gaps: List[str] = []
    strengths: List[str] = []