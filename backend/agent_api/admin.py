from django.contrib import admin
from django.utils.html import format_html

from .models import AgentApiKey, CitizenAgentDelegation, AgentAuditLog


@admin.register(AgentApiKey)
class AgentApiKeyAdmin(admin.ModelAdmin):
    list_display = ("name", "key_prefix", "is_active", "created_at", "last_used_at", "revoked_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "key_prefix")
    readonly_fields = ("id", "key_prefix", "hashed_key", "created_at", "revoked_at", "last_used_at")
    actions = ["revoke_keys"]

    def revoke_keys(self, request, queryset):
        for key in queryset:
            key.revoke()
        self.message_user(request, f"{queryset.count()} key(s) successfully revoked.")
    revoke_keys.short_description = "Revoke selected Agent API keys"


@admin.register(CitizenAgentDelegation)
class CitizenAgentDelegationAdmin(admin.ModelAdmin):
    list_display = ("citizen", "delegation_status", "scopes_display", "created_at", "expires_at", "last_used_at")
    list_filter = ("is_active", "created_at", "expires_at")
    search_fields = ("citizen__mobile", "citizen__full_name", "delegation_token")
    readonly_fields = ("id", "citizen", "delegation_token", "created_at", "revoked_at", "last_used_at")
    actions = ["revoke_delegations"]

    def delegation_status(self, obj):
        if not obj.is_active or obj.revoked_at:
            return format_html('<span style="color: red; font-weight: bold;">Revoked</span>')
        if not obj.is_valid():
            return format_html('<span style="color: gray;">Expired</span>')
        return format_html('<span style="color: green; font-weight: bold;">Active</span>')
    delegation_status.short_description = "Status"

    def scopes_display(self, obj):
        return ", ".join(obj.scopes) if obj.scopes else "None"
    scopes_display.short_description = "Scopes"

    def revoke_delegations(self, request, queryset):
        for item in queryset:
            item.revoke()
        self.message_user(request, f"{queryset.count()} delegation(s) successfully revoked.")
    revoke_delegations.short_description = "Revoke selected Citizen delegations"


@admin.register(AgentAuditLog)
class AgentAuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "action", "status_code", "agent_key_name", "citizen", "endpoint", "ip_address")
    list_filter = ("action", "status_code", "created_at")
    search_fields = ("action", "endpoint", "agent_key_name", "citizen__mobile", "ip_address")
    readonly_fields = (
        "id", "created_at", "agent_key_name", "agent_key_prefix", "citizen",
        "action", "endpoint", "method", "status_code", "ip_address", "user_agent"
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
