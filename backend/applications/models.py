import os
import uuid

from django.db import models
from django.utils import timezone

from accounts.models import Citizen
from schemes.models import Scheme


def application_document_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    clean_name = f"{uuid.uuid4().hex[:12]}{ext}"
    app_no = instance.application.application_number or "temp"
    return f"documents/{app_no}/{clean_name}"


class Application(models.Model):

    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("SUBMITTED", "Submitted"),
        ("UNDER_REVIEW", "Under Review"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("CORRECTION_REQUIRED", "Correction Required"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    application_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False
    )

    citizen = models.ForeignKey(
        Citizen,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    scheme = models.ForeignKey(
        Scheme,
        on_delete=models.PROTECT,
        related_name="applications"
    )

    form_data = models.JSONField(
        default=dict
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="DRAFT"
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if not self.application_number:
            self.application_number = (
                f"YJS-{self.id.hex[:10].upper()}"
            )
        super().save(*args, **kwargs)

    @property
    def documents_count(self):
        return self.documents.count()

    @property
    def verified_documents_count(self):
        return self.documents.filter(verification_status="VERIFIED").count()

    @property
    def total_required_documents_count(self):
        return len(self.scheme.documents) if self.scheme and self.scheme.documents else 0

    @property
    def all_documents_verified(self):
        if not self.scheme or not self.scheme.documents:
            return False
        verified_types = set(
            self.documents.filter(verification_status="VERIFIED").values_list("document_type", flat=True)
        )
        return all(d in verified_types for d in self.scheme.documents)

    def __str__(self):
        return self.application_number


class ApplicationDocument(models.Model):

    STATUS_CHOICES = [
        ("UPLOADED", "Uploaded"),
        ("UNDER_REVIEW", "Under Review"),
        ("VERIFIED", "Verified"),
        ("REJECTED", "Rejected"),
        ("CORRECTION_REQUIRED", "Correction Required"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    document_type = models.CharField(
        max_length=150
    )

    file = models.FileField(
        upload_to=application_document_upload_path
    )

    file_name = models.CharField(
        max_length=255,
        blank=True
    )

    file_size = models.PositiveIntegerField(
        default=0
    )

    file_type = models.CharField(
        max_length=50,
        blank=True
    )

    verification_status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="UPLOADED"
    )

    remarks = models.TextField(
        blank=True,
        default=""
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["uploaded_at"]
        unique_together = ["application", "document_type"]

    def __str__(self):
        return f"{self.application.application_number} - {self.document_type} ({self.verification_status})"


class Notification(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    citizen = models.ForeignKey(
        Citizen,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications"
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    type = models.CharField(
        max_length=50,
        default="info"
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.citizen.mobile} - {self.title}"


def verify_document(document, new_status, remarks=""):
    """
    Verify or update status of an ApplicationDocument.
    Sets verified_at, updates status, and generates citizen notifications.
    """
    old_status = document.verification_status
    document.verification_status = new_status
    document.remarks = remarks

    if new_status == "VERIFIED":
        document.verified_at = timezone.now()
    elif new_status != "VERIFIED":
        document.verified_at = None

    document.save(update_fields=["verification_status", "remarks", "verified_at"])

    # If marked verified, create citizen notification
    if new_status == "VERIFIED" and old_status != "VERIFIED":
        Notification.objects.create(
            citizen=document.application.citizen,
            application=document.application,
            title="Document Verified",
            message=f"Your {document.document_type} for application {document.application.application_number} has been verified by YojanaSaathi Demo Review.",
            type="document_verified"
        )

        # Check if all required documents for this scheme are verified
        scheme = document.application.scheme
        required_docs = scheme.documents or []
        verified_types = set(
            document.application.documents.filter(verification_status="VERIFIED").values_list("document_type", flat=True)
        )

        if required_docs and all(d in verified_types for d in required_docs):
            # Check if all-verified notification already sent
            if not Notification.objects.filter(
                application=document.application,
                type="all_documents_verified"
            ).exists():
                Notification.objects.create(
                    citizen=document.application.citizen,
                    application=document.application,
                    title="All Documents Verified",
                    message=f"All required documents for your application {document.application.application_number} have been verified.",
                    type="all_documents_verified"
                )