from pydantic import BaseModel


class ATSCheckItem(BaseModel):
    label: str
    passed: bool
    detail: str


class ATSCategory(BaseModel):
    name: str
    score: int
    max_score: int
    checks: list[ATSCheckItem]


class ATSReport(BaseModel):
    overall_score: int
    categories: list[ATSCategory]


class TailoredSuggestion(BaseModel):
    category: str
    issue: str
    suggestion: str
    example: str


class AnalysisResponse(BaseModel):
    match_score: int
    matched_skills: list[str]
    unmatched_skills: list[str]
    summary: str
    ats_report: ATSReport
    tailored_suggestions: list[TailoredSuggestion]
