from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import career_agent
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="CareerPrep AI")

class AnalyzeRequest(BaseModel):
    role: str
    resume_text: str

@app.post("/analyze")
def analyze_resume(req: AnalyzeRequest):
    try:
        prompt = f"""
Target Role: {req.role}

Resume:
{req.resume_text}
"""
        result = career_agent.run_sync(prompt)
        return result
    except Exception as e:
        logging.exception("AI processing failed")
        raise HTTPException(status_code=500, detail=str(e))
