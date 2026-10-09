from django.utils import timezone
from rest_framework import exceptions
from rest_framework.permissions import BasePermission

from .models import CitizenAgentDelegation


class IsAgentAuthenticated(BasePermission):
    """
    Allows access only to authenticated machine-to-machine AI Agents.
    Rejects citizens, anonymous users, or invalid agent keys.
    """

    message = {
        "error": "Machine-to-machine Agent authentication is required. Provide a valid 'X-Agent-API-Key'.",
        "code": "AGENT_AUTHENTICATION_REQUIRED",
    }

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        return bool(user and getattr(user, "is_agent", False) and user.is_authenticated)


class HasCitizenDelegation(BasePermission):
    """
    Enforces citizen consent and short-lived delegation for private citizen operations.
    Requires:
      1. Machine-to-machine Agent authentication (IsAgentAuthenticated).
      2. Valid, active, non-expired 'X-Citizen-Delegation-Token' header.
      3. Token must contain required scope for the view action.
    """

    HEADER_NAME = "HTTP_X_CITIZEN_DELEGATION_TOKEN"

    def has_permission(self, request, view):
        # 1. First ensure agent itself is authenticated
        agent_user = getattr(request, "user", None)
        if not (agent_user and getattr(agent_user, "is_agent", False) and agent_user.is_authenticated):
            raise exceptions.AuthenticationFailed({
                "error": "Agent authentication required before presenting delegation token.",
                "code": "AGENT_AUTHENTICATION_REQUIRED",
            })

        # 2. Extract citizen delegation token
        token_str = (
            request.headers.get("X-Citizen-Delegation-Token")
            or request.META.get(self.HEADER_NAME)
        )
        if not token_str:
            raise exceptions.PermissionDenied({
                "error": "Citizen delegation token is required in 'X-Citizen-Delegation-Token' header for private citizen endpoints.",
                "code": "DELEGATION_TOKEN_REQUIRED",
            })

        token_str = token_str.strip()

        # 3. Lookup delegation record
        delegation = CitizenAgentDelegation.objects.filter(
            delegation_token=token_str
        ).select_related("citizen", "citizen__user").first()

        if not delegation or not delegation.is_valid():
            raise exceptions.PermissionDenied({
                "error": "Citizen delegation token is invalid, expired, or has been revoked.",
                "code": "DELEGATION_TOKEN_INVALID",
            })

        # 4. Check scope if view or permission class defines required_scope
        required_scope = getattr(self, "required_scope", None) or getattr(view, "required_scope", None)
        if required_scope and not delegation.has_scope(required_scope):
            raise exceptions.PermissionDenied({
                "error": f"Citizen delegation does not permit scope '{required_scope}'.",
                "code": "DELEGATION_SCOPE_INSUFFICIENT",
            })

        # 5. Update last used and attach to request
        delegation.last_used_at = timezone.now()
        delegation.save(update_fields=["last_used_at"])

        request.delegation = delegation
        request.delegated_citizen = delegation.citizen
        return True
