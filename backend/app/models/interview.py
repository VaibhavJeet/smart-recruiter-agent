"""Interview models."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class Interview(Base):
    """Interview database model."""

    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    interview_type = Column(String(50), default="video")
    interviewers = Column(JSON, default=list)
    location = Column(String(255), nullable=True)
    meeting_link = Column(String(500), nullable=True)
    notes = Column(String(1000), nullable=True)
    status = Column(String(50), default="scheduled")
    feedback = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class InterviewCreate(BaseModel):
    """Interview creation schema."""
    candidate_id: int
    job_id: int
    scheduled_at: datetime
    duration_minutes: int = 60
    interview_type: str = "video"
    interviewers: List[str] = []
    location: Optional[str] = None
    meeting_link: Optional[str] = None
    notes: Optional[str] = None


class InterviewResponse(BaseModel):
    """Interview response schema."""
    id: int
    candidate_id: int
    job_id: int
    scheduled_at: datetime
    duration_minutes: int
    interview_type: str
    interviewers: List[str] = []
    location: Optional[str] = None
    meeting_link: Optional[str] = None
    notes: Optional[str] = None
    status: str
    feedback: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InterviewUpdate(BaseModel):
    """Interview update schema."""
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    interview_type: Optional[str] = None
    interviewers: Optional[List[str]] = None
    location: Optional[str] = None
    meeting_link: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    feedback: Optional[dict] = None