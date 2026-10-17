const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL;
const inferredBaseUrl = `${window.location.protocol}//${window.location.hostname}:8000`;

export const API_BASE_URL = (configuredBaseUrl || inferredBaseUrl).replace(/\/+$/, "");

async function apiRequest(path, options = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: {
        Accept: "application/json",
        ...(options.body ? { "Content-Type": "application/json" } : {}),
        ...options.headers,
      },
    });
  } catch {
    throw new Error(
      `Cannot reach the TruthLatch API at ${API_BASE_URL}. Check that the backend is running and its CORS origins include this frontend URL.`
    );
  }

  const text = await response.text();
  let data = null;

  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }
  }

  if (!response.ok) {
    const detail = data && typeof data === "object" ? data.detail : null;
    throw new Error(
      typeof detail === "string"
        ? detail
        : `TruthLatch API returned HTTP ${response.status}.`
    );
  }

  return data;
}

export function fetchHistory() {
  return apiRequest("/api/v1/history");
}

export function verifyClaim(payload) {
  return apiRequest("/api/v1/verify", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function fetchHealth() {
  return apiRequest("/health");
}
