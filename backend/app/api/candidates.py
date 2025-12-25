"""Candidate API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from app.models.candidate import Candidate, CandidateCreate, CandidateResponse, CandidateMatch
from app.agents.resume_parser import ResumeParserAgent
from app.agents.job_matcher import JobMatcherAgent

router = APIRouter()


@router.post("", response_model=CandidateResponse)
async def create_candidate(
    candidate: CandidateCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new candidate."""
    db_candidate = Candidate(**candidate.model_dump())
    session.add(db_candidate)
    await session.commit()
    await session.refresh(db_candidate)
    return db_candidate


@router.post("/upload", response_model=CandidateResponse)
async def upload_resume(
    file: UploadFile = File(...),
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    session: AsyncSession = Depends(get_session),
):
    """Upload and parse a resume."""
    content = await file.read()
    parser = ResumeParserAgent()
    parsed_data = await parser.parse(content, file.filename)

    candidate_data = {
        "name": name or parsed_data.get("name", "Unknown"),
        "email": email or parsed_data.get("email", "unknown@example.com"),
        "phone": parsed_data.get("phone"),
        "resume_text": parsed_data.get("raw_text", ""),
        "skills": parsed_data.get("skills", []),
        "experience_years": parsed_data.get("experience_years", 0),
        "education": parsed_data.get("education", []),
        "work_history": parsed_data.get("work_history", []),
        "parsed_data": parsed_data,
    }

    db_candidate = Candidate(**candidate_data)
    session.add(db_candidate)
    await session.commit()
    await session.refresh(db_candidate)
    return db_candidate


@router.get("", response_model=List[CandidateResponse])
async def list_candidates(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    """List all candidates."""
    query = select(Candidate)
    if status:
        query = query.where(Candidate.status == status)
    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Get a specific candidate."""
    result = await session.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@router.post("/{candidate_id}/match/{job_id}", response_model=CandidateMatch)
async def match_candidate_to_job(
    candidate_id: int,
    job_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Match a candidate against a job posting."""
    from app.models.job import Job

    result = await session.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    result = await session.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    matcher = JobMatcherAgent()
    match_result = await matcher.match(candidate, job)
    return match_result


@router.delete("/{candidate_id}")
async def delete_candidate(
    candidate_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Delete a candidate."""
    result = await session.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    await session.delete(candidate)
    await session.commit()
    return {"message": "Candidate deleted"}