// YojanaSaathi Agent API — server-side proxy example
//
// Run this on YOUR server (or a serverless function). The agent key stays here
// and is never sent to the browser. Your frontend calls these local routes.
//
//   cp .env.example .env      # then fill in the values
//   npm install
//   npm start

import express from "express";

const app = express();

const PORT = process.env.PORT || 8080;
const API_BASE =
  process.env.YOJANASAATHI_API_BASE ||
  "https://yojanasaathi-backend-b8ih.onrender.com";
const AGENT_KEY = process.env.YOJANASAATHI_AGENT_API_KEY;
const ALLOWED_ORIGIN = process.env.ALLOWED_ORIGIN || "*";

if (!AGENT_KEY) {
  console.error(
    "Missing YOJANASAATHI_AGENT_API_KEY. Copy .env.example to .env and set it."
  );
  process.exit(1);
}

// ---- Minimal CORS so your own frontend can call this proxy ----
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", ALLOWED_ORIGIN);
  res.setHeader(
    "Access-Control-Allow-Headers",
    "Content-Type, X-Citizen-Delegation-Token"
  );
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  if (req.method === "OPTIONS") return res.sendStatus(204);
  next();
});

app.use(express.json());

// ---- Single place that talks to YojanaSaathi and injects the key ----
async function callAgent(path, { method = "GET", delegation, body } = {}) {
  const headers = { "X-Agent-API-Key": AGENT_KEY };
  if (delegation) headers["X-Citizen-Delegation-Token"] = delegation;
  if (body) headers["Content-Type"] = "application/json";

  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  const text = await response.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = text;
  }
  return { status: response.status, data };
}

function handler(fn) {
  return async (req, res) => {
    try {
      const { status, data } = await fn(req);
      res.status(status).json(data);
    } catch (err) {
      res.status(502).json({ error: "Agent API request failed", detail: String(err) });
    }
  };
}

// ---- Public scheme endpoints (no citizen consent needed) ----
app.get(
  "/public/schemes",
  handler((req) => {
    const qs = new URLSearchParams(req.query).toString();
    return callAgent(`/api/agent/v1/schemes/${qs ? `?${qs}` : ""}`);
  })
);

app.get(
  "/public/schemes/:id",
  handler((req) => callAgent(`/api/agent/v1/schemes/${req.params.id}/`))
);

app.get(
  "/public/schemes/:id/requirements",
  handler((req) =>
    callAgent(`/api/agent/v1/schemes/${req.params.id}/requirements/`)
  )
);

app.get(
  "/public/schemes/:id/eligibility",
  handler((req) =>
    callAgent(`/api/agent/v1/schemes/${req.params.id}/eligibility/`)
  )
);

// ---- Citizen endpoints ----
// The caller must supply a citizen delegation token (from citizen consent).
// It is passed through in the X-Citizen-Delegation-Token header.
function delegationFrom(req) {
  return req.headers["x-citizen-delegation-token"];
}

app.get(
  "/citizen/applications",
  handler((req) =>
    callAgent("/api/agent/v1/citizen/applications/", {
      delegation: delegationFrom(req),
    })
  )
);

app.get(
  "/citizen/applications/:number",
  handler((req) =>
    callAgent(`/api/agent/v1/citizen/applications/${req.params.number}/`, {
      delegation: delegationFrom(req),
    })
  )
);

app.get(
  "/citizen/applications/:number/documents",
  handler((req) =>
    callAgent(
      `/api/agent/v1/citizen/applications/${req.params.number}/documents/`,
      { delegation: delegationFrom(req) }
    )
  )
);

app.get(
  "/citizen/applications/:number/history",
  handler((req) =>
    callAgent(
      `/api/agent/v1/citizen/applications/${req.params.number}/history/`,
      { delegation: delegationFrom(req) }
    )
  )
);

app.get(
  "/citizen/notifications",
  handler((req) =>
    callAgent("/api/agent/v1/citizen/notifications/", {
      delegation: delegationFrom(req),
    })
  )
);

app.post(
  "/citizen/applications/draft",
  handler((req) =>
    callAgent("/api/agent/v1/citizen/applications/draft/", {
      method: "POST",
      delegation: delegationFrom(req),
      body: req.body,
    })
  )
);

// ---- Health ----
app.get("/health", (_req, res) => res.json({ status: "ok" }));

app.listen(PORT, () => {
  console.log(`YojanaSaathi proxy listening on http://localhost:${PORT}`);
  console.log(`Upstream: ${API_BASE}`);
});
