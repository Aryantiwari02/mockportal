import secrets
from django.conf import settings
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from .models import AgentApiKey


class AgentPrincipal:
    """
    Principal representation for an authenticated machine-to-machine AI Agent.
    Implements standard Django User-like interface for DRF compatibility.
    """

    def __init__(self, name: str, prefix: str, key_id=None):
        self.name = name
        self.prefix = prefix
        self.key_id = key_id
        self.is_agent = True
        self.is_authenticated = True
        self.is_staff = False
        self.is_superuser = False
        self.username = f"agent_{prefix}"

    def __str__(self):
        return f"Agent({self.name} [{self.prefix}])"

    def __repr__(self):
        return f"<AgentPrincipal: {self.name}>"


class AgentApiKeyAuthentication(BaseAuthentication):
    """
    Dedicated authentication class for YojanaSaathi AI Agent.
    Authenticates requests via 'X-Agent-API-Key' header or Bearer/AgentKey Authorization.
    """

    HEADER_NAME = "HTTP_X_AGENT_API_KEY"

    def authenticate(self, request):
        raw_key = self.extract_key(request)
        if not raw_key:
            return None

        # 1. Check against active Database AgentApiKey records
        incoming_hash = AgentApiKey.hash_key(raw_key)
        key_record = AgentApiKey.objects.filter(
            hashed_key=incoming_hash,
            is_active=True,
            revoked_at__isnull=True,
        ).first()

        if key_record:
            # Update last used timestamp
            key_record.last_used_at = timezone.now()
            key_record.save(update_fields=["last_used_at"])

            principal = AgentPrincipal(
                name=key_record.name,
                prefix=key_record.key_prefix,
                key_id=key_record.id,
            )
            return (principal, key_record)

        # 2. Check against environment variable fallback (YOJANASAATHI_AGENT_API_KEY)
        env_key = getattr(settings, "YOJANASAATHI_AGENT_API_KEY", "")
        if env_key and isinstance(env_key, str) and len(env_key) >= 16:
            if secrets.compare_digest(raw_key.strip(), env_key.strip()):
                principal = AgentPrincipal(
                    name="YojanaSaathi Env Agent",
                    prefix=env_key[:14],
                    key_id=None,
                )
                return (principal, "env_key")

        # If key was provided but neither matched
        raise exceptions.AuthenticationFailed({
            "error": "Invalid or revoked Agent API Key.",
            "code": "AGENT_AUTHENTICATION_FAILED",
        })

    def extract_key(self, request) -> str:
        # 1. Custom header: X-Agent-API-Key
        key = request.headers.get("X-Agent-API-Key") or request.META.get(self.HEADER_NAME)
        if key:
            return key.strip()

        # 2. Authorization header fallback
        auth_header = request.headers.get("Authorization") or request.META.get("HTTP_AUTHORIZATION", "")
        if auth_header:
            parts = auth_header.strip().split()
            if len(parts) == 2:
                prefix_type, token = parts[0].lower(), parts[1]
                if prefix_type in ("agentkey", "agent"):
                    return token.strip()
                if prefix_type == "bearer" and token.startswith("yjs_ag_"):
                    return token.strip()

        return None

    def authenticate_header(self, request):
        return 'X-Agent-API-Key realm="YojanaSaathi Agent API"'
