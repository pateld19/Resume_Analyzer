function getScoreTier(score) {
  if (score >= 80) {
    return { color: "var(--success)", verdict: "ATS Ready" };
  }
  if (score >= 50) {
    return { color: "var(--warning)", verdict: "Needs Work" };
  }
  return { color: "var(--danger)", verdict: "High Risk" };
}

export default function ATSReport({ report }) {
  const { overall_score, categories } = report;
  const tier = getScoreTier(overall_score);

  return (
    <div className="ats-report">
      <div className="ats-header">
        <h3>🤖 ATS Compliance Score</h3>
        <div className="ats-overall">
          <span className="ats-overall-value" style={{ color: tier.color }}>
            {overall_score}
          </span>
          <span className="ats-overall-max">/100</span>
          <span className="ats-overall-verdict" style={{ color: tier.color }}>
            {tier.verdict}
          </span>
        </div>
      </div>

      <div className="ats-categories">
        {categories.map((category) => {
          const pct = Math.round((category.score / category.max_score) * 100);
          const catTier = getScoreTier(pct);
          return (
            <details className="ats-category" key={category.name}>
              <summary>
                <span className="ats-category-name">{category.name}</span>
                <span className="ats-category-score" style={{ color: catTier.color }}>
                  {category.score}/{category.max_score}
                </span>
              </summary>
              <div className="ats-progress-track">
                <div
                  className="ats-progress-fill"
                  style={{ width: `${pct}%`, background: catTier.color }}
                />
              </div>
              <ul className="ats-checks">
                {category.checks.map((check) => (
                  <li key={check.label} className={check.passed ? "passed" : "failed"}>
                    <span className="ats-check-icon">{check.passed ? "✓" : "✗"}</span>
                    <div>
                      <div className="ats-check-label">{check.label}</div>
                      <div className="ats-check-detail">{check.detail}</div>
                    </div>
                  </li>
                ))}
              </ul>
            </details>
          );
        })}
      </div>
    </div>
  );
}
