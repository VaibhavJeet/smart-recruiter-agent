"""Resume processing tools for LangChain."""

from typing import List, Dict, Any
from langchain_core.tools import tool


@tool
def extract_skills_tool(text: str) -> List[str]:
    """Extract skills from resume text.

    Args:
        text: Resume text content

    Returns:
        List of extracted skills
    """
    common_skills = [
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
        "react", "angular", "vue", "node.js", "django", "flask", "fastapi",
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
        "sql", "postgresql", "mysql", "mongodb", "redis",
        "git", "ci/cd", "agile", "scrum",
        "machine learning", "deep learning", "nlp", "computer vision",
        "data analysis", "data science", "statistics",
    ]

    text_lower = text.lower()
    found_skills = [skill for skill in common_skills if skill in text_lower]
    return found_skills


@tool
def calculate_experience_tool(work_history: List[Dict[str, Any]]) -> int:
    """Calculate total years of experience from work history.

    Args:
        work_history: List of work experience entries

    Returns:
        Total years of experience
    """
    total_years = 0
    for job in work_history:
        duration = job.get("duration_years", 0)
        if isinstance(duration, (int, float)):
            total_years += duration
    return int(total_years)


@tool
def normalize_education_tool(education_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize education entries to standard format.

    Args:
        education_entries: Raw education data

    Returns:
        Normalized education entries
    """
    degree_levels = {
        "phd": 5, "doctorate": 5,
        "master": 4, "mba": 4,
        "bachelor": 3,
        "associate": 2,
        "diploma": 1, "certificate": 1,
    }

    normalized = []
    for entry in education_entries:
        degree = entry.get("degree", "").lower()
        level = 0
        for key, value in degree_levels.items():
            if key in degree:
                level = value
                break

        normalized.append({
            "degree": entry.get("degree", "Unknown"),
            "institution": entry.get("institution", "Unknown"),
            "year": entry.get("year"),
            "field": entry.get("field", ""),
            "level": level,
        })

    normalized.sort(key=lambda x: x["level"], reverse=True)
    return normalized