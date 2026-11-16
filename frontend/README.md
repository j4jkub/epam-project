# Ledgerly (frontend)

React + Vite frontend for the FastAPI project/document backend.

## Run

```bash
npm install
cp .env.example .env     # set API_PROXY_TARGET if your API isn't on :8000
npm run dev
```

Open http://localhost:5173. In dev, `/api/*` is proxied to your backend with the `/api` prefix
removed, so no CORS setup is needed.

For a production build set `VITE_API_URL` to your API's base URL and enable CORS
(allow the `Authorization` header) on the backend, or serve the built `dist/` behind the
same reverse proxy as the API.

## Backend contract used

| Feature | Call |
|---|---|
| Register | `POST /auth` (JSON incl. `repeat_password`), then login |
| Login | `POST /token` (form: `username`, `password`) → `{access_token, user}` |
| Current user | `GET /auth/me/` |
| Projects | `GET/POST /projects`, `GET /project/{id}/info`, `PUT /project/{id}/info`, `DELETE /project/{id}` |
| Add / remove person | `POST` / `DELETE /project/{id}/invite?user=<username>` |
| List / upload files | `GET` / `POST /project/{id}/documents` (multipart field `file`) |
| Download / preview | `GET /document/{id}` (fetched with the bearer token, shown from a blob URL) |
| Delete file | `DELETE /document/{id}` ← **new endpoint required** |

## Preview support
Images, PDF, video, audio, plain text / code / JSON / CSV and Markdown preview in the browser.
Everything else shows a download prompt.

## Optional: email invites
Set `emailInvite: true` in `src/config.js` after adding:

- `POST /project/{id}/invite/email?email=a@b.c` → `{ "sent": bool, "link": "https://app/invite/<token>" }`
- `GET /invites/{token}` → `{ "project_name", "invited_by" }`
- `POST /invites/{token}/accept` (auth) → `{ "project_id" }`
