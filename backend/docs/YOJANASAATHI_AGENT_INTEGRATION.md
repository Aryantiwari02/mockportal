# YojanaSaathi AI Agent Integration Guide

## 1. Overview & Architecture

The **YojanaSaathi AI Agent Integration** provides a secure, machine-to-machine (M2M) REST API that allows an externally hosted AI agent (running online or on a separate cloud machine) to interact with the Government Yojana Portal backend over HTTPS.

```
+-----------------------------+                           +--------------------------------------+
|                             |   X-Agent-API-Key         |  Government Yojana Portal (Django)   |
|   External YojanaSaathi     |   -------------------->   |                                      |
|   AI Agent Service          |                           |  /api/agent/v1/schemes/              |
|   (Cloud / LLM Runner)      |   X-Agent-API-Key +       |  /api/agent/v1/citizen/applications/ |
|                             |   X-Citizen-Delegation    |                                      |
|                             |   -------------------->   |  [Audited & Rate-Limited]            |
+-----------------------------+                           +--------------------------------------+
                                                                             ^
                                                                             | Grants delegation
                                                                             | via OTP session
                                                                  +-----------------------+
                                                                  |  Verified Citizen     |
                                                                  |  (Citizen Portal)     |
                                                                  +-----------------------+
```

### Core Security Principles

1. **Separation of Concerns:** The Agent API Key identifies the AI service, but **never** grants unrestricted access to citizens' personal data.
2. **Citizen-Consent Delegation:** Access to a citizen's applications, draft editing, and verification tracking requires an active, short-lived, scoped delegation token (`X-Citizen-Delegation-Token`) generated after citizen OTP verification.
3. **Citizen Isolation:** The AI agent can strictly access only records belonging to the delegated citizen. Inquiries for any other citizen's application return HTTP `404 Not Found` without disclosing existence.
4. **Least Privilege & No Authority Impersonation:**
   - The agent can create or edit **DRAFT** applications only.
   - The agent **cannot** mark applications as submitted or approved.
   - The agent **cannot** verify, approve, or reject documents.
   - Uploaded document binary files and raw URLs are never leaked to the agent (only verification statuses and remarks are returned).
5. **Credential Rotation & Revocation:**
   - Database-backed keys support instant revocation and zero-downtime rotation.
   - Management CLI allows administrators to create, list, rotate, and revoke keys without restarting the server.
6. **Audit Trail & Rate Limiting:** Every agent interaction is recorded in `AgentAuditLog` with timestamp, key prefix, IP, citizen ID (if applicable), and HTTP status code.

---

## 2. Authentication & Headers

### Required Headers

| Header | Required For | Format / Description |
|---|---|---|
| `X-Agent-API-Key` | **All** Agent API calls | Cryptographically strong secret key (e.g. `yjs_ag_...`). Also accepts `Authorization: Bearer <key>`. |
| `X-Citizen-Delegation-Token` | **Citizen-specific** calls (`/api/agent/v1/citizen/*`) | Scoped delegation token issued after citizen OTP authentication (e.g. `yjs_del_...`). |
| `Content-Type` | POST / PATCH requests | `application/json` |

---

## 3. Public Scheme Endpoints

*Requires `X-Agent-API-Key` only. No citizen delegation needed.*

### 3.1 List & Search Schemes
- **URL:** `GET /api/agent/v1/schemes/`
- **Query Parameters:**
  - `q`: Search string (matches title, short_description, description, category)
  - `category`: Filter by category (e.g., `Health`, `Pension`)
- **Example Request:**
  ```http
  GET /api/agent/v1/schemes/?q=Ayushman HTTP/1.1
  Host: api.yojanasaathi.gov.in
  X-Agent-API-Key: yjs_ag_YOUR_SECRET_AGENT_KEY
  ```
- **Example Response (200 OK):**
  ```json
  {
    "count": 1,
    "results": [
      {
        "id": "health-001",
        "category": "Health",
        "title": "Ayushman Bharat PM-JAY",
        "short_description": "Comprehensive health protection coverage up to ₹5 lakh per family.",
        "benefits": [
          "Cashless treatment up to ₹5 Lakhs",
          "Secondary and tertiary hospitalization"
        ],
        "eligibility": [
          "Families identified in SECC 2011",
          "Rural households in specified deprivation categories"
        ],
        "updated_at": "2026-10-09T04:00:00Z"
      }
    ]
  }
  ```

### 3.2 Retrieve Complete Scheme Details
- **URL:** `GET /api/agent/v1/schemes/{scheme_id}/`
- **Example Response (200 OK):**
  ```json
  {
    "id": "health-001",
    "category": "Health",
    "title": "Ayushman Bharat PM-JAY",
    "short_description": "...",
    "description": "Full details...",
    "benefits": [...],
    "documents": ["Aadhaar Card", "Ration Card"],
    "eligibility": [...],
    "eligibility_rules": { "max_income": 300000, "resident": true },
    "application_fields": [
      { "name": "full_name", "label": "Full Name", "type": "text", "required": true },
      { "name": "annual_income", "label": "Annual Income", "type": "number", "required": true }
    ],
    "application_process": ["Step 1", "Step 2"],
    "translations": {},
    "updated_at": "2026-10-09T04:00:00Z"
  }
  ```

### 3.3 Retrieve Scheme Requirements (Fields & Documents)
- **URL:** `GET /api/agent/v1/schemes/{scheme_id}/requirements/`
- **Example Response (200 OK):**
  ```json
  {
    "id": "health-001",
    "title": "Ayushman Bharat PM-JAY",
    "category": "Health",
    "application_fields": [
      { "name": "full_name", "label": "Full Name", "type": "text", "required": true },
      { "name": "annual_income", "label": "Annual Income", "type": "number", "required": true }
    ],
    "required_documents": [
      "Aadhaar Card",
      "Ration Card",
      "Income Certificate"
    ]
  }
  ```

### 3.4 Retrieve Scheme Eligibility Rules & Application Process
- **URL:** `GET /api/agent/v1/schemes/{scheme_id}/eligibility/`
- **Example Response (200 OK):**
  ```json
  {
    "id": "health-001",
    "title": "Ayushman Bharat PM-JAY",
    "category": "Health",
    "eligibility_criteria": [
      "Resident citizen",
      "Annual income within specified cap"
    ],
    "eligibility_rules": {
      "max_income": 300000,
      "resident": true
    },
    "application_process": [
      "1. Verify eligibility using portal checker",
      "2. Prepare draft application with verified identity details",
      "3. Upload self-attested documents",
      "4. Submit and track verification status"
    ]
  }
  ```

---

## 4. Citizen Delegation Flow

Before the agent can access any private citizen endpoints, the citizen must authorize delegation.

### Step 1: Citizen OTP Login
The citizen verifies their phone number via standard OTP flow:
```http
POST /api/auth/verify-otp/
Content-Type: application/json

{ "mobile": "9876543210", "otp": "123456" }
```
Response contains the citizen's session token (`token`).

### Step 2: Granting Delegation to YojanaSaathi Agent
The citizen generates a scoped delegation token:
```http
POST /api/auth/agent-delegation/
Authorization: Token <citizen_token>
Content-Type: application/json

{
  "duration_hours": 24,
  "scopes": [
    "applications:read",
    "applications:draft",
    "notifications:read"
  ]
}
```
**Response (201 Created):**
```json
{
  "message": "YojanaSaathi AI delegation granted successfully.",
  "delegation_id": "c1f7b889-1234-4567-89ab-cdef01234567",
  "delegation_token": "yjs_del_X9kL2pQm4Rt8Wv...",
  "scopes": ["applications:read", "applications:draft", "notifications:read"],
  "expires_at": "2026-10-10T09:30:00Z"
}
```

The citizen provides this `delegation_token` to their conversational AI session.

---

## 5. Private Citizen Endpoints (On Behalf of Authorized Citizen)

*Requires both `X-Agent-API-Key` and `X-Citizen-Delegation-Token`.*

### 5.1 Create or Update Draft Application
- **URL:** `POST /api/agent/v1/citizen/applications/draft/`
- **Required Scope:** `applications:draft`
- **Request Body:**
  ```json
  {
    "scheme_id": "health-001",
    "form_data": {
      "full_name": "Rajesh Kumar",
      "annual_income": "240000",
      "district": "Bengaluru Urban"
    }
  }
  ```
- **Response (201 Created / 200 OK):**
  ```json
  {
    "message": "Draft application created successfully.",
    "application": {
      "application_number": "YJS-A1B2C3D4E5",
      "scheme_id": "health-001",
      "scheme_title": "Ayushman Bharat PM-JAY",
      "scheme_category": "Health",
      "form_data": {
        "full_name": "Rajesh Kumar",
        "annual_income": "240000",
        "district": "Bengaluru Urban"
      },
      "status": "DRAFT",
      "status_label": "Draft",
      "next_step": "Complete your application form and upload the required documents, then submit.",
      "submitted_at": null,
      "created_at": "2026-10-09T09:40:00Z",
      "updated_at": "2026-10-09T09:40:00Z",
      "documents_count": 0,
      "verified_documents_count": 0,
      "total_required_documents_count": 2,
      "all_documents_verified": false
    }
  }
  ```

### 5.2 Retrieve Citizen Applications & Statuses
- **URL:** `GET /api/agent/v1/citizen/applications/`
- **Required Scope:** `applications:read`
- **Response (200 OK):**
  ```json
  {
    "count": 1,
    "citizen_mobile": "XXXXXX4321",
    "results": [
      {
        "application_number": "YJS-A1B2C3D4E5",
        "scheme_id": "health-001",
        "scheme_title": "Ayushman Bharat PM-JAY",
        "scheme_category": "Health",
        "status": "SUBMITTED",
        "status_label": "Submitted",
        "next_step": "Your application has been received and is awaiting review. No action needed.",
        "submitted_at": "2026-10-09T09:45:00Z",
        "created_at": "2026-10-09T09:40:00Z",
        "updated_at": "2026-10-09T09:45:00Z",
        "documents_count": 2,
        "verified_documents_count": 1,
        "total_required_documents_count": 2,
        "all_documents_verified": false
      }
    ]
  }
  ```

### 5.3 Retrieve Specific Application Details
- **URL:** `GET /api/agent/v1/citizen/applications/{application_number}/`
- **Required Scope:** `applications:read`
- **Response (200 OK):** Full detail of the application.
- **Security:** Returns 404 if the application belongs to another citizen.

### 5.4 Retrieve Document Verification Statuses
- **URL:** `GET /api/agent/v1/citizen/applications/{application_number}/documents/`
- **Required Scope:** `applications:read`
- **Response (200 OK):**
  ```json
  {
    "application_number": "YJS-A1B2C3D4E5",
    "total_documents": 2,
    "verified_documents": 1,
    "results": [
      {
        "id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
        "document_type": "Aadhaar Card",
        "file_name": "aadhaar_masked.pdf",
        "file_size": 1048576,
        "verification_status": "VERIFIED",
        "remarks": "Document verified successfully.",
        "uploaded_at": "2026-10-09T09:42:00Z",
        "verified_at": "2026-10-09T09:44:00Z"
      },
      {
        "id": "e2c3d4e5-4a5b-6c7d-8e9f-0a1b2c3d4e5f",
        "document_type": "Ration Card",
        "file_name": "ration_card.jpg",
        "file_size": 524288,
        "verification_status": "UNDER_REVIEW",
        "remarks": "",
        "uploaded_at": "2026-10-09T09:43:00Z",
        "verified_at": null
      }
    ]
  }
  ```

### 5.5 Retrieve Application History & Lifecycle
- **URL:** `GET /api/agent/v1/citizen/applications/{application_number}/history/`
- **Required Scope:** `applications:read`
- **Response (200 OK):** Complete timeline of submissions and status events.

### 5.6 Retrieve Citizen Notifications
- **URL:** `GET /api/agent/v1/citizen/notifications/`
- **Required Scope:** `notifications:read`
- **Response (200 OK):** List of relevant updates (e.g. document verified, corrections required).

---

## 6. Error Responses & Status Codes

All errors return a predictable JSON payload:

```json
{
  "error": "Human readable error message",
  "code": "STANDARD_ERROR_CODE"
}
```

| HTTP Status | Error Code | Meaning |
|---|---|---|
| **401 Unauthorized** | `AGENT_AUTHENTICATION_REQUIRED` | Missing or invalid `X-Agent-API-Key`. |
| **401 Unauthorized** | `AGENT_AUTHENTICATION_FAILED` | Key not recognized or revoked. |
| **403 Forbidden** | `DELEGATION_TOKEN_REQUIRED` | Missing `X-Citizen-Delegation-Token` for private endpoint. |
| **403 Forbidden** | `DELEGATION_TOKEN_INVALID` | Citizen delegation has expired or been revoked. |
| **403 Forbidden** | `DELEGATION_SCOPE_INSUFFICIENT` | Delegation does not include the required scope for this operation. |
| **404 Not Found** | `SCHEME_NOT_FOUND` | Specified scheme ID does not exist. |
| **404 Not Found** | `APPLICATION_NOT_FOUND` | Application does not exist or belongs to another citizen (isolated). |
| **429 Too Many Requests** | `THROTTLED` | Rate limit exceeded. |

---

## 7. Key Management CLI

Manage keys directly on the backend server:

```bash
# 1. Create a new key
python manage.py manage_agent_keys create --name "Production YojanaSaathi Agent"

# 2. List all existing keys and their status
python manage.py manage_agent_keys list

# 3. Rotate key (generates new key and immediately revokes old key)
python manage.py manage_agent_keys rotate --old-prefix yjs_ag_1234abc --name "Rotated Agent Key"

# 4. Revoke a compromised or retired key
python manage.py manage_agent_keys revoke --prefix yjs_ag_1234abc
```

---

## 8. Interactive Documentation & OpenAPI Spec

Interactive Swagger UI is available at:
`https://api.yojanasaathi.gov.in/api/agent/v1/docs/`

Raw OpenAPI 3.0 specification available at:
`https://api.yojanasaathi.gov.in/api/agent/v1/openapi.json`
Local files:
- `backend/docs/openapi-yojanasaathi-agent.json`
- `backend/docs/openapi-yojanasaathi-agent.yaml`
