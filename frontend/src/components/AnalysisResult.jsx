import ATSReport from "./ATSReport";
import TailoredSuggestions from "./TailoredSuggestions";

function getScoreTier(score) {
  if (score >= 80) {
    return { color: "var(--success)", verdict: "Strong Match" };
  }
  if (score >= 50) {
    return { color: "var(--warning)", verdict: "Partial Match" };
  }
  return { color: "var(--danger)", verdict: "Weak Match" };
}

export default function AnalysisResult({ result }) {
  const {
    match_score,
    matched_skills,
    unmatched_skills,
    summary,
    ats_report,
    tailored_suggestions,
  } = result;
  const tier = getScoreTier(match_score);

  return (
    <div className="result">
      <div className="score-block">
        <div
          className="score-ring"
          style={{ "--pct": match_score, "--ring-color": tier.color }}
        >
          <div className="score-ring-inner">
            <span className="score-ring-value">{match_score}%</span>
            <span className="score-ring-label">Match</span>
          </div>
        </div>
        <span className="score-verdict" style={{ color: tier.color }}>
          {tier.verdict}
        </span>
      </div>

      <p className="summary">{summary}</p>

      <div className="skill-columns">
        <div>
          <h3 style={{ color: "var(--success)" }}>✅ Matched Skills</h3>
          <ul className="skill-list matched">
            {matched_skills.length === 0 && <li className="empty">None found</li>}
            {matched_skills.map((skill) => (
              <li key={skill}>{skill}</li>
            ))}
          </ul>
        </div>

        <div>
          <h3 style={{ color: "var(--danger)" }}>❌ Unmatched Skills</h3>
          <ul className="skill-list unmatched">
            {unmatched_skills.length === 0 && <li className="empty">None found</li>}
            {unmatched_skills.map((skill) => (
              <li key={skill}>{skill}</li>
            ))}
          </ul>
        </div>
      </div>

      {ats_report && <ATSReport report={ats_report} />}
      {tailored_suggestions && <TailoredSuggestions suggestions={tailored_suggestions} />}
    </div>
  );
}
