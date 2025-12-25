"""API endpoint tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Smart Recruiter Agent"


@pytest.mark.asyncio
async def test_create_candidate(client: AsyncClient):
    candidate_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
    }
    response = await client.post("/api/candidates", json=candidate_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"


@pytest.mark.asyncio
async def test_create_job(client: AsyncClient):
    job_data = {
        "title": "Software Engineer",
        "description": "We are looking for a talented software engineer.",
        "required_skills": ["Python", "FastAPI"],
        "experience_min": 3,
    }
    response = await client.post("/api/jobs", json=job_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Software Engineer"