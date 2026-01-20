from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agent import career_agent
import logging
import os

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="CareerPrep AI",
    version="0.1.0",
)

# ---------- FRONTEND ----------

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)

# ---------- API ----------

class AnalyzeRequest(BaseModel):
    role: str
    resume_text: str

@app.post("/analyze")
def analyze_resume(req: AnalyzeRequest):
    try:
        result = career_agent.run_sync(
            f"""
You are a professional career preparation AI.

Target Role:
{req.role}

Resume:
{req.resume_text}

Give clear, structured, actionable feedback with:
- Strengths
- Gaps
- Improvements
- Final summary
"""
        )

        # ✅ CORRECT + SAFE OUTPUT EXTRACTION
        if hasattr(result, "output_text") and result.output_text:
            analysis = result.output_text
        elif hasattr(result, "output") and result.output:
            analysis = str(result.output)
        else:
            analysis = str(result)

        return {
            "analysis": analysis
        }

    except Exception as e:
        logging.exception("AI processing failed")
        raise HTTPException(status_code=500, detail=str(e))
