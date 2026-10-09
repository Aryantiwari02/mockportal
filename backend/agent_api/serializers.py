from rest_framework import serializers

from accounts.models import Citizen
from applications.models import Application, ApplicationDocument, Notification
from applications.serializers import _STATUS_NEXT_STEP
from schemes.models import Scheme

from .models import AgentApiKey, CitizenAgentDelegation


# ============================================================
# SCHEMES SERIALIZERS
# ============================================================

class AgentSchemeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme
        fields = [
            "id",
            "category",
            "title",
            "short_description",
            "benefits",
            "eligibility",
            "updated_at",
        ]


class AgentSchemeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme
        fields = [
            "id",
            "category",
            "title",
            "short_description",
            "description",
            "benefits",
            "documents",
            "eligibility",
            "eligibility_rules",
            "application_fields",
            "application_process",
            "translations",
            "updated_at",
        ]


class AgentSchemeRequirementsSerializer(serializers.ModelSerializer):
    required_documents = serializers.JSONField(source="documents")

    class Meta:
        model = Scheme
        fields = [
            "id",
            "title",
            "category",
            "application_fields",
            "required_documents",
        ]


class AgentSchemeEligibilitySerializer(serializers.ModelSerializer):
    eligibility_criteria = serializers.JSONField(source="eligibility")

    class Meta:
        model = Scheme
        fields = [
            "id",
            "title",
            "category",
            "eligibility_criteria",
            "eligibility_rules",
            "application_process",
        ]


# ============================================================
# CITIZEN APPLICATION SERIALIZERS (SCOPED & SAFE)
# ============================================================

class AgentDraftApplicationInputSerializer(serializers.Serializer):
    scheme_id = serializers.CharField(max_length=100, required=True)
    form_data = serializers.DictField(required=False, default=dict)


class AgentApplicationSummarySerializer(serializers.ModelSerializer):
    scheme_id = serializers.CharField(source="scheme.id", read_only=True)
    scheme_title = serializers.CharField(source="scheme.title", read_only=True)
    scheme_category = serializers.CharField(source="scheme.category", read_only=True)
    status_label = serializers.SerializerMethodField()
    next_step = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            "application_number",
            "scheme_id",
            "scheme_title",
            "scheme_category",
            "status",
            "status_label",
            "next_step",
            "submitted_at",
            "created_at",
            "updated_at",
            "documents_count",
            "verified_documents_count",
            "total_required_documents_count",
            "all_documents_verified",
        ]

    def get_status_label(self, obj):
        return dict(Application.STATUS_CHOICES).get(obj.status, obj.status)

    def get_next_step(self, obj):
        return _STATUS_NEXT_STEP.get(obj.status, "")


class AgentApplicationDetailSerializer(serializers.ModelSerializer):
    scheme_id = serializers.CharField(source="scheme.id", read_only=True)
    scheme_title = serializers.CharField(source="scheme.title", read_only=True)
    scheme_category = serializers.CharField(source="scheme.category", read_only=True)
    status_label = serializers.SerializerMethodField()
    next_step = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            "application_number",
            "scheme_id",
            "scheme_title",
            "scheme_category",
            "form_data",
            "status",
            "status_label",
            "next_step",
            "submitted_at",
            "created_at",
            "updated_at",
            "documents_count",
            "verified_documents_count",
            "total_required_documents_count",
            "all_documents_verified",
        ]
        read_only_fields = [
            "application_number",
            "scheme_id",
            "scheme_title",
            "scheme_category",
            "status",
            "status_label",
            "next_step",
            "submitted_at",
            "created_at",
            "updated_at",
            "documents_count",
            "verified_documents_count",
            "total_required_documents_count",
            "all_documents_verified",
        ]

    def get_status_label(self, obj):
        return dict(Application.STATUS_CHOICES).get(obj.status, obj.status)

    def get_next_step(self, obj):
        return _STATUS_NEXT_STEP.get(obj.status, "")


class AgentDocumentVerificationStatusSerializer(serializers.ModelSerializer):
    """
    Exposes document verification status without leaking document file path
    or enabling unauthorized download of citizen documents.
    """
    class Meta:
        model = ApplicationDocument
        fields = [
            "id",
            "document_type",
            "file_name",
            "file_size",
            "verification_status",
            "remarks",
            "uploaded_at",
            "verified_at",
        ]


class AgentNotificationSerializer(serializers.ModelSerializer):
    application_number = serializers.CharField(
        source="application.application_number",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = Notification
        fields = [
            "id",
            "application_number",
            "title",
            "message",
            "type",
            "is_read",
            "created_at",
        ]


# ============================================================
# CITIZEN DELEGATION SERIALIZERS
# ============================================================

class CitizenAgentDelegationSerializer(serializers.ModelSerializer):
    is_valid = serializers.BooleanField(read_only=True)

    class Meta:
        model = CitizenAgentDelegation
        fields = [
            "id",
            "scopes",
            "is_active",
            "is_valid",
            "expires_at",
            "created_at",
            "revoked_at",
            "last_used_at",
        ]


class CreateCitizenDelegationSerializer(serializers.Serializer):
    duration_hours = serializers.IntegerField(
        min_value=1,
        max_value=168,
        default=24,
        required=False,
        help_text="Delegation validity period in hours (1-168). Default 24.",
    )
    scopes = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=lambda: [
            "applications:read",
            "applications:draft",
            "notifications:read",
        ],
        help_text="Scopes granted to YojanaSaathi agent",
    )
