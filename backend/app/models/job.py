"""Job models."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class Job(Base):
    """Job database model."""

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    department = Column(String(100), nullable=True)
    location = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    requirements = Column(JSON, default=list)
    required_skills = Column(JSON, default=list)
    preferred_skills = Column(JSON, default=list)
    experience_min = Column(Integer, default=0)
    experience_max = Column(Integer, nullable=True)
    education_level = Column(String(50), nullable=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    status = Column(String(50), default="open")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class JobCreate(BaseModel):
    """Job creation schema."""
    title: str = Field(..., min_length=1, max_length=255)
    department: Optional[str] = None
    location: Optional[str] = None
    description: str = Field(..., min_length=10)
    requirements: List[str] = []
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    experience_min: int = 0
    experience_max: Optional[int] = None
    education_level: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None


class JobResponse(BaseModel):
    """Job response schema."""
    id: int
    title: str
    department: Optional[str] = None
    location: Optional[str] = None
    description: str
    requirements: List[str] = []
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    experience_min: int = 0
    experience_max: Optional[int] = None
    education_level: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    status: str = "open"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True