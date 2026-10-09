# Agent API Proxy (Node/Express)

A tiny **server-side proxy** so your own website can use the YojanaSaathi Agent API
**without exposing the agent key** to the browser.

The browser calls this proxy; this proxy adds the `X-Agent-API-Key` header and
forwards the request to YojanaSaathi.

## Setup

```bash
cd examples/agent-proxy
cp .env.example .env     # then edit .env
npm install
npm start
```

`.env`:

```
YOJANASAATHI_API_BASE=https://yojanasaathi-backend-b8ih.onrender.com
YOJANASAATHI_AGENT_API_KEY=yjs_ag_...
ALLOWED_ORIGIN=https://your-other-website.example.com
PORT=8080
```

## Endpoints exposed by the proxy

| Proxy route | Forwards to |
|---|---|
| `GET /public/schemes?q=&category=` | `/api/agent/v1/schemes/` |
| `GET /public/schemes/:id` | `/api/agent/v1/schemes/:id/` |
| `GET /public/schemes/:id/requirements` | `.../requirements/` |
| `GET /public/schemes/:id/eligibility` | `.../eligibility/` |
| `GET /citizen/applications` | `/api/agent/v1/citizen/applications/` |
| `GET /citizen/applications/:number` | `.../citizen/applications/:number/` |
| `GET /citizen/applications/:number/documents` | `.../documents/` |
| `GET /citizen/applications/:number/history` | `.../history/` |
| `GET /citizen/notifications` | `/api/agent/v1/citizen/notifications/` |
| `POST /citizen/applications/draft` | `/api/agent/v1/citizen/applications/draft/` |

## Calling it from your frontend

```js
// Public data (no consent needed)
const res = await fetch("http://localhost:8080/public/schemes");
const { count, results } = await res.json();

// Private data (after the citizen granted a delegation in YojanaSaathi)
const mine = await fetch("http://localhost:8080/citizen/applications", {
  headers: { "X-Citizen-Delegation-Token": delegationToken },
});
```

> Citizen routes require a `X-Citizen-Delegation-Token` obtained through the
> citizen consent flow (see `../../AGENT_API_INTEGRATION.md`).
>
> The agent key itself is **only** in this proxy's `.env` — it never reaches the browser.
