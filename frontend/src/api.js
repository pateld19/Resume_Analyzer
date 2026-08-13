const API_BASE_URL = "http://localhost:8000";

export async function analyzeResume(file, jobDescription) {
  const formData = new FormData();
  formData.append("resume", file);
  formData.append("job_description", jobDescription);

  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);
    const message = errorBody?.detail || `Request failed with status ${response.status}`;
    throw new Error(message);
  }

  return response.json();
}
