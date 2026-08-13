export default function JobDescriptionInput({ value, onChange }) {
  return (
    <div className="field">
      <label className="field-label" htmlFor="job-description">
        <span className="icon">💼</span> Job Description
      </label>
      <textarea
        id="job-description"
        rows={8}
        placeholder="Paste the job description here..."
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
    </div>
  );
}
