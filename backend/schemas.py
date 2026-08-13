from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    match_score: int
    matched_skills: list[str]
    unmatched_skills: list[str]
    summary: str
