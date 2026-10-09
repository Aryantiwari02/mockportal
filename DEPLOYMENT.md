# Deployment Guide — YojanaSaathi

Production target: **Django/DRF backend on Render** + **React/Vite frontend on Vercel** + **PostgreSQL**.

---

## 1. Push this repo to GitHub

```bash
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

## 2. Backend → Render (Blueprint)

1. Go to **Render Dashboard → New → Blueprint**.
2. Connect the GitHub repo. Render reads `render.yaml` and creates:
   - a **web service** `yojanasaathi-backend` (Gunicorn),
   - a **PostgreSQL** database `yojanasaathi-db`.
3. When prompted (`sync: false`), fill in these environment variables:

   | Key | Value |
   |---|---|
   | `DJANGO_SECRET_KEY` | your secret key |
   | `TWILIO_ACCOUNT_SID` | `AC...` |
   | `TWILIO_AUTH_TOKEN` | your auth token |
   | `TWILIO_VERIFY_SERVICE_SID` | `VA...` |
   | `YOJANASAATHI_AGENT_API_KEY` | `yjs_ag_...` |
   | `DJANGO_CORS_ALLOWED_ORIGINS` | `https://<your-app>.vercel.app` |
   | `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://<your-app>.vercel.app` |

   `DATABASE_URL` is injected automatically from the managed database.
4. Deploy. The build runs `backend/build.sh`:
   install → `collectstatic` → `migrate` → `seed_schemes`.

Backend URL will look like `https://yojanasaathi-backend.onrender.com`.

## 3. Frontend → Vercel

1. **Vercel → Add New → Project → Import** the same GitHub repo.
2. Set **Root Directory** to `frontend`.
3. Add an environment variable (Production **and** Preview):

   | Key | Value |
   |---|---|
   | `VITE_API_BASE_URL` | `https://yojanasaathi-backend.onrender.com/api` |

4. Deploy.

## 4. Close the loop (CORS)

Copy the Vercel production URL (e.g. `https://yojanasaathi.vercel.app`) back into
Render's `DJANGO_CORS_ALLOWED_ORIGINS` and `DJANGO_CSRF_TRUSTED_ORIGINS`, then
redeploy the backend. Without this the browser blocks API calls.

## 5. Verify

- `https://<backend>/api/status/` → `{"status": "success", ...}`
- `https://<backend>/api/schemes/` → 4 seeded schemes
- `https://<backend>/api/agent/v1/docs/` → Swagger UI
- Frontend loads and scheme browsing works

---

## Environment variables reference

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | **Required.** Django signing key. |
| `DJANGO_DEBUG` | `False` in production. |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames (`.onrender.com` etc.). |
| `DJANGO_CORS_ALLOWED_ORIGINS` | Frontend origin(s) allowed to call the API. |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Trusted HTTPS origins for CSRF. |
| `DJANGO_SECURE_SSL_REDIRECT` | `True` for automatic HTTP→HTTPS (set `False` if the host proxy handles it). |
| `DATABASE_URL` | PostgreSQL connection string (Render injects this). |
| `OTP_MODE` | `demo` = fixed OTP, no SMS; `twilio` = real SMS. |
| `OTP_DEMO_CODE` | Fixed demo OTP (default `123456`). |
| `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN` / `TWILIO_VERIFY_SERVICE_SID` | Twilio Verify credentials. |
| `TWILIO_ALLOWED_MOBILE` | Comma-separated numbers allowed to receive OTP. |
| `YOJANASAATHI_AGENT_API_KEY` | M2M API key for the AI agent. |

---

## Demo login

With `OTP_MODE=demo`, no SMS is sent. Use an allowed mobile number
(`TWILIO_ALLOWED_MOBILE`) and the OTP code `OTP_DEMO_CODE` (default `123456`).
To let anyone log in during a demo, clear `TWILIO_ALLOWED_MOBILE` (empty
value allows all valid 10-digit numbers).

---

## Notes & limitations

- **Uploaded documents** are stored on the instance disk (`MEDIA_ROOT`). On
  hosts with an ephemeral filesystem they are lost on redeploy/restart. For
  durable storage, add Cloudinary/S3 via `django-storages`.
- Render's **free PostgreSQL** expires after 30 days; migrate to Neon or a paid
  plan for anything long-lived.
- The free Render web service **sleeps** after inactivity; the first request
  after idle is slow.
