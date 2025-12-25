"""Resume parsing agent using LangChain."""

import io
from typing import Dict, Any, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from app.core.llm import get_llm


class ParsedResume(BaseModel):
    """Structured resume data."""
    name: str = Field(description="Full name of the candidate")
    email: Optional[str] = Field(description="Email address")
    phone: Optional[str] = Field(description="Phone number")
    summary: Optional[str] = Field(description="Professional summary")
    skills: list[str] = Field(description="List of technical and soft skills")
    experience_years: int = Field(description="Total years of experience")
    education: list[Dict[str, Any]] = Field(description="Education history")
    work_history: list[Dict[str, Any]] = Field(description="Work experience")


class ResumeParserAgent:
    """Agent for parsing and extracting information from resumes."""

    def __init__(self):
        self.llm = get_llm()
        self.parser = JsonOutputParser(pydantic_object=ParsedResume)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert resume parser. Extract structured information from resumes.

Your task is to analyze the resume text and extract:
1. Contact information (name, email, phone)
2. Professional summary
3. Skills (both technical and soft skills)
4. Total years of experience
5. Education history (degree, institution, year)
6. Work history (company, title, duration, responsibilities)

Be thorough and accurate. If information is not present, use null or empty values.

{format_instructions}"""),
            ("human", "Parse this resume:\n\n{resume_text}"),
        ])

    async def parse(self, content: bytes, filename: str) -> Dict[str, Any]:
        """Parse resume content and extract structured data."""
        raw_text = await self._extract_text(content, filename)
        chain = self.prompt | self.llm | self.parser

        result = await chain.ainvoke({
            "resume_text": raw_text,
            "format_instructions": self.parser.get_format_instructions(),
        })

        result["raw_text"] = raw_text
        return result

    async def _extract_text(self, content: bytes, filename: str) -> str:
        """Extract text from various file formats."""
        filename_lower = filename.lower()

        if filename_lower.endswith(".pdf"):
            return await self._extract_from_pdf(content)
        elif filename_lower.endswith(".docx"):
            return await self._extract_from_docx(content)
        elif filename_lower.endswith(".txt"):
            return content.decode("utf-8", errors="ignore")
        else:
            return content.decode("utf-8", errors="ignore")

    async def _extract_from_pdf(self, content: bytes) -> str:
        """Extract text from PDF."""
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error extracting PDF: {e}"

    async def _extract_from_docx(self, content: bytes) -> str:
        """Extract text from DOCX."""
        try:
            from docx import Document
            doc = Document(io.BytesIO(content))
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            return f"Error extracting DOCX: {e}"