import json
import os

from google import genai
from google.genai import types
from pydantic import BaseModel

MODEL = "gemini-3.6-flash"

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "match_score": {
            "type": "integer",
            "description": "Overall match between the resume and job description, 0-100.",
        },
        "matched_skills": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Skills/requirements from the job description that the resume demonstrates.",
        },
        "unmatched_skills": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Skills/requirements from the job description that the resume does not demonstrate.",
        },
        "summary": {
            "type": "string",
            "description": "A short (2-4 sentence) summary of the candidate's fit for the role.",
        },
        "tailored_suggestions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": (
                            "Short label for the type of fix, e.g. 'Missing Keyword', "
                            "'Quantify Achievement', 'Action Verb', 'Formatting'."
                        ),
                    },
                    "issue": {
                        "type": "string",
                        "description": "The specific gap in the resume relative to the job description or ATS findings.",
                    },
                    "suggestion": {
                        "type": "string",
                        "description": "A concrete, actionable edit the candidate should make.",
                    },
                    "example": {
                        "type": "string",
                        "description": (
                            "A short before/after or ready-to-use example the candidate "
                            "could drop into their resume, grounded in their actual experience."
                        ),
                    },
                },
                "required": ["category", "issue", "suggestion", "example"],
            },
            "description": (
                "3-6 specific, actionable edits to improve the resume's ATS score and "
                "match rate for this job description, ranked by likely impact."
            ),
        },
    },
    "required": [
        "match_score",
        "matched_skills",
        "unmatched_skills",
        "summary",
        "tailored_suggestions",
    ],
}

SYSTEM_PROMPT = """You are a resume-to-job-description matching evaluator and ATS \
(Applicant Tracking System) optimization coach. Given a candidate's resume text, a \
job description, and a set of automated ATS findings about the resume, assess fit \
and recommend concrete improvements.

Guidelines:
- Base match_score primarily on overlap between the candidate's demonstrated \
skills/experience and the job description's requirements. Weigh explicitly \
required qualifications more heavily than "nice to have" ones.
- matched_skills should list specific skills, technologies, or qualifications \
from the job description that the resume evidences (not generic traits).
- unmatched_skills should list specific requirements from the job description \
that the resume does not evidence.
- Do not invent skills that appear in neither document.
- summary should briefly explain the score in plain language.
- tailored_suggestions must be specific and actionable, grounded in both the \
missing keywords (unmatched_skills) and the provided ATS findings (e.g. missing \
sections, low quantified-achievement ratio, weak action verbs, tables/images/\
header-footer issues). Do not suggest fixes for things the ATS findings say are \
already fine. Each suggestion's example should be concrete and usable, written \
from the candidate's actual resume content wherever possible (not generic \
filler). Order suggestions by likely impact on both ATS score and human \
readability."""


class GeminiAnalysis(BaseModel):
    match_score: int
    matched_skills: list[str]
    unmatched_skills: list[str]
    summary: str
    tailored_suggestions: list[dict]


def analyze_resume(
    resume_text: str, job_description: str, ats_findings_summary: str
) -> GeminiAnalysis:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

    client = genai.Client(api_key=api_key)

    user_message = (
        f"## Job Description\n{job_description}\n\n"
        f"## Resume\n{resume_text}\n\n"
        f"## Automated ATS Findings\n{ats_findings_summary}"
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=RESPONSE_SCHEMA,
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel.LOW
            ),
        ),
    )

    data = json.loads(response.text)
    return GeminiAnalysis(**data)
