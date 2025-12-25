"""Recruitment workflow orchestrator using LangGraph."""

from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from app.agents.resume_parser import ResumeParserAgent
from app.agents.job_matcher import JobMatcherAgent
from app.agents.scheduler import SchedulerAgent


class RecruitmentState(TypedDict):
    """State for the recruitment workflow."""
    messages: Annotated[list, add_messages]
    candidate_data: Dict[str, Any]
    job_data: Dict[str, Any]
    match_result: Dict[str, Any]
    interview_data: Dict[str, Any]
    current_step: str
    error: str | None


class RecruitmentOrchestrator:
    """Orchestrates the full recruitment workflow using LangGraph."""

    def __init__(self):
        self.resume_parser = ResumeParserAgent()
        self.job_matcher = JobMatcherAgent()
        self.scheduler = SchedulerAgent()
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the recruitment workflow graph."""
        workflow = StateGraph(RecruitmentState)

        workflow.add_node("parse_resume", self._parse_resume)
        workflow.add_node("match_job", self._match_job)
        workflow.add_node("schedule_interview", self._schedule_interview)
        workflow.add_node("notify", self._send_notifications)

        workflow.add_edge("parse_resume", "match_job")
        workflow.add_conditional_edges(
            "match_job",
            self._should_schedule,
            {"schedule": "schedule_interview", "reject": END},
        )
        workflow.add_edge("schedule_interview", "notify")
        workflow.add_edge("notify", END)

        workflow.set_entry_point("parse_resume")
        return workflow.compile()

    async def _parse_resume(self, state: RecruitmentState) -> RecruitmentState:
        """Parse the candidate's resume."""
        try:
            resume_content = state.get("resume_content", b"")
            filename = state.get("filename", "resume.pdf")
            parsed = await self.resume_parser.parse(resume_content, filename)
            state["candidate_data"] = parsed
            state["current_step"] = "parsed"
        except Exception as e:
            state["error"] = str(e)
        return state

    async def _match_job(self, state: RecruitmentState) -> RecruitmentState:
        """Match candidate against job requirements."""
        try:
            candidate = state["candidate_data"]
            job = state["job_data"]

            class MockCandidate:
                def __init__(self, data):
                    self.id = data.get("id", 0)
                    self.name = data.get("name", "")
                    self.skills = data.get("skills", [])
                    self.experience_years = data.get("experience_years", 0)
                    self.education = data.get("education", [])
                    self.work_history = data.get("work_history", [])

            class MockJob:
                def __init__(self, data):
                    self.id = data.get("id", 0)
                    self.title = data.get("title", "")
                    self.description = data.get("description", "")
                    self.required_skills = data.get("required_skills", [])
                    self.preferred_skills = data.get("preferred_skills", [])
                    self.experience_min = data.get("experience_min", 0)
                    self.experience_max = data.get("experience_max")
                    self.education_level = data.get("education_level")

            match = await self.job_matcher.match(MockCandidate(candidate), MockJob(job))
            state["match_result"] = match.model_dump()
            state["current_step"] = "matched"
        except Exception as e:
            state["error"] = str(e)
        return state

    def _should_schedule(self, state: RecruitmentState) -> str:
        """Determine if we should schedule an interview."""
        match_result = state.get("match_result", {})
        score = match_result.get("overall_score", 0)
        return "schedule" if score >= 60 else "reject"

    async def _schedule_interview(self, state: RecruitmentState) -> RecruitmentState:
        """Schedule an interview."""
        try:
            candidate = state["candidate_data"]
            job = state["job_data"]
            scheduled = await self.scheduler.schedule(
                candidate_id=candidate.get("id", 0),
                job_id=job.get("id", 0),
                interviewers=["hiring.manager@company.com"],
            )
            state["interview_data"] = scheduled
            state["current_step"] = "scheduled"
        except Exception as e:
            state["error"] = str(e)
        return state

    async def _send_notifications(self, state: RecruitmentState) -> RecruitmentState:
        """Send notifications about the scheduled interview."""
        state["current_step"] = "notified"
        return state

    async def run(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """Run the recruitment workflow."""
        state = RecruitmentState(
            messages=[],
            candidate_data=initial_state.get("candidate_data", {}),
            job_data=initial_state.get("job_data", {}),
            match_result={},
            interview_data={},
            current_step="started",
            error=None,
        )
        final_state = await self.graph.ainvoke(state)
        return dict(final_state)