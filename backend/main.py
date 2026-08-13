from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google.genai import errors as genai_errors

from gemini_client import analyze_resume
from schemas import AnalysisResponse
from text_extraction import EmptyTextError, UnsupportedFileTypeError, extract_text

load_dotenv()

app = FastAPI(title="Resume Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
) -> AnalysisResponse:
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    content = await resume.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded resume file is empty.")

    try:
        resume_text = extract_text(resume.filename or "", content)
    except (UnsupportedFileTypeError, EmptyTextError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        return analyze_resume(resume_text, job_description)
    except genai_errors.ClientError as exc:
        status_code = 429 if exc.code == 429 else 400
        detail = (
            "Rate limited by Gemini API. Please try again shortly."
            if exc.code == 429
            else f"Gemini API rejected the request: {exc.message}"
        )
        raise HTTPException(status_code=status_code, detail=detail) from exc
    except genai_errors.ServerError as exc:
        raise HTTPException(
            status_code=502, detail=f"Gemini API error: {exc.message}"
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
