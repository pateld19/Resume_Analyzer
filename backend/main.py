import os

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google.genai import errors as genai_errors

import ats_checker
from gemini_client import analyze_resume
from schemas import AnalysisResponse
from text_extraction import EmptyTextError, UnsupportedFileTypeError, extract_text

load_dotenv()

app = FastAPI(title="Resume Analyzer API")

allowed_origins = [
    origin.strip()
    for origin in os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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

    findings = ats_checker.gather_findings(resume.filename or "", content, resume_text)

    try:
        gemini_analysis = analyze_resume(
            resume_text, job_description, findings.summary_for_prompt()
        )
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

    ats_report = ats_checker.build_report(
        findings, gemini_analysis.matched_skills, gemini_analysis.unmatched_skills
    )

    return AnalysisResponse(
        match_score=gemini_analysis.match_score,
        matched_skills=gemini_analysis.matched_skills,
        unmatched_skills=gemini_analysis.unmatched_skills,
        summary=gemini_analysis.summary,
        ats_report=ats_report,
        tailored_suggestions=gemini_analysis.tailored_suggestions,
    )
