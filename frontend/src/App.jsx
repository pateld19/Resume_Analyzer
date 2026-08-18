import { useState } from "react";
import "./App.css";
import ResumeUpload from "./components/ResumeUpload";
import JobDescriptionInput from "./components/JobDescriptionInput";
import AnalysisResult from "./components/AnalysisResult";
import EmptyState from "./components/EmptyState";
import ThemeToggle from "./components/ThemeToggle";
import { analyzeResume } from "./api";

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const canSubmit = file && jobDescription.trim().length > 0 && !loading;

  async function handleSubmit(event) {
    event.preventDefault();
    if (!canSubmit) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const analysis = await analyzeResume(file, jobDescription);
      setResult(analysis);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="app">
        <div className="topbar">
          <div className="brand">
            <div className="badge">📊</div>
            <div>
              <h1>Resume Analyzer</h1>
              <p className="subtitle">
                Match score, ATS compliance, and tailored edits — in one pass.
              </p>
            </div>
          </div>
          <ThemeToggle />
        </div>

        <div className="layout">
          <div className="card form-card">
            <form onSubmit={handleSubmit}>
              <ResumeUpload file={file} onFileChange={setFile} />
              <JobDescriptionInput value={jobDescription} onChange={setJobDescription} />

              <button className="submit-btn" type="submit" disabled={!canSubmit}>
                {loading && <span className="spinner" />}
                {loading ? "Analyzing..." : "Analyze Match"}
              </button>
            </form>

            {error && (
              <p className="error">
                <span>⚠️</span> {error}
              </p>
            )}
          </div>

          <div className="card result-card">
            {result ? <AnalysisResult result={result} /> : <EmptyState loading={loading} />}
          </div>
        </div>

        <p className="footer-note">Powered by Gemini · Your files never leave this session</p>
      </div>
    </div>
  );
}

export default App;
