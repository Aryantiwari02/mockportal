import datetime
import hashlib
import secrets
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from accounts.models import Citizen


class AgentApiKey(models.Model):
    """
    Dedicated machine-to-machine API key for YojanaSaathi AI Agent.
    Stores cryptographically hashed keys to prevent exposure if database is inspected.
    Supports key rotation and revocation.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=120,
        default="YojanaSaathi AI Agent",
        help_text="Descriptive identifier for this agent key",
    )
    key_prefix = models.CharField(
        max_length=16,
        db_index=True,
        help_text="Public prefix used for key lookup without exposing secret",
    )
    hashed_key = models.CharField(
        max_length=128,
        db_index=True,
        help_text="SHA-256 hash of the complete secret key",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this key is currently enabled",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    last_used_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_agent_keys",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Agent API Key"
        verbose_name_plural = "Agent API Keys"

    def __str__(self):
        status_str = "Active" if self.is_active else "Revoked"
        return f"{self.name} ({self.key_prefix}...) - {status_str}"

    @classmethod
    def hash_key(cls, raw_key: str) -> str:
        return hashlib.sha256(raw_key.strip().encode("utf-8")).hexdigest()

    @classmethod
    def create_key(cls, name="YojanaSaathi AI Agent", user=None):
        """
        Generate a cryptographically strong secret key, hash it, and save.
        Returns (AgentApiKey instance, raw_secret_key).
        The raw secret key is only available at creation time.
        """
        raw_secret = f"yjs_ag_{secrets.token_urlsafe(36)}"
        prefix = raw_secret[:14]
        hashed = cls.hash_key(raw_secret)

        instance = cls.objects.create(
            name=name,
            key_prefix=prefix,
            hashed_key=hashed,
            is_active=True,
            created_by=user,
        )
        return instance, raw_secret

    def verify_key(self, raw_key: str) -> bool:
        if not self.is_active or self.revoked_at:
            return False
        incoming_hash = self.hash_key(raw_key)
        return secrets.compare_digest(incoming_hash, self.hashed_key)

    def revoke(self):
        self.is_active = False
        self.revoked_at = timezone.now()
        self.save(update_fields=["is_active", "revoked_at"])


class CitizenAgentDelegation(models.Model):
    """
    Scoped, time-limited delegation granted by a verified citizen to the AI agent.
    Enforces least privilege: agent credentials alone cannot access citizen data
    without an active delegation token granted by the citizen.
    """

    ALLOWED_SCOPES = [
        "schemes:read",
        "applications:read",
        "applications:draft",
        "notifications:read",
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    citizen = models.ForeignKey(
        Citizen,
        on_delete=models.CASCADE,
        related_name="agent_delegations",
    )
    delegation_token = models.CharField(
        max_length=128,
        unique=True,
        db_index=True,
    )
    scopes = models.JSONField(
        default=list,
        help_text="List of granted scope strings",
    )
    is_active = models.BooleanField(
        default=True,
    )
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    last_used_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Citizen Agent Delegation"
        verbose_name_plural = "Citizen Agent Delegations"

    def __str__(self):
        status_str = "Valid" if self.is_valid() else "Expired/Revoked"
        return f"Delegation for {self.citizen.mobile} ({status_str})"

    @classmethod
    def create_delegation(cls, citizen, scopes=None, duration_hours=24):
        """
        Create a secure delegation token for a citizen.
        Default duration is 24 hours. Max duration 168 hours (7 days).
        """
        if scopes is None:
            scopes = [
                "applications:read",
                "applications:draft",
                "notifications:read",
            ]
        else:
            # Validate scopes
            scopes = [s for s in scopes if s in cls.ALLOWED_SCOPES or s == "*"]

        duration = max(1, min(int(duration_hours), 168))
        expires_at = timezone.now() + datetime.timedelta(hours=duration)
        token = f"yjs_del_{secrets.token_urlsafe(36)}"

        return cls.objects.create(
            citizen=citizen,
            delegation_token=token,
            scopes=scopes,
            is_active=True,
            expires_at=expires_at,
        )

    def is_valid(self) -> bool:
        if not self.is_active or self.revoked_at is not None:
            return False
        return timezone.now() < self.expires_at

    def has_scope(self, required_scope: str) -> bool:
        if not self.is_valid():
            return False
        if "*" in self.scopes or "admin" in self.scopes:
            return True
        return required_scope in self.scopes

    def revoke(self):
        self.is_active = False
        self.revoked_at = timezone.now()
        self.save(update_fields=["is_active", "revoked_at"])


class AgentAuditLog(models.Model):
    """
    Audit log of all machine-to-machine agent operations.
    Keeps track of access for security audits and non-repudiation.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    agent_key_name = models.CharField(
        max_length=120,
        blank=True,
    )
    agent_key_prefix = models.CharField(
        max_length=20,
        blank=True,
    )
    citizen = models.ForeignKey(
        Citizen,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="agent_audit_logs",
    )
    action = models.CharField(
        max_length=100,
    )
    endpoint = models.CharField(
        max_length=255,
    )
    method = models.CharField(
        max_length=10,
    )
    status_code = models.IntegerField()
    ip_address = models.CharField(
        max_length=60,
        blank=True,
    )
    user_agent = models.CharField(
        max_length=255,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Agent Audit Log"
        verbose_name_plural = "Agent Audit Logs"

    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d %H:%M:%S')} - {self.action} ({self.status_code})"
