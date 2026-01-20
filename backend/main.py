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
            f"Target Role: {req.role}\n\nResume:\n{req.resume_text}"
        )

        # ✅ THIS IS THE FIX
        return {
            "analysis": result.output
        }

    except Exception as e:
        logging.exception("AI processing failed")
        raise HTTPException(status_code=500, detail=str(e))
