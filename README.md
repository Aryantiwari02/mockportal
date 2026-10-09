# HR2-OI-FF337B77
HACKERING 2.0 Round 2 Project Repository for Team AURA (Open Innovation Track)

---

# YojanaSaathi — Government Scheme Navigator

> ⚠ **DEMO PORTAL** — This is an educational demonstration project, not an official government website. All scheme information, application records, and verification data are for demonstration purposes only.

---

## Project Overview

**YojanaSaathi** is a full-stack demonstration of a citizen-facing government welfare scheme portal, built to explore:

- Secure citizen authentication (OTP-based mobile verification via Twilio)
- Multi-step online application forms with document upload
- Application status tracking with audit trail timeline
- Trilingual UI (English · ಕನ್ನಡ · हिन्दी)
- Secure YojanaSaathi AI Agent M2M Public REST API with citizen delegation (v1)

---

## Architecture

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite, React Router v7 |
| Backend | Django 6.1 + Django REST Framework |
| Auth | Twilio Verify (OTP) + DRF Token Auth + M2M Agent API Keys |
| Database | SQLite (local dev) / PostgreSQL (production) |
| Styles | Vanilla CSS with design-token system |

---

## Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Node.js 20+
- A [Twilio account](https://www.twilio.com/) with a Verify service SID

### 1. Clone the repository

```bash
git clone https://github.com/hackering-2-0/HR2-OI-FF337B77.git
cd HR2-OI-FF337B77
```

### 2. Backend setup

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Create environment file from template
cp backend/.env.example backend/.env
# Edit backend/.env and set DJANGO_SECRET_KEY and Twilio credentials

# Apply migrations
cd backend
python manage.py migrate

# (Optional) Generate an Agent API key for external AI agent
python manage.py manage_agent_keys create --name "Local AI Agent"

# Start the backend server (default: http://127.0.0.1:8000)
python manage.py runserver
```

### 3. Frontend setup

```bash
# In a separate terminal, from the project root:
cd frontend
npm install

# Start the development server (default: http://localhost:5173)
npm run dev
```

> The Vite dev server is pre-configured to proxy `/api` and `/media` requests to `http://127.0.0.1:8000` automatically — no CORS issues during development.

---

## API Reference

### Interactive Documentation & OpenAPI Specification
- Swagger UI Interactive Docs: `http://127.0.0.1:8000/api/agent/v1/docs/`
- OpenAPI 3.0 Schema: `http://127.0.0.1:8000/api/agent/v1/openapi.json`
- Full Guide: See `backend/docs/YOJANASAATHI_AGENT_INTEGRATION.md`

### Key Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/auth/request-otp/` | None | Send OTP to mobile number |
| `POST` | `/api/auth/verify-otp/` | None | Verify OTP and receive token |
| `POST` | `/api/auth/agent-delegation/` | Token | Grant delegation token to YojanaSaathi AI agent |
| `GET` | `/api/schemes/` | None | List all schemes |
| `GET` | `/api/schemes/<id>/` | None | Scheme details |
| `GET` | `/api/schemes/<id>/blank-form-pdf/` | None | Download blank application PDF |
| `POST` | `/api/applications/` | Token | Create application draft |
| `GET` | `/api/applications/mine/` | Token | List citizen's applications |
| `GET` | `/api/applications/<app_no>/` | Token | Application detail |
| `POST` | `/api/applications/<app_no>/submit/` | Token | Submit application |
| `POST` | `/api/applications/<app_no>/documents/` | Token | Upload document |
| `GET` | `/api/applications/<app_no>/pdf/` | Token | Download application PDF |
| `GET` | `/api/agent/v1/schemes/` | Agent Key | Agent scheme search & discovery |
| `POST` | `/api/agent/v1/citizen/applications/draft/` | Agent Key + Delegation | Draft application on citizen's behalf |
| `GET` | `/api/agent/v1/citizen/applications/` | Agent Key + Delegation | Citizen application tracking |

---

## Project Structure

```
GOVERNMENT-YOJANA-PORTAL/
├── backend/
│   ├── accounts/          # Citizen auth, OTP (Twilio), Token
│   ├── agent_api/         # Machine-to-machine AI Agent API (v1)
│   ├── applications/      # Application workflow, documents, notifications
│   ├── schemes/           # Scheme data, trilingual translations
│   ├── config/            # Django settings & URLs
│   ├── docs/              # OpenAPI specs & Integration documentation
│   ├── .env.example       # Template environment variables
│   └── manage.py
├── frontend/
│   ├── src/               # React components, pages, i18n
│   ├── vercel.json        # Vercel deployment rewrites
│   ├── vite.config.js     # Dev proxy
│   └── package.json
├── .gitignore
└── README.md
```

---

## License

This project is a demonstration portfolio project. Not for production or official government use.

---

*Built with Django · React · Vite · Twilio · ❤️ for Indian governance technology*
