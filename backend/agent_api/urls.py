import json
from pathlib import Path
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import path

from .views import (
    agent_citizen_application_detail,
    agent_citizen_application_documents,
    agent_citizen_application_history,
    agent_citizen_applications,
    agent_citizen_notifications,
    agent_create_or_update_draft,
    agent_scheme_detail,
    agent_scheme_eligibility,
    agent_scheme_list,
    agent_scheme_requirements,
)


def agent_openapi_json(request):
    """
    Returns the OpenAPI 3.0 specification for YojanaSaathi Agent API.
    """
    spec_path = settings.BASE_DIR / "docs" / "openapi-yojanasaathi-agent.json"
    if spec_path.exists():
        with open(spec_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Dynamically set host/url based on incoming request if needed
            host = request.get_host()
            scheme = "https" if request.is_secure() else "http"
            data["servers"] = [
                {"url": f"{scheme}://{host}/api/agent/v1", "description": "Current Server Host"},
                {"url": "https://api.yojanasaathi.gov.in/api/agent/v1", "description": "Production Server Placeholder"}
            ]
            return JsonResponse(data)
    return JsonResponse({"error": "OpenAPI specification not found."}, status=404)


def agent_api_docs(request):
    """
    Renders Swagger UI / Interactive documentation for the Agent API.
    """
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>YojanaSaathi AI Agent API Documentation</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css" />
  <style>
    body { margin: 0; background: #0f172a; font-family: system-ui, -apple-system, sans-serif; }
    .topbar { background: #1e293b; color: white; padding: 14px 24px; border-bottom: 1px solid #334155; display: flex; align-items: center; justify-content: space-between; }
    .topbar h1 { margin: 0; font-size: 1.15rem; font-weight: 600; color: #38bdf8; }
    .topbar span { font-size: 0.85rem; color: #94a3b8; }
    .swagger-ui .topbar { display: none; }
    .swagger-ui { filter: invert(88%) hue-rotate(180deg); }
    .swagger-ui .wrapper { max-width: 1200px; padding: 20px; }
  </style>
</head>
<body>
  <div class="topbar">
    <h1>YojanaSaathi AI Agent — Public REST API (v1)</h1>
    <span>Machine-to-Machine Secure Interface</span>
  </div>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js" charset="UTF-8"></script>
  <script>
    window.onload = function() {
      SwaggerUIBundle({
        url: "/api/agent/v1/openapi.json",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout"
      });
    };
  </script>
</body>
</html>"""
    return HttpResponse(html, content_type="text/html")


urlpatterns = [
    # OpenAPI Spec and Interactive Docs
    path("docs/", agent_api_docs, name="agent-api-docs"),
    path("openapi.json", agent_openapi_json, name="agent-openapi-json"),

    # Public Scheme APIs (M2M Agent Key authenticated)
    path("schemes/", agent_scheme_list, name="agent-scheme-list"),
    path("schemes/<str:scheme_id>/", agent_scheme_detail, name="agent-scheme-detail"),
    path("schemes/<str:scheme_id>/requirements/", agent_scheme_requirements, name="agent-scheme-requirements"),
    path("schemes/<str:scheme_id>/eligibility/", agent_scheme_eligibility, name="agent-scheme-eligibility"),

    # Citizen Operations (Agent Key + Citizen Delegation Token authenticated)
    path("citizen/applications/draft/", agent_create_or_update_draft, name="agent-draft-application"),
    path("citizen/applications/", agent_citizen_applications, name="agent-citizen-applications"),
    path("citizen/applications/<str:application_number>/", agent_citizen_application_detail, name="agent-citizen-app-detail"),
    path("citizen/applications/<str:application_number>/documents/", agent_citizen_application_documents, name="agent-citizen-app-documents"),
    path("citizen/applications/<str:application_number>/history/", agent_citizen_application_history, name="agent-citizen-app-history"),
    path("citizen/notifications/", agent_citizen_notifications, name="agent-citizen-notifications"),
]
