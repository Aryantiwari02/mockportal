import logging

from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from .models import Citizen
from .serializers import CitizenSerializer

logger = logging.getLogger(__name__)


# =========================================================
# TWILIO
# =========================================================

def get_twilio_client():
    return Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN
    )


# =========================================================
# OTP MODE HELPERS
# =========================================================

def is_demo_otp_mode():
    """
    Demo mode (OTP_MODE=demo/dev/console/local) skips Twilio entirely and
    accepts a fixed verification code. Useful for demos and reviewers.
    """
    mode = str(getattr(settings, "OTP_MODE", "twilio")).strip().lower()
    return mode in ("demo", "dev", "console", "local")


def get_demo_otp_code():
    return str(getattr(settings, "OTP_DEMO_CODE", "123456")).strip()


# =========================================================
# MOBILE NUMBER NORMALIZATION & RESTRICTION
# =========================================================

def normalize_mobile(mobile):
    """
    Normalize mobile number to a 10-digit Indian mobile number.
    Handles formats:
    - XXXXXXXXXX
    - 91XXXXXXXXXX
    - +91XXXXXXXXXX
    """
    if not mobile:
        return None

    digits = "".join(filter(str.isdigit, str(mobile).strip()))

    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]

    if len(digits) != 10:
        return None

    return digits


def get_allowed_mobiles():
    """
    Retrieve and normalize the authorized Twilio recipient mobile numbers.
    Supports single or comma-separated numbers.
    """
    raw_allowed = getattr(settings, "TWILIO_ALLOWED_MOBILE", "")
    if isinstance(raw_allowed, (list, tuple)):
        items = raw_allowed
    else:
        items = str(raw_allowed).split(",")
    normalized = set()
    for item in items:
        norm = normalize_mobile(item.strip())
        if norm:
            normalized.add(norm)
    return normalized


# =========================================================
# REQUEST OTP
# =========================================================

@api_view(["POST"])
def request_otp(request):
    raw_mobile = request.data.get("mobile", "")
    mobile = normalize_mobile(raw_mobile)

    if not mobile:
        return Response(
            {
                "error": "Please enter a valid 10-digit mobile number."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    allowed_mobiles = get_allowed_mobiles()

    # Only allow verified Twilio recipient number for trial account
    if not allowed_mobiles or mobile not in allowed_mobiles:
        return Response(
            {
                "error": "For this demo, OTP verification is available only for the registered test mobile number."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if is_demo_otp_mode():
        # No SMS is sent in demo mode. The fixed code is returned in the
        # response so the portal can be demonstrated without live Twilio.
        return Response(
            {
                "message": "OTP generated successfully (demo mode).",
                "status": "pending",
                "demo": True,
                "demo_otp": get_demo_otp_code(),
            },
            status=status.HTTP_200_OK
        )

    phone_number = f"+91{mobile}"

    try:
        client = get_twilio_client()
        verification = (
            client.verify.v2
            .services(settings.TWILIO_VERIFY_SERVICE_SID)
            .verifications
            .create(
                channel="sms",
                to=phone_number
            )
        )

        return Response(
            {
                "message": "OTP sent successfully to your mobile number.",
                "status": verification.status,
            },
            status=status.HTTP_200_OK
        )

    except TwilioRestException as exc:
        logger.error("Twilio error sending OTP: %s", exc)
        return Response(
            {
                "error": "Unable to send OTP. Please try again."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as exc:
        logger.error("Unexpected error sending OTP: %s", exc)
        return Response(
            {
                "error": "Unable to send OTP. Please try again."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# =========================================================
# VERIFY OTP
# =========================================================

@api_view(["POST"])
def verify_otp(request):
    raw_mobile = request.data.get("mobile", "")
    otp = request.data.get("otp", "")

    mobile = normalize_mobile(raw_mobile)

    if not mobile:
        return Response(
            {
                "error": "Please enter a valid 10-digit mobile number."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    allowed_mobiles = get_allowed_mobiles()

    # Reject unauthorized number before calling Twilio verification checks
    if not allowed_mobiles or mobile not in allowed_mobiles:
        return Response(
            {
                "error": "For this demo, OTP verification is available only for the registered test mobile number."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if not otp:
        return Response(
            {
                "error": "OTP is required."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    otp = str(otp).strip()

    if len(otp) != 6 or not otp.isdigit():
        return Response(
            {
                "error": "Please enter a valid 6-digit OTP."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if is_demo_otp_mode():
        if otp != get_demo_otp_code():
            return Response(
                {
                    "error": "Incorrect or expired OTP."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        phone_number = f"+91{mobile}"

        try:
            client = get_twilio_client()
            verification_check = (
                client.verify.v2
                .services(settings.TWILIO_VERIFY_SERVICE_SID)
                .verification_checks
                .create(
                    to=phone_number,
                    code=otp
                )
            )

        except TwilioRestException as exc:
            logger.error("Twilio error verifying OTP: %s", exc)
            return Response(
                {
                    "error": "Unable to verify OTP."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as exc:
            logger.error("Unexpected error verifying OTP: %s", exc)
            return Response(
                {
                    "error": "Unable to verify OTP."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if verification_check.status != "approved":
            return Response(
                {
                    "error": "Incorrect or expired OTP."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    # =====================================================
    # OTP VERIFIED
    # =====================================================

    user, user_created = User.objects.get_or_create(
        username=f"citizen_{mobile}"
    )

    citizen, citizen_created = Citizen.objects.get_or_create(
        mobile=mobile
    )

    if citizen.user_id != user.id:
        citizen.user = user

    citizen.is_verified = True
    citizen.save()

    # =====================================================
    # AUTH TOKEN
    # =====================================================

    token, _ = Token.objects.get_or_create(
        user=user
    )

    return Response(
        {
            "message": "OTP verified successfully.",
            "token": token.key,
            "citizen_id": citizen.id,
            "is_new_citizen": citizen_created,
            "citizen": CitizenSerializer(citizen).data
        },
        status=status.HTTP_200_OK
    )