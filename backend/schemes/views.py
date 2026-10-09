from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Scheme
from .serializers import SchemeSerializer


def api_status(request):
    return JsonResponse({
        "status": "success",
        "message": "Government Yojana Portal API is running",
        "project": "Government Yojana Portal"
    })


def health_check(request):
    """Lightweight uptime probe used by hosting platforms / monitors."""
    return JsonResponse({"status": "ok"})


def robots_txt(request):
    return HttpResponse(
        "User-agent: *\nDisallow: /admin/\nDisallow: /media/\n",
        content_type="text/plain",
    )


def _frontend_url():
    """Best available public URL of the frontend portal (for links)."""
    origins = getattr(settings, "CORS_ALLOWED_ORIGINS", []) or []

    for origin in origins:
        if "localhost" not in origin and "127.0.0.1" not in origin:
            return origin

    return origins[0] if origins else ""


def root_landing(request):
    """Friendly landing page for the API root instead of a bare 404."""
    base = request.build_absolute_uri("/")
    frontend = _frontend_url()

    links = [
        ("API status", base + "api/status/"),
        ("Schemes API", base + "api/schemes/"),
        ("AI agent documentation", base + "api/agent/v1/docs/"),
        ("Admin", base + "admin/"),
    ]

    if frontend:
        links.insert(0, ("Citizen portal", frontend))

    items = "\n".join(
        f'      <li><a href="{url}">{label}</a>'
        f'<span class="url">{url}</span></li>'
        for label, url in links
    )

    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>YojanaSaathi API</title>
    <style>
      body {{
        margin: 0;
        font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
        background: #f4f6fb;
        color: #1f2937;
        display: flex;
        min-height: 100vh;
        align-items: center;
        justify-content: center;
      }}
      .card {{
        background: #fff;
        max-width: 640px;
        width: calc(100% - 2rem);
        margin: 2rem;
        padding: 2rem;
        border-radius: 14px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
      }}
      h1 {{ margin: 0 0 0.25rem; font-size: 1.5rem; }}
      p.lead {{ margin: 0 0 1.5rem; color: #6b7280; }}
      ul {{ list-style: none; padding: 0; margin: 0; }}
      li {{
        padding: 0.75rem 0;
        border-top: 1px solid #eef1f6;
        display: flex;
        flex-direction: column;
        gap: 0.15rem;
      }}
      a {{ color: #1d4ed8; font-weight: 600; text-decoration: none; }}
      a:hover {{ text-decoration: underline; }}
      .url {{ color: #9ca3af; font-size: 0.8rem; word-break: break-all; }}
      .ok {{ color: #047857; font-weight: 600; }}
    </style>
  </head>
  <body>
    <main class="card">
      <h1>YojanaSaathi API</h1>
      <p class="lead">
        Government Yojana Portal backend is <span class="ok">running</span>.
        This is an API service &mdash; use the citizen portal for the interface.
      </p>
      <ul>
{items}
      </ul>
    </main>
  </body>
</html>
"""

    return HttpResponse(html)


@api_view(["GET"])
def scheme_list(request):
    schemes = Scheme.objects.all()

    # Search
    search_query = request.GET.get("q", "").strip()

    if search_query:
        schemes = schemes.filter(
            Q(title__icontains=search_query)
            | Q(short_description__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(category__icontains=search_query)
        )

    # Category filter
    category = request.GET.get("category", "").strip()

    if category and category.lower() != "all":
        schemes = schemes.filter(
            category__iexact=category
        )

    schemes = schemes.order_by("category", "title")

    serializer = SchemeSerializer(schemes, many=True)

    return Response({
        "count": schemes.count(),
        "results": serializer.data
    })


@api_view(["GET"])
def scheme_detail(request, scheme_id):
    try:
        scheme = Scheme.objects.get(id=scheme_id)
    except Scheme.DoesNotExist:
        return Response(
            {"error": "Scheme not found"},
            status=404
        )

    serializer = SchemeSerializer(scheme)

    return Response(serializer.data)