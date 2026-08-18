export default function TailoredSuggestions({ suggestions }) {
  if (!suggestions || suggestions.length === 0) return null;

  return (
    <div className="suggestions">
      <h3>✨ Tailored Improvements</h3>
      <div className="suggestion-list">
        {suggestions.map((suggestion, index) => (
          <div className="suggestion-card" key={index}>
            <span className="suggestion-badge">{suggestion.category}</span>
            <p className="suggestion-issue">{suggestion.issue}</p>
            <p className="suggestion-fix">
              <strong>Fix:</strong> {suggestion.suggestion}
            </p>
            {suggestion.example && (
              <div className="suggestion-example">{suggestion.example}</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
