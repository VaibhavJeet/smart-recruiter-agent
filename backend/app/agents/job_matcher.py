"""Job matching agent using LangChain."""

from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from app.core.llm import get_llm
from app.models.candidate import CandidateMatch


class MatchAnalysis(BaseModel):
    """Match analysis result."""
    overall_score: float = Field(description="Overall match score 0-100")
    skill_match: float = Field(description="Skills match score 0-100")
    experience_match: float = Field(description="Experience match score 0-100")
    education_match: float = Field(description="Education match score 0-100")
    reasoning: str = Field(description="Detailed reasoning for the scores")
    gaps: list[str] = Field(description="Skills or requirements the candidate lacks")
    strengths: list[str] = Field(description="Candidate's notable strengths for this role")


class JobMatcherAgent:
    """Agent for matching candidates to job requirements."""

    def __init__(self):
        self.llm = get_llm()
        self.parser = JsonOutputParser(pydantic_object=MatchAnalysis)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert recruiter analyzing candidate-job fit.

Analyze the match between a candidate and a job posting. Consider:
1. Skills match - how well the candidate's skills align with requirements
2. Experience match - years of experience and relevance
3. Education match - education level and field relevance
4. Overall fit - combining all factors

Be fair and objective. Provide specific reasoning for your scores.

{format_instructions}"""),
            ("human", """Analyze this candidate-job match:

## JOB POSTING
Title: {job_title}
Description: {job_description}
Required Skills: {required_skills}
Preferred Skills: {preferred_skills}
Experience Required: {experience_required}
Education: {education_required}

## CANDIDATE
Name: {candidate_name}
Skills: {candidate_skills}
Experience: {candidate_experience} years
Education: {candidate_education}
Work History: {work_history}

Provide a detailed match analysis."""),
        ])

    async def match(self, candidate, job) -> CandidateMatch:
        """Match a candidate against a job posting."""
        chain = self.prompt | self.llm | self.parser

        result = await chain.ainvoke({
            "job_title": job.title,
            "job_description": job.description,
            "required_skills": ", ".join(job.required_skills or []),
            "preferred_skills": ", ".join(job.preferred_skills or []),
            "experience_required": f"{job.experience_min}-{job.experience_max or 'any'} years",
            "education_required": job.education_level or "Not specified",
            "candidate_name": candidate.name,
            "candidate_skills": ", ".join(candidate.skills or []),
            "candidate_experience": candidate.experience_years or 0,
            "candidate_education": str(candidate.education or []),
            "work_history": str(candidate.work_history or []),
            "format_instructions": self.parser.get_format_instructions(),
        })

        return CandidateMatch(
            candidate_id=candidate.id,
            job_id=job.id,
            overall_score=result["overall_score"],
            skill_match=result["skill_match"],
            experience_match=result["experience_match"],
            education_match=result["education_match"],
            reasoning=result["reasoning"],
            gaps=result["gaps"],
            strengths=result["strengths"],
        )