const BASE = import.meta.env.VITE_API_URL || '/api';

const authHeader = () => {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

// FastAPI errors look like { detail: "msg" } or { detail: [{ msg, loc }, ...] }
async function toError(res) {
  const data = await res.json().catch(() => null);
  let msg = data?.detail ?? data?.error;
  if (Array.isArray(msg)) msg = msg.map((m) => m.msg).join('. ');
  return new Error(typeof msg === 'string' && msg ? msg : `Request failed (${res.status})`);
}

/**
 * body can be a plain object (sent as JSON), FormData (file upload)
 * or URLSearchParams (form-encoded, used by /token).
 */
export async function api(path, { method = 'GET', body } = {}) {
  const isRaw = body instanceof FormData || body instanceof URLSearchParams;
  const res = await fetch(BASE + path, {
    method,
    headers: {
      ...authHeader(),
      ...(body && !isRaw ? { 'Content-Type': 'application/json' } : {}),
    },
    body: body ? (isRaw ? body : JSON.stringify(body)) : undefined,
  });
  if (!res.ok) throw await toError(res);
  const text = await res.text();
  try {
    return text ? JSON.parse(text) : null;
  } catch {
    return text;
  }
}

/** Authenticated binary download (used for previews and downloads). */
export async function apiBlob(path) {
  const res = await fetch(BASE + path, { headers: authHeader() });
  if (!res.ok) throw await toError(res);
  return res.blob();
}
