# AI Resume Analyzer

An AI-powered tool that compares a candidate's resume against a job description and
reports how well they match — a score, matched skills, unmatched skills, and a short
summary — using Google's Gemini API.

## Phase 1 Scope

This is the first phase of the project, focused on a single core workflow:

- Upload a resume (`.pdf` or `.docx`) and paste a job description.
- Extract the resume text and send it, along with the job description, to Gemini.
- Return a structured analysis: match score (0-100), matched skills, unmatched
  skills, and a plain-language summary.

There is no user authentication, no persistence/database, and no history of past
analyses — each analysis is a single, stateless request.

## Tech Stack

**Frontend**
- React 19 + Vite
- Plain CSS

**Backend**
- FastAPI (Python)
- Google Gemini API (`google-genai`) for the resume/job-description analysis
- `pypdf` and `python-docx` for text extraction from uploaded resumes
- Pydantic for response validation

## Project Structure

```
Resume_Analyzer/
├── backend/
│   ├── main.py              # FastAPI app and /api/analyze endpoint
│   ├── gemini_client.py     # Gemini API call, prompt, and response schema
│   ├── text_extraction.py   # PDF/DOCX text extraction
│   ├── schemas.py           # Pydantic response model
│   ├── requirements.txt
│   └── .env.example         # Required environment variables (no real secrets)
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── api.js                     # Calls the backend /api/analyze endpoint
    │   └── components/
    │       ├── ResumeUpload.jsx
    │       ├── JobDescriptionInput.jsx
    │       └── AnalysisResult.jsx
    └── package.json
```

## Local Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- A Gemini API key (see below)

### 1. Clone and configure the API key

```bash
git clone <your-repo-url>
cd Resume_Analyzer/backend
cp .env.example .env
```

Edit `backend/.env` and set your key:

```
GEMINI_API_KEY=your-actual-key-here
```

Get a key from [Google AI Studio](https://aistudio.google.com/apikey). Never commit
`.env` — it's already excluded via `.gitignore`.

### 2. Run the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### 3. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173` (Vite's default), and is
configured to call the backend at `http://localhost:8000`.

## Current Limitations

- Only `.pdf` and `.docx` resumes are supported (no scanned/image-only PDFs, since
  there's no OCR).
- No authentication, no saved history — every analysis is a one-off request.
- Single job description at a time; no batch comparison against multiple roles.
- No retrieval augmented context — the model only sees the raw resume text and job
  description passed to it, nothing else.
- CORS is currently locked to `http://localhost:5173` for local development.

## Future Plans

Planned for later phases:

- **RAG (Retrieval-Augmented Generation)**: ground analysis in a broader knowledge
  base (e.g. skill taxonomies, role benchmarks, company-specific requirements)
  instead of relying solely on the raw job description text.
- **Agentic functionality**: multi-step reasoning workflows, such as suggesting
  concrete resume edits, drafting tailored cover letters, or iteratively refining
  the match score based on follow-up questions.
- Persistent storage of past analyses and resume/job-description history.
- Support for additional resume formats (e.g. plain text, scanned/image PDFs via
  OCR).
