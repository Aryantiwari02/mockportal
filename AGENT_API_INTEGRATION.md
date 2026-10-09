# Integrating Another Website with the YojanaSaathi Agent API

This guide lets a **separate website** consume the YojanaSaathi API safely.

> **The API is machine-to-machine (M2M).** Use it from your website's **server / serverless function**, never from browser JavaScript. The agent key must never reach the end user.

---

## 1. Base URL

```
https://yojanasaathi-backend-b8ih.onrender.com
```

Agent API prefix: `/api/agent/v1`

Interactive docs (Swagger): `https://yojanasaathi-backend-b8ih.onrender.com/api/agent/v1/docs/`

> First request after ~15 min idle can be slow (Render free tier cold start).

## 2. Authentication

Every agent request needs the API key in **one** of these headers:

| Header | Value |
|---|---|
| `X-Agent-API-Key` | `yjs_ag_...` |
| `Authorization` | `Bearer yjs_ag_...` |

Store the key as an environment variable on **your** server, e.g. `YOJANASAATHI_AGENT_API_KEY`.

```bash
curl https://yojanasaathi-backend-b8ih.onrender.com/api/agent/v1/schemes/ \
  -H "X-Agent-API-Key: $YOJANASAATHI_AGENT_API_KEY"
```

## 3. What the key can access

### 3a. Public scheme endpoints — key only

| Method & path | Purpose |
|---|---|
| `GET /api/agent/v1/schemes/` | List/search schemes (`?q=`, `?category=`) |
| `GET /api/agent/v1/schemes/{id}/` | Full scheme details |
| `GET /api/agent/v1/schemes/{id}/requirements/` | Form fields + required documents |
| `GET /api/agent/v1/schemes/{id}/eligibility/` | Eligibility rules + process |

### 3b. Citizen endpoints — key **plus** a citizen delegation token

These require a second header, `X-Citizen-Delegation-Token`, that the **citizen** grants after logging in. Tokens are scoped and expire (max 7 days).

| Method & path | Required scope |
|---|---|
| `GET /api/agent/v1/citizen/applications/` | `applications:read` |
| `GET /api/agent/v1/citizen/applications/{number}/` | `applications:read` |
| `GET /api/agent/v1/citizen/applications/{number}/documents/` | `applications:read` |
| `GET /api/agent/v1/citizen/applications/{number}/history/` | `applications:read` |
| `GET /api/agent/v1/citizen/notifications/` | `notifications:read` |
| `POST /api/agent/v1/citizen/applications/draft/` | `applications:draft` |

### 3c. What the agent can **never** do

- No `/admin/` access (separate Django superuser login).
- No raw document/file downloads — only verification statuses.
- Cannot **submit** applications — only save **drafts** (citizen submits).
- Cannot read a citizen's data without that citizen's own delegation.

## 4. Citizen delegation flow

The citizen consents inside the portal (or your own UI that logs into YojanaSaathi):

```bash
# 1) Citizen logs in with OTP (demo: 7204058792 / 123456) and gets a DRF token
curl -X POST https://yojanasaathi-backend-b8ih.onrender.com/api/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{"mobile":"7204058792","otp":"123456"}'
# -> { "token": "<citizen-token>", "citizen": {...} }

# 2) Citizen grants the agent a scoped, time-limited delegation
curl -X POST https://yojanasaathi-backend-b8ih.onrender.com/api/auth/agent-delegation/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <citizen-token>" \
  -d '{"duration_hours": 2, "scopes": ["applications:read","notifications:read"]}'
# -> { "delegation_token": "yjs_del_...", "scopes": [...], "expires_at": "..." }

# 3) Agent uses key + delegation token
curl https://yojanasaathi-backend-b8ih.onrender.com/api/agent/v1/citizen/applications/ \
  -H "X-Agent-API-Key: $YOJANASAATHI_AGENT_API_KEY" \
  -H "X-Citizen-Delegation-Token: yjs_del_..."
```

The citizen can list/revoke delegations at `GET /api/auth/agent-delegations/` and `POST /api/auth/agent-delegation/{id}/revoke/`.

## 5. Recommended pattern: server-side proxy

Do **not** call the agent API directly from the browser. Put a tiny proxy on your own server that:

1. Holds the agent key in an environment variable.
2. Exposes only the endpoints you need to your frontend.
3. Adds your own auth/rate limiting.

A ready-to-run Node example lives in [`examples/agent-proxy/`](examples/agent-proxy/).

```js
// Minimal illustration (Express)
app.get("/public/schemes", async (req, res) => {
  const r = await fetch(`${process.env.YOJANASAATHI_API_BASE}/api/agent/v1/schemes/`, {
    headers: { "X-Agent-API-Key": process.env.YOJANASAATHI_AGENT_API_KEY },
  });
  res.status(r.status).json(await r.json());
});
```

Python equivalent:

```python
import os, requests

BASE = os.environ["YOJANASAATHI_API_BASE"]
HEADERS = {"X-Agent-API-Key": os.environ["YOJANASAATHI_AGENT_API_KEY"]}

def list_schemes():
    r = requests.get(f"{BASE}/api/agent/v1/schemes/", headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()
```

## 6. CORS

The backend currently only allows the YojanaSaathi portal origin. CORS only affects **browser** calls — server-to-server calls (recommended) are unaffected.

If your frontend must call the backend directly from a browser, add your origin on Render:

```
DJANGO_CORS_ALLOWED_ORIGINS = https://portal.example.com,https://frontend-five-rust-92.vercel.app
DJANGO_CSRF_TRUSTED_ORIGINS = https://portal.example.com,https://frontend-five-rust-92.vercel.app
```

…then redeploy the backend. **Even then, never ship the agent key to the browser.**

## 7. Rate limits

| Scope | Limit |
|---|---|
| Public scheme endpoints | 300 requests/min per key |
| Citizen operations | 120 requests/min per key |

Exceeding a limit returns HTTP `429`.

## 8. Rotating / revoking the key

The current key is the **environment key** (`YOJANASAATHI_AGENT_API_KEY` on Render):

1. Update `YOJANASAATHI_AGENT_API_KEY` in Render → Environment.
2. Redeploy. The old value stops working immediately.

For multiple consumers / per-client keys, create database-backed keys (rotate without redeploy):

```bash
python manage.py manage_agent_keys create  --name "Partner site"
python manage.py manage_agent_keys list
python manage.py manage_agent_keys revoke --prefix yjs_ag_xxxxxxxx
python manage.py manage_agent_keys rotate --old-prefix yjs_ag_xxxxxxxx
```

The raw secret is shown **once** at creation — copy it straight into your server's env vars.

## 9. Security checklist

- [ ] Key stored only in server-side environment variables.
- [ ] Never logged, never committed, never sent to the browser.
- [ ] Prefer a dedicated DB-backed key per consumer so you can rotate/revoke independently.
- [ ] Only request the citizen delegation scopes you actually need.
- [ ] Treat delegation tokens as sensitive and short-lived.
- [ ] Call over HTTPS only.
