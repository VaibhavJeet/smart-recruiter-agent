"""Job API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.models.job import Job, JobCreate, JobResponse
from app.models.candidate import Candidate, CandidateMatch
from app.agents.job_matcher import JobMatcherAgent

router = APIRouter()


@router.post("", response_model=JobResponse)
async def create_job(
    job: JobCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new job posting."""
    db_job = Job(**job.model_dump())
    session.add(db_job)
    await session.commit()
    await session.refresh(db_job)
    return db_job


@router.get("", response_model=List[JobResponse])
async def list_jobs(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    """List all jobs."""
    query = select(Job)
    if status:
        query = query.where(Job.status == status)
    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get a specific job."""
    result = await session.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/{job_id}/candidates", response_model=List[CandidateMatch])
async def get_matched_candidates(
    job_id: int,
    min_score: float = 50.0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session),
):
    """Get candidates matched to a job, ranked by score."""
    result = await session.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    result = await session.execute(select(Candidate))
    candidates = result.scalars().all()

    matcher = JobMatcherAgent()
    matches = []
    for candidate in candidates:
        match = await matcher.match(candidate, job)
        if match.overall_score >= min_score:
            matches.append(match)

    matches.sort(key=lambda x: x.overall_score, reverse=True)
    return matches[:limit]


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_update: JobCreate,
    session: AsyncSession = Depends(get_session),
):
    """Update a job posting."""
    result = await session.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    for key, value in job_update.model_dump().items():
        setattr(job, key, value)

    await session.commit()
    await session.refresh(job)
    return job


@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Delete a job posting."""
    result = await session.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    await session.delete(job)
    await session.commit()
    return {"message": "Job deleted"}