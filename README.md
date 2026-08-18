# AI Resume Analyzer

An AI-powered tool that compares a candidate's resume against a job description and
reports how well they match — a match score, an ATS compliance score, matched/unmatched
skills, and tailored suggestions for improving the resume — using Google's Gemini API.

## Live Demo

**[pateld19-resume-analyzer-web.onrender.com](https://pateld19-resume-analyzer-web.onrender.com)**

Hosted on Render's free tier. The backend spins down after 15 minutes of inactivity,
so the first request after a quiet period can take 30-50 seconds to wake up —
subsequent requests are fast.

## Features

- **Match analysis**: upload a resume (`.pdf` or `.docx`) and paste a job description
  to get a 0-100 match score, matched/unmatched skills, and a plain-language summary.
- **ATS Compliance Score**: a 0-100 score across four weighted categories —
  formatting & parseability, section headings & contact info, content quality
  (quantified achievements, action verbs), and keyword match with the job
  description — grounded in published ATS-optimization guidance (Jobscan and
  similar sources).
- **Tailored suggestions**: concrete, actionable edits (with before/after examples)
  to close keyword gaps and fix ATS issues, generated from the resume, the job
  description, and the ATS findings together.
- **Dark mode** with persisted preference, and a desktop-friendly two-column layout.

There is no user authentication, no persistence/database, and no history of past
analyses — each analysis is a single, stateless request.

## Tech Stack

**Frontend**
- React 19 + Vite
- Plain CSS

**Backend**
- FastAPI (Python)
- Google Gemini API (`google-genai`) for the resume/job-description analysis and
  tailored suggestions
- `pypdf` and `python-docx` for text extraction and rule-based ATS structure checks
- Pydantic for response validation

**Hosting**
- Render (free tier) — a Blueprint (`render.yaml`) provisions a Python web service
  for the backend and a static site for the frontend, wired together via env vars.

## Project Structure

```
Resume_Analyzer/
├── render.yaml               # Render Blueprint: backend web service + frontend static site
├── backend/
│   ├── main.py                # FastAPI app and /api/analyze endpoint
│   ├── gemini_client.py       # Gemini API call, prompt, and response schema
│   ├── ats_checker.py         # Rule-based ATS formatting/section/content checks
│   ├── text_extraction.py     # PDF/DOCX text extraction
│   ├── schemas.py             # Pydantic response models
│   ├── requirements.txt
│   └── .env.example           # Required environment variables (no real secrets)
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── api.js                        # Calls the backend /api/analyze endpoint
    │   └── components/
    │       ├── ResumeUpload.jsx
    │       ├── JobDescriptionInput.jsx
    │       ├── AnalysisResult.jsx
    │       ├── ATSReport.jsx             # ATS score + category breakdown
    │       ├── TailoredSuggestions.jsx   # Suggested resume edits
    │       ├── EmptyState.jsx
    │       └── ThemeToggle.jsx           # Dark/light mode toggle
    └── package.json
```

## Local Setup

The live demo above works out of the box, but if you want to run it locally for
development:

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

The API will be available at `http://localhost:8000`. CORS defaults to
`http://localhost:5173`; override with a comma-separated `ALLOWED_ORIGINS` env var
for other origins.

### 3. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173` (Vite's default), and calls
the backend at `http://localhost:8000` by default. Set `VITE_API_BASE_URL` to point
it at a different backend (e.g. the deployed one).

## Deployment

The root-level `render.yaml` is a [Render Blueprint](https://render.com/docs/infrastructure-as-code)
that provisions both services in one shot:

- `pateld19-resume-analyzer-api` — Python web service running the FastAPI backend.
  Needs `GEMINI_API_KEY` set as a secret in the Render dashboard (never stored in
  the repo); `ALLOWED_ORIGINS` is pre-wired to the frontend's URL.
- `pateld19-resume-analyzer-web` — static site serving the built frontend, with
  `VITE_API_BASE_URL` pre-wired to the backend's URL.

To deploy: push to GitHub, then in Render click **New +** → **Blueprint**, select
the repo, and supply `GEMINI_API_KEY` when prompted. Every subsequent push to `main`
auto-redeploys both services.

## Current Limitations

- Only `.pdf` and `.docx` resumes are supported (no scanned/image-only PDFs, since
  there's no OCR).
- No authentication, no saved history — every analysis is a one-off request.
- Single job description at a time; no batch comparison against multiple roles.
- No retrieval augmented context — the model only sees the raw resume text and job
  description passed to it, nothing else.
- ATS structural checks (tables, header/footer content) are only reliably
  detectable for `.docx` files — PDF layout analysis (columns, tables) is limited
  by what `pypdf` can inspect.
- The free-tier backend sleeps after 15 minutes of inactivity, adding a cold-start
  delay to the first request after a quiet period.

## Future Plans

Planned for later phases:

- **RAG (Retrieval-Augmented Generation)**: ground analysis in a broader knowledge
  base (e.g. skill taxonomies, role benchmarks, company-specific requirements)
  instead of relying solely on the raw job description text.
- **Agentic functionality**: multi-step reasoning workflows, such as drafting
  tailored cover letters or iteratively refining the match score based on
  follow-up questions.
- Persistent storage of past analyses and resume/job-description history.
- Support for additional resume formats (e.g. plain text, scanned/image PDFs via
  OCR).
