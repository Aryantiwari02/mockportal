from django.contrib import admin
from django.utils.html import format_html

from .models import Application, ApplicationDocument, Notification, verify_document


class ApplicationDocumentInline(admin.TabularInline):
    model = ApplicationDocument
    extra = 0
    readonly_fields = ("file_name", "file_size", "uploaded_at", "verified_at")
    fields = (
        "document_type",
        "file",
        "file_name",
        "file_size",
        "verification_status",
        "remarks",
        "uploaded_at",
        "verified_at",
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "application_number",
        "citizen",
        "scheme",
        "status",
        "documents_summary",
        "created_at",
        "submitted_at",
    )

    list_filter = (
        "status",
        "scheme",
        "created_at",
    )

    search_fields = (
        "application_number",
        "citizen__mobile",
        "citizen__full_name",
        "scheme__title",
    )

    readonly_fields = (
        "id",
        "application_number",
        "created_at",
        "updated_at",
        "submitted_at",
    )

    inlines = [ApplicationDocumentInline]

    def documents_summary(self, obj):
        verified = obj.verified_documents_count
        total = obj.documents_count
        req = obj.total_required_documents_count
        return f"{verified}/{req} Verified ({total} uploaded)"

    documents_summary.short_description = "Document Status"


@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "document_type",
        "application_link",
        "citizen_mobile",
        "scheme_title",
        "verification_status_badge",
        "uploaded_at",
        "verified_at",
    )

    list_filter = (
        "verification_status",
        "uploaded_at",
        "verified_at",
        "application__scheme",
    )

    search_fields = (
        "document_type",
        "file_name",
        "application__application_number",
        "application__citizen__mobile",
    )

    readonly_fields = (
        "id",
        "file_size",
        "file_type",
        "uploaded_at",
        "verified_at",
    )

    actions = [
        "action_mark_verified",
        "action_mark_rejected",
        "action_mark_correction_required",
    ]

    def application_link(self, obj):
        return obj.application.application_number

    application_link.short_description = "Application"

    def citizen_mobile(self, obj):
        return obj.application.citizen.mobile

    citizen_mobile.short_description = "Citizen"

    def scheme_title(self, obj):
        return obj.application.scheme.title

    scheme_title.short_description = "Scheme"

    def verification_status_badge(self, obj):
        colors = {
            "VERIFIED": "#16a34a",
            "REJECTED": "#dc2626",
            "CORRECTION_REQUIRED": "#d97706",
            "UNDER_REVIEW": "#2563eb",
            "UPLOADED": "#64748b",
        }
        color = colors.get(obj.verification_status, "#64748b")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            color,
            obj.verification_status.replace("_", " "),
        )

    verification_status_badge.short_description = "Status"

    def save_model(self, request, obj, form, change):
        if change and "verification_status" in form.changed_data:
            verify_document(
                obj,
                obj.verification_status,
                remarks=obj.remarks or "Reviewed via Django Admin"
            )
        else:
            super().save_model(request, obj, form, change)

    @admin.action(description="✓ Mark selected documents as VERIFIED (Demo Review)")
    def action_mark_verified(self, request, queryset):
        for doc in queryset:
            verify_document(doc, "VERIFIED", remarks="Verified by YojanaSaathi Demo Review")
        self.message_user(request, f"{queryset.count()} document(s) marked as VERIFIED and citizen notified.")

    @admin.action(description="✗ Mark selected documents as REJECTED")
    def action_mark_rejected(self, request, queryset):
        for doc in queryset:
            verify_document(doc, "REJECTED", remarks="Rejected - document illegible or incomplete")
        self.message_user(request, f"{queryset.count()} document(s) marked as REJECTED.")

    @admin.action(description="⚠ Mark selected documents as CORRECTION REQUIRED")
    def action_mark_correction_required(self, request, queryset):
        for doc in queryset:
            verify_document(doc, "CORRECTION_REQUIRED", remarks="Please upload a clearer copy of this document")
        self.message_user(request, f"{queryset.count()} document(s) marked as CORRECTION REQUIRED.")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "citizen",
        "type",
        "is_read",
        "created_at",
    )

    list_filter = (
        "type",
        "is_read",
        "created_at",
    )

    search_fields = (
        "title",
        "message",
        "citizen__mobile",
    )

    readonly_fields = (
        "id",
        "created_at",
    )