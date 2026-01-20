import os
from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from models import CareerResponse

load_dotenv()

# Create model (NO base_url here)
model = OpenAIModel(
    model_name=os.getenv("OPENAI_MODEL", "meta-llama/llama-3.1-8b-instruct")
)

career_agent = Agent(
    model=model,
    system_prompt="""
You are a professional career preparation AI.

Analyze resumes for a given job role.
Give practical, actionable, and honest advice.
Return clear structured feedback.
"""
)
