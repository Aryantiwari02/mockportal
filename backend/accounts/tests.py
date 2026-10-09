from unittest.mock import MagicMock, patch
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from accounts.views import normalize_mobile


class TwilioAllowedMobileTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_normalize_mobile_formats(self):
        # 10 digits
        self.assertEqual(normalize_mobile("9876543210"), "9876543210")
        # 91 + 10 digits
        self.assertEqual(normalize_mobile("919876543210"), "9876543210")
        # +91 + 10 digits
        self.assertEqual(normalize_mobile("+919876543210"), "9876543210")
        # Formatted with spaces or dashes
        self.assertEqual(normalize_mobile("+91 98765-43210"), "9876543210")
        # Leading zero 11 digits
        self.assertEqual(normalize_mobile("09876543210"), "9876543210")
        # Invalid numbers
        self.assertIsNone(normalize_mobile("12345"))
        self.assertIsNone(normalize_mobile("abcdefghij"))
        self.assertIsNone(normalize_mobile(""))
        self.assertIsNone(normalize_mobile(None))

    @override_settings(TWILIO_ALLOWED_MOBILE="9876543210")
    @patch("accounts.views.get_twilio_client")
    def test_request_otp_rejects_unauthorized_number_without_calling_twilio(self, mock_twilio):
        response = self.client.post(
            "/api/auth/request-otp/",
            {"mobile": "9999999999"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("error"),
            "For this demo, OTP verification is available only for the registered test mobile number."
        )
        mock_twilio.assert_not_called()

    @override_settings(TWILIO_ALLOWED_MOBILE="9876543210", OTP_MODE="twilio")
    @patch("accounts.views.get_twilio_client")
    def test_request_otp_succeeds_for_authorized_number(self, mock_twilio):
        # Mock Twilio Verify response
        mock_client_instance = MagicMock()
        mock_verification = MagicMock()
        mock_verification.status = "pending"
        mock_client_instance.verify.v2.services.return_value.verifications.create.return_value = mock_verification
        mock_twilio.return_value = mock_client_instance

        # Test with +91 format
        response = self.client.post(
            "/api/auth/request-otp/",
            {"mobile": "+919876543210"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("status"), "pending")
        mock_twilio.assert_called_once()
        mock_client_instance.verify.v2.services.return_value.verifications.create.assert_called_once_with(
            channel="sms",
            to="+919876543210"
        )

    @override_settings(TWILIO_ALLOWED_MOBILE="9876543210")
    @patch("accounts.views.get_twilio_client")
    def test_verify_otp_rejects_unauthorized_number_without_calling_twilio(self, mock_twilio):
        response = self.client.post(
            "/api/auth/verify-otp/",
            {"mobile": "9999999999", "otp": "123456"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("error"),
            "For this demo, OTP verification is available only for the registered test mobile number."
        )
        mock_twilio.assert_not_called()

    @override_settings(TWILIO_ALLOWED_MOBILE="9876543210", OTP_MODE="twilio")
    @patch("accounts.views.get_twilio_client")
    def test_verify_otp_succeeds_and_creates_user_and_citizen(self, mock_twilio):
        mock_client_instance = MagicMock()
        mock_verification_check = MagicMock()
        mock_verification_check.status = "approved"
        mock_client_instance.verify.v2.services.return_value.verification_checks.create.return_value = mock_verification_check
        mock_twilio.return_value = mock_client_instance

        response = self.client.post(
            "/api/auth/verify-otp/",
            {"mobile": "9876543210", "otp": "123456"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("citizen", response.data)
        self.assertEqual(response.data["citizen"]["mobile"], "9876543210")
        self.assertTrue(response.data["citizen"]["is_verified"])
        mock_twilio.assert_called_once()
        mock_client_instance.verify.v2.services.return_value.verification_checks.create.assert_called_once_with(
            to="+919876543210",
            code="123456"
        )


class DemoOtpModeTests(TestCase):
    """OTP_MODE=demo must work end-to-end without contacting Twilio."""

    def setUp(self):
        self.client = APIClient()

    @override_settings(
        TWILIO_ALLOWED_MOBILE="9876543210",
        OTP_MODE="demo",
        OTP_DEMO_CODE="123456",
    )
    @patch("accounts.views.get_twilio_client")
    def test_demo_request_otp_does_not_call_twilio(self, mock_twilio):
        response = self.client.post(
            "/api/auth/request-otp/",
            {"mobile": "9876543210"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("demo"))
        self.assertEqual(response.data.get("demo_otp"), "123456")
        mock_twilio.assert_not_called()

    @override_settings(
        TWILIO_ALLOWED_MOBILE="9876543210",
        OTP_MODE="demo",
        OTP_DEMO_CODE="123456",
    )
    @patch("accounts.views.get_twilio_client")
    def test_demo_verify_otp_accepts_fixed_code(self, mock_twilio):
        response = self.client.post(
            "/api/auth/verify-otp/",
            {"mobile": "9876543210", "otp": "123456"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["citizen"]["mobile"], "9876543210")
        mock_twilio.assert_not_called()

    @override_settings(
        TWILIO_ALLOWED_MOBILE="9876543210",
        OTP_MODE="demo",
        OTP_DEMO_CODE="123456",
    )
    @patch("accounts.views.get_twilio_client")
    def test_demo_verify_otp_rejects_wrong_code(self, mock_twilio):
        response = self.client.post(
            "/api/auth/verify-otp/",
            {"mobile": "9876543210", "otp": "000000"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("error"), "Incorrect or expired OTP.")
        mock_twilio.assert_not_called()
