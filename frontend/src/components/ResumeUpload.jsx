import { useState } from "react";

export default function ResumeUpload({ file, onFileChange }) {
  const [isDragging, setIsDragging] = useState(false);

  function handleChange(event) {
    const selected = event.target.files?.[0] ?? null;
    onFileChange(selected);
  }

  function handleDrop(event) {
    event.preventDefault();
    setIsDragging(false);
    const dropped = event.dataTransfer.files?.[0] ?? null;
    if (dropped) onFileChange(dropped);
  }

  return (
    <div className="field">
      <label className="field-label" htmlFor="resume-upload">
        <span className="icon">📄</span> Resume
      </label>
      <div
        className={`dropzone ${isDragging ? "dragging" : ""} ${file ? "has-file" : ""}`}
        onDragOver={(event) => {
          event.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
      >
        <input
          id="resume-upload"
          type="file"
          accept=".pdf,.docx"
          onChange={handleChange}
        />
        {file ? (
          <span className="dropzone-file">✅ {file.name}</span>
        ) : (
          <>
            <div className="dropzone-icon">⬆️</div>
            <div className="dropzone-title">Drag & drop your resume here</div>
            <div className="dropzone-hint">or click to browse · PDF or DOCX</div>
          </>
        )}
      </div>
    </div>
  );
}
