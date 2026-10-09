from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Citizen(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="citizen_profile"
    )

    mobile = models.CharField(max_length=15, unique=True)

    full_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mobile


class OTPVerification(models.Model):
    mobile = models.CharField(max_length=15)

    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.mobile} - {self.otp}"