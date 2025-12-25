"""Interview scheduling agent using LangChain."""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from app.core.llm import get_llm


class ScheduleRecommendation(BaseModel):
    """Schedule recommendation."""
    recommended_time: str = Field(description="Recommended datetime ISO format")
    reasoning: str = Field(description="Why this time was chosen")
    alternatives: list[str] = Field(description="Alternative time slots")


class SchedulerAgent:
    """Agent for scheduling interviews."""

    def __init__(self):
        self.llm = get_llm()
        self.parser = JsonOutputParser(pydantic_object=ScheduleRecommendation)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intelligent scheduling assistant.

Your task is to recommend optimal interview times considering:
1. Preferred dates provided
2. Standard business hours (9 AM - 5 PM)
3. Buffer time between meetings
4. Time zone considerations

Always suggest times during business hours unless specified otherwise.
Provide alternatives in case the primary recommendation doesn't work.

{format_instructions}"""),
            ("human", """Schedule an interview:

Candidate ID: {candidate_id}
Job ID: {job_id}
Interviewers: {interviewers}
Preferred Dates: {preferred_dates}
Current Time: {current_time}

Recommend the best interview time."""),
        ])

    async def schedule(
        self,
        candidate_id: int,
        job_id: int,
        interviewers: List[str],
        preferred_dates: Optional[List[datetime]] = None,
    ) -> Dict[str, Any]:
        """Schedule an interview."""
        chain = self.prompt | self.llm | self.parser

        preferred_str = "None specified"
        if preferred_dates:
            preferred_str = ", ".join([d.isoformat() for d in preferred_dates])

        result = await chain.ainvoke({
            "candidate_id": candidate_id,
            "job_id": job_id,
            "interviewers": ", ".join(interviewers),
            "preferred_dates": preferred_str,
            "current_time": datetime.now().isoformat(),
            "format_instructions": self.parser.get_format_instructions(),
        })

        try:
            scheduled_at = datetime.fromisoformat(
                result["recommended_time"].replace("Z", "+00:00")
            )
        except ValueError:
            scheduled_at = datetime.now().replace(
                hour=10, minute=0, second=0, microsecond=0
            ) + timedelta(days=1)

        return {
            "candidate_id": candidate_id,
            "job_id": job_id,
            "scheduled_at": scheduled_at,
            "duration_minutes": 60,
            "interview_type": "video",
            "interviewers": interviewers,
            "notes": result["reasoning"],
        }