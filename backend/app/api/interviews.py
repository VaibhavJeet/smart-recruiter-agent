"""Interview API endpoints."""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.models.interview import Interview, InterviewCreate, InterviewResponse, InterviewUpdate
from app.agents.scheduler import SchedulerAgent

router = APIRouter()


@router.post("", response_model=InterviewResponse)
async def create_interview(
    interview: InterviewCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new interview."""
    db_interview = Interview(**interview.model_dump())
    session.add(db_interview)
    await session.commit()
    await session.refresh(db_interview)
    return db_interview


@router.post("/schedule", response_model=InterviewResponse)
async def schedule_interview(
    candidate_id: int,
    job_id: int,
    interviewers: List[str],
    preferred_dates: Optional[List[datetime]] = None,
    session: AsyncSession = Depends(get_session),
):
    """Automatically schedule an interview."""
    scheduler = SchedulerAgent()
    scheduled = await scheduler.schedule(
        candidate_id=candidate_id,
        job_id=job_id,
        interviewers=interviewers,
        preferred_dates=preferred_dates,
    )

    db_interview = Interview(**scheduled)
    session.add(db_interview)
    await session.commit()
    await session.refresh(db_interview)
    return db_interview


@router.get("", response_model=List[InterviewResponse])
async def list_interviews(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    candidate_id: Optional[int] = None,
    job_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
):
    """List all interviews."""
    query = select(Interview)
    if status:
        query = query.where(Interview.status == status)
    if candidate_id:
        query = query.where(Interview.candidate_id == candidate_id)
    if job_id:
        query = query.where(Interview.job_id == job_id)
    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{interview_id}", response_model=InterviewResponse)
async def get_interview(
    interview_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get a specific interview."""
    result = await session.execute(
        select(Interview).where(Interview.id == interview_id)
    )
    interview = result.scalar_one_or_none()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview


@router.patch("/{interview_id}", response_model=InterviewResponse)
async def update_interview(
    interview_id: int,
    update: InterviewUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Update an interview."""
    result = await session.execute(
        select(Interview).where(Interview.id == interview_id)
    )
    interview = result.scalar_one_or_none()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(interview, key, value)

    await session.commit()
    await session.refresh(interview)
    return interview


@router.delete("/{interview_id}")
async def delete_interview(
    interview_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Delete an interview."""
    result = await session.execute(
        select(Interview).where(Interview.id == interview_id)
    )
    interview = result.scalar_one_or_none()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    await session.delete(interview)
    await session.commit()
    return {"message": "Interview deleted"}