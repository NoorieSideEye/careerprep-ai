from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import career_agent
import logging
import os

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="CareerPrep AI")

class AnalyzeRequest(BaseModel):
    role: str
    resume_text: str

@app.get("/")
def serve_ui():
    return FileResponse("frontend/index.html")

@app.post("/analyze")
def analyze_resume(req: AnalyzeRequest):
    try:
        result = career_agent.run_sync(
            f"""
Target Role: {req.role}

Resume:
{req.resume_text}
"""
        )
        return {"output": result.output}
    except Exception as e:
        logging.exception("AI processing failed")
        raise HTTPException(status_code=500, detail=str(e))
