from pydantic import BaseModel
from typing import List

class SkillGap(BaseModel):
    skill: str
    current_level: str
    required_level: str
    suggestion: str

class CareerResponse(BaseModel):
    role: str
    strengths: List[str]
    missing_skills: List[SkillGap]
    resume_improvements: List[str]
    interview_questions: List[str]
    learning_roadmap: List[str]
