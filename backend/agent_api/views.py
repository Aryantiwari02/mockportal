from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Citizen
from applications.models import Application, Notification
from applications.serializers import _STATUS_NEXT_STEP
from schemes.models import Scheme

from .authentication import AgentApiKeyAuthentication
from .models import AgentAuditLog, CitizenAgentDelegation
from .permissions import HasCitizenDelegation, IsAgentAuthenticated
from .serializers import (
    AgentApplicationDetailSerializer,
    AgentApplicationSummarySerializer,
    AgentDocumentVerificationStatusSerializer,
    AgentDraftApplicationInputSerializer,
    AgentNotificationSerializer,
    AgentSchemeDetailSerializer,
    AgentSchemeEligibilitySerializer,
    AgentSchemeRequirementsSerializer,
    AgentSchemeSummarySerializer,
    CitizenAgentDelegationSerializer,
    CreateCitizenDelegationSerializer,
)
from .throttling import AgentPublicRateThrottle, AgentRateThrottle


def log_agent_access(request, action: str, status_code: int):
    """
    Structured audit logging for machine-to-machine AI agent requests.
    Never logs secret credentials or PII payload.
    """
    try:
        agent_user = getattr(request, "user", None)
        key_name = getattr(agent_user, "name", "")
        key_prefix = getattr(agent_user, "prefix", "")
        citizen = getattr(request, "delegated_citizen", None)

        ip = request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR") or ""
        if ip and "," in ip:
            ip = ip.split(",")[0].strip()

        AgentAuditLog.objects.create(
            agent_key_name=key_name,
            agent_key_prefix=key_prefix,
            citizen=citizen,
            action=action,
            endpoint=request.path,
            method=request.method,
            status_code=status_code,
            ip_address=ip[:60],
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:255],
        )
    except Exception:
        # Logging failures must not interrupt core API operations
        pass


# ============================================================
# PUBLIC SCHEME ENDPOINTS (Agent authenticated, no citizen delegation required)
# ============================================================

@api_view(["GET"])
@authentication_classes([AgentApiKeyAuthentication])
@permission_classes([IsAgentAuthenticated])
@throttle_classes([AgentPublicRateThrottle])
def agent_scheme_list(request):
    """
    List and search schemes for YojanaSaathi AI agent.
    Supports ?q= query and ?category= filter.
    """
    schemes = Scheme.objects.all()

    search_query = request.GET.get("q", "").strip()
    if search_query:
        schemes = schemes.filter(
            Q(title__icontains=search_query)
            | Q(short_description__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(category__icontains=search_query)
        )

    category = request.GET.get("category", "").strip()
    if category and category.lower() != "all":
        schemes = schemes.filter(category__iexact=category)

    schemes = schemes.order_by("category", "title")
    serializer = AgentSchemeSummarySerializer(schemes, many=True)

    log_agent_access(request, "schemes_list", status.HTTP_200_OK)
    return Response({
        "count": schemes.count(),
        "results": serializer.data,
    })


@api_view(["GET"])
@authentication_classes([AgentApiKeyAuthentication])
@permission_classes([IsAgentAuthenticated])
@throttle_classes([AgentPublicRateThrottle])
def agent_scheme_detail(request, scheme_id):
    """
    Retrieve full scheme details including descriptions, benefits, and process.
    """
    try:
        scheme = Scheme.objects.get(id=scheme_id)
    except Scheme.DoesNotExist:
        log_agent_access(request, "scheme_detail_not_found", status.HTTP_404_NOT_FOUND)
        return Response(
            {"error": "Scheme not found.", "code": "SCHEME_NOT_FOUND"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = AgentSchemeDetailSerializer(scheme)
    log_agent_access(request, "scheme_detail", status.HTTP_200_OK)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([AgentApiKeyAuthentication])
@permission_classes([IsAgentAuthenticated])
@throttle_classes([AgentPublicRateThrottle])
def agent_scheme_requirements(request, scheme_id):
    """
    Retrieve scheme-specific form fields and required documents.
    """
    try:
        scheme = Scheme.objects.get(id=scheme_id)
    except Scheme.DoesNotExist:
        log_agent_access(request, "scheme_requirements_not_found", status.HTTP_404_NOT_FOUND)
        return Response(
            {"error": "Scheme not found.", "code": "SCHEME_NOT_FOUND"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = AgentSchemeRequirementsSerializer(scheme)
    log_agent_access(request, "scheme_requirements", status.HTTP_200_OK)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([AgentApiKeyAuthentication])
@permission_classes([IsAgentAuthenticated])
@throttle_classes([AgentPublicRateThrottle])
def agent_scheme_eligibility(request, scheme_id):
    """
    Retrieve eligibility rules, criteria, and application instructions.
    """
    try:
        scheme = Scheme.objects.get(id=scheme_id)
    except Scheme.DoesNotExist:
        log_agent_access(request, "scheme_eligibility_not_found", status.HTTP_404_NOT_FOUND)
        return Response(
            {"error": "Scheme not found.", "code": "SCHEME_NOT_FOUND"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = AgentSchemeEligibilitySerializer(scheme)
    log_agent_access(request, "scheme_eligibility", status.HTTP_200_OK)
    return Response(serializer.data)


# ============================================================
# PRIVATE CITIZEN OPERATIONS (Agent Key + Citizen Delegation Required)
# ============================================================

class ScopedDraftPermission(HasCitizenDelegation):
    required_scope = "applications:draft"


class ScopedReadPermission(HasCitizenDelegation):
    required_scope = "applications:read"


class ScopedNotificationsPermission(HasCitizenDelegation):
    required_scope = "notifications:read"


@api_view(["POST"])
@authentication_classes([AgentApiKeyAuthentication])
@permission_classes([ScopedDraftPermission])
@throttle_classes([AgentRateThrottle])
def agent_create_or_update_draft(request):
    """
    Create or update a draft application on behalf of an authorized citizen.
    Requires:
      - Valid Agent API Key
      - Valid Citizen Delegation Token with 'applications:draft' scope
    Guarantees:
      - Only operates on the citizen identified by delegation.
      - Cannot submit or alter submitted/approved applications.
      - Never allows document approval or bypass of citizen consent.
    """
    citizen = request.delegated_citizen

    serializer = AgentDraftApplicationInputSerializer(data=request.data)
    if not serializer.is_valid():
        log_agent_access(request, "draft_application_invalid_input", status.HTTP_400_BAD_REQUEST)
        return Response(
            {"error": serializer.errors, "code": "INVALID_INPUT"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    scheme_id = serializer.validated_data["scheme_id"]
    incoming_form_data = serializer.validated_data.get("form_data", {})

    try:
        scheme = Scheme.objects.get(id=scheme_id)
    except Scheme.DoesNotExist:
        log_agent_access(request, "draft_application_scheme_not_found", status.HTTP_404_NOT_FOUND)
        return Response(
            {"error": "Scheme not found.", "code": "SCHEME_NOT_FOUND"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check for existing draft for this citizen and scheme
    existing_draft = Application.objects.filter(
        citizen=citizen,
        scheme=scheme,
        status="DRAFT",
    ).first()

    if existing_draft:
        if incoming_form_data:
            current_data = existing_draft.form_data or {}
            current_data.update(incoming_form_data)
            existing_draft.form_data = current_data
            existing_draft.save(update_fields=["form_data", "updated_at"])

        output_serializer = AgentApplicationDetailSerializer(existing_draft)
        log_agent_access(request, "draft_application_updated", status.HTTP_200_OK)
        return Response(
            {
                "message": "Draft application updated successfully.",
                "application": output_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # Create new draft
    application = Application.objects.create(
        citizen=citizen,
        scheme=scheme,
        form_data=incoming_form_data,
        status="DRAFT",
    )

    output_serializer = AgentApplicationDetailSerializer(application)
    log_agent_access(request, "draft_application_created", status.HTTP_201_CREATED)
    return Response(
        {
            "message": "Draft application created successfully.",
            "application": output_serializer.data,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@authentication_classes([AgentApiKeyAuthentication])
@permission_classes([ScopedReadPermission])
@throttle_classes([AgentRateThrottle])
def agent_citizen_applications(request):
    """
    Retrieve all applications and statuses for the delegated citizen.
    Guarantees isolation: strictly returns records belonging to request.delegated_citizen.
    """
    citizen = request.delegated_citizen

    applications = (
        Application.objects
        .filter(citizen=citizen)
        .select_related("scheme")
        .prefetch_related("documents")
        .order_by("-created_at")
    )

    serializer = AgentApplicationSummarySerializer(applications, many=True)
    log_agent_access(request, "citizen_applications_list", status.HTTP_200_OK)
    return Response({
        "count": applications.count(),
        "citizen_mobile": citizen.mobile[-4:].rjust(10, "X"),  # Masked PII
        "results": serializer.data,
    })


@api_view(["GET"])
@authentication_classes([AgentApiKeyAuthentication])
@permission_classes([ScopedReadPermission])
@throttle_classes([AgentRateThrottle])
def agent_citizen_application_detail(request, application_number):
    """
    Retrieve application details for a specific application of the delegated citizen.
    Returns 404 if application doesn't exist or belongs to another citizen.
    """
    citizen = request.delegated_citizen

    try:
        application = (
            Application.objects
            .select_related("scheme")
            .prefetch_related("documents")
            .get(
                application_number=application_number,
                citizen=citizen,
            )
        )
    except Application.DoesNotExist:
        log_agent_access(request, "citizen_application_not_found", status.HTTP_404_NOT_FOUND)
        return Response(
            {"error": "Application not found or not accessible under current delegation.", "code": "APPLICATION_NOT_FOUND"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = AgentApplicationDetailSerializer(application)
    log_agent_access(request, "citizen_application_detail", status.HTTP_200_OK)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([AgentApiKeyAuthentication])
@permission_classes([ScopedReadPermission])
@throttle_classes([AgentRateThrottle])
def agent_citizen_application_documents(request, application_number):
    """
    Retrieve document verification statuses for the delegated citizen's application.
    Security: Exposes verification status and remarks, but never exposes raw file downloads.
    """
    citizen = request.delegated_citizen

    try:
        application = Application.objects.get(
            application_number=application_number,
            citizen=citizen,
        )
    except Application.DoesNotExist:
        log_agent_access(request, "documents_application_not_found", status.HTTP_404_NOT_FOUND)
        return Response(
            {"error": "Application not found or not accessible under current delegation.", "code": "APPLICATION_NOT_FOUND"},
            status=status.HTTP_404_NOT_FOUND,
        )

    documents = application.documents.all()
    serializer = AgentDocumentVerificationStatusSerializer(documents, many=True)

    log_agent_access(request, "application_documents_status", status.HTTP_200_OK)
    return Response({
        "application_number": application.application_number,
        "total_documents": documents.count(),
        "verified_documents": documents.filter(verification_status="VERIFIED").count(),
        "results": serializer.data,
    })


@api_view(["GET"])
@authentication_classes([AgentApiKeyAuthentication])
@permission_classes([ScopedReadPermission])
@throttle_classes([AgentRateThrottle])
def agent_citizen_application_history(request, application_number):
    """
    Retrieve application status lifecycle, submission timestamps, and event history.
    """
    citizen = request.delegated_citizen

    try:
        application = (
            Application.objects
            .select_related("scheme")
            .get(
                application_number=application_number,
                citizen=citizen,
            )
        )
    except Application.DoesNotExist:
        log_agent_access(request, "history_application_not_found", status.HTTP_404_NOT_FOUND)
        return Response(
            {"error": "Application not found or not accessible under current delegation.", "code": "APPLICATION_NOT_FOUND"},
            status=status.HTTP_404_NOT_FOUND,
        )

    notifications = Notification.objects.filter(
        citizen=citizen,
        application=application,
    ).order_by("-created_at")
    notif_serializer = AgentNotificationSerializer(notifications, many=True)

    status_history = {
        "application_number": application.application_number,
        "scheme_id": application.scheme.id,
        "scheme_title": application.scheme.title,
        "current_status": application.status,
        "status_label": dict(Application.STATUS_CHOICES).get(application.status, application.status),
        "next_step": _STATUS_NEXT_STEP.get(application.status, ""),
        "created_at": application.created_at,
        "submitted_at": application.submitted_at,
        "updated_at": application.updated_at,
        "documents_summary": {
            "total_uploaded": application.documents_count,
            "verified": application.verified_documents_count,
            "required": application.total_required_documents_count,
            "all_verified": application.all_documents_verified,
        },
        "lifecycle_events": notif_serializer.data,
    }

    log_agent_access(request, "application_history", status.HTTP_200_OK)
    return Response(status_history)


@api_view(["GET"])
@authentication_classes([AgentApiKeyAuthentication])
@permission_classes([ScopedNotificationsPermission])
@throttle_classes([AgentRateThrottle])
def agent_citizen_notifications(request):
    """
    Retrieve notifications and alerts for the delegated citizen.
    """
    citizen = request.delegated_citizen

    notes = Notification.objects.filter(citizen=citizen).order_by("-created_at")
    serializer = AgentNotificationSerializer(notes, many=True)

    log_agent_access(request, "citizen_notifications", status.HTTP_200_OK)
    return Response({
        "count": notes.count(),
        "unread_count": notes.filter(is_read=False).count(),
        "results": serializer.data,
    })


# ============================================================
# CITIZEN DELEGATION MANAGEMENT (Called by Citizen via DRF Token)
# ============================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def citizen_create_delegation(request):
    """
    Citizen consent endpoint: Authenticated citizen grants a short-lived,
    scoped delegation token to YojanaSaathi AI Agent.
    """
    try:
        citizen = request.user.citizen_profile
    except Citizen.DoesNotExist:
        return Response(
            {"error": "Citizen profile not found.", "code": "CITIZEN_NOT_FOUND"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = CreateCitizenDelegationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {"error": serializer.errors, "code": "INVALID_INPUT"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    duration_hours = serializer.validated_data.get("duration_hours", 24)
    scopes = serializer.validated_data.get("scopes")

    delegation = CitizenAgentDelegation.create_delegation(
        citizen=citizen,
        scopes=scopes,
        duration_hours=duration_hours,
    )

    return Response(
        {
            "message": "YojanaSaathi AI delegation granted successfully.",
            "delegation_id": delegation.id,
            "delegation_token": delegation.delegation_token,
            "scopes": delegation.scopes,
            "expires_at": delegation.expires_at,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def citizen_list_delegations(request):
    """
    List all delegation grants for the authenticated citizen.
    """
    try:
        citizen = request.user.citizen_profile
    except Citizen.DoesNotExist:
        return Response(
            {"error": "Citizen profile not found.", "code": "CITIZEN_NOT_FOUND"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    delegations = CitizenAgentDelegation.objects.filter(citizen=citizen).order_by("-created_at")
    serializer = CitizenAgentDelegationSerializer(delegations, many=True)

    return Response({
        "count": delegations.count(),
        "results": serializer.data,
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def citizen_revoke_delegation(request, delegation_id):
    """
    Citizen revoke endpoint: Instantly revokes a delegation token.
    """
    try:
        citizen = request.user.citizen_profile
    except Citizen.DoesNotExist:
        return Response(
            {"error": "Citizen profile not found.", "code": "CITIZEN_NOT_FOUND"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        delegation = CitizenAgentDelegation.objects.get(
            id=delegation_id,
            citizen=citizen,
        )
    except CitizenAgentDelegation.DoesNotExist:
        return Response(
            {"error": "Delegation not found.", "code": "DELEGATION_NOT_FOUND"},
            status=status.HTTP_404_NOT_FOUND,
        )

    delegation.revoke()

    return Response(
        {"message": "YojanaSaathi delegation revoked successfully."},
        status=status.HTTP_200_OK,
    )
