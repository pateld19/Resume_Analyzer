import json
import os

from google import genai

from schemas import AnalysisResponse

MODEL = "gemini-flash-latest"

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
    },
    "required": ["match_score", "matched_skills", "unmatched_skills", "summary"],
}

SYSTEM_PROMPT = """You are a resume-to-job-description matching evaluator. \
Given a candidate's resume text and a job description, assess how well the \
candidate matches the role.

Guidelines:
- Base match_score primarily on overlap between the candidate's demonstrated \
skills/experience and the job description's requirements. Weigh explicitly \
required qualifications more heavily than "nice to have" ones.
- matched_skills should list specific skills, technologies, or qualifications \
from the job description that the resume evidences (not generic traits).
- unmatched_skills should list specific requirements from the job description \
that the resume does not evidence.
- Do not invent skills that appear in neither document.
- summary should briefly explain the score in plain language."""


def analyze_resume(resume_text: str, job_description: str) -> AnalysisResponse:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

    client = genai.Client(api_key=api_key)

    user_message = (
        f"## Job Description\n{job_description}\n\n"
        f"## Resume\n{resume_text}"
    )

    interaction = client.interactions.create(
        model=MODEL,
        system_instruction=SYSTEM_PROMPT,
        input=user_message,
        response_format=[
            {
                "type": "text",
                "mime_type": "application/json",
                "schema": RESPONSE_SCHEMA,
            }
        ],
    )

    data = json.loads(interaction.output_text)
    return AnalysisResponse(**data)
