from rest_framework import serializers

from .models import Application, ApplicationDocument, Notification


class ApplicationDocumentSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationDocument
        fields = [
            "id",
            "document_type",
            "file_name",
            "file_size",
            "file_type",
            "verification_status",
            "remarks",
            "uploaded_at",
            "verified_at",
            "download_url",
        ]
        read_only_fields = [
            "id",
            "file_size",
            "file_type",
            "verification_status",
            "uploaded_at",
            "verified_at",
            "download_url",
        ]

    def get_download_url(self, obj):
        return f"/api/applications/{obj.application.application_number}/documents/{obj.id}/download/"


class ApplicationSerializer(serializers.ModelSerializer):
    scheme_title = serializers.CharField(
        source="scheme.title",
        read_only=True
    )

    scheme_category = serializers.CharField(
        source="scheme.category",
        read_only=True
    )

    documents = ApplicationDocumentSerializer(
        many=True,
        read_only=True
    )

    documents_count = serializers.IntegerField(
        read_only=True
    )

    verified_documents_count = serializers.IntegerField(
        read_only=True
    )

    total_required_documents_count = serializers.IntegerField(
        read_only=True
    )

    all_documents_verified = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = Application
        fields = [
            "id",
            "application_number",
            "citizen",
            "scheme",
            "scheme_title",
            "scheme_category",
            "form_data",
            "status",
            "submitted_at",
            "created_at",
            "updated_at",
            "documents",
            "documents_count",
            "verified_documents_count",
            "total_required_documents_count",
            "all_documents_verified",
        ]
        read_only_fields = [
            "id",
            "application_number",
            "citizen",
            "status",
            "submitted_at",
            "created_at",
            "updated_at",
            "documents",
            "documents_count",
            "verified_documents_count",
            "total_required_documents_count",
            "all_documents_verified",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    application_number = serializers.CharField(
        source="application.application_number",
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Notification
        fields = [
            "id",
            "application",
            "application_number",
            "title",
            "message",
            "type",
            "is_read",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "application",
            "application_number",
            "title",
            "message",
            "type",
            "created_at",
        ]


# ---------------------------------------------------------------
# PHASE 4 — Minimal read-only status serializer for agent access
# ---------------------------------------------------------------

_STATUS_NEXT_STEP = {
    "DRAFT": "Complete your application form and upload the required documents, then submit.",
    "SUBMITTED": "Your application has been received and is awaiting review. No action needed.",
    "UNDER_REVIEW": (
        "Your application is under departmental review. "
        "You will be notified of any updates."
    ),
    "CORRECTION_REQUIRED": (
        "Additional information or corrected documents are required. "
        "Please log in and update your application."
    ),
    "APPROVED": (
        "Your application has been approved. "
        "Benefits will be processed by the responsible department."
    ),
    "REJECTED": (
        "Your application was not approved. "
        "Please contact the relevant authority for further guidance."
    ),
}


class ApplicationStatusSerializer(serializers.ModelSerializer):
    """
    Minimal read-only serializer exposing only status-tracking fields.

    Does NOT expose: form_data, citizen PII, documents, Aadhaar, bank
    information, OTPs, internal notes, or any other sensitive personal data.

    Intended for:
      - Citizen self-service status tracking (authenticated via Token).
      - Future Phase 4 agent integration (requires separate service auth;
        see README for instructions).
    """

    scheme_title = serializers.CharField(source="scheme.title", read_only=True)
    scheme_id = serializers.CharField(source="scheme.id", read_only=True)
    status_label = serializers.SerializerMethodField()
    next_step = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            "application_number",
            "scheme_id",
            "scheme_title",
            "status",
            "status_label",
            "submitted_at",
            "updated_at",
            "next_step",
        ]
        read_only_fields = [
            "application_number",
            "scheme_id",
            "scheme_title",
            "status",
            "status_label",
            "submitted_at",
            "updated_at",
            "next_step",
        ]

    def get_status_label(self, obj):
        return dict(Application.STATUS_CHOICES).get(obj.status, obj.status)

    def get_next_step(self, obj):
        return _STATUS_NEXT_STEP.get(obj.status, "")