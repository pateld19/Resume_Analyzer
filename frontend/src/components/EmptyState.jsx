export default function EmptyState({ loading }) {
  if (loading) {
    return (
      <div className="empty-state">
        <span className="spinner spinner-lg" />
        <h3>Analyzing your resume...</h3>
        <p>Checking your match score, ATS compliance, and tailored improvements.</p>
      </div>
    );
  }

  return (
    <div className="empty-state">
      <div className="empty-state-icon">🎯</div>
      <h3>Your results will appear here</h3>
      <p>
        Upload a resume and paste a job description to get your match score, ATS
        compliance score, and tailored suggestions.
      </p>
    </div>
  );
}
