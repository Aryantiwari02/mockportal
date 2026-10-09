import io
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from accounts.models import Citizen
from schemes.models import Scheme
from applications.models import Application, ApplicationDocument, Notification, verify_document


class ApplicationWorkflowTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create Scheme 1
        self.scheme = Scheme.objects.create(
            id="health-001",
            category="Health",
            title="National Health Support Scheme",
            short_description="Healthcare assistance for eligible citizens.",
            description="Full description of health assistance.",
            eligibility=["Resident citizen", "Satisfy income criteria"],
            documents=["Identity Proof", "Residence Proof", "Income Certificate"],
            application_fields=[
                {
                    "name": "full_name",
                    "label": "Full Name",
                    "type": "text",
                    "required": True,
                },
                {
                    "name": "annual_income",
                    "label": "Annual Income",
                    "type": "number",
                    "required": True,
                },
                {
                    "name": "declaration_consent",
                    "label": "Declaration Consent",
                    "type": "checkbox",
                    "required": True,
                },
            ]
        )

        # Create Citizen 1
        self.user1 = User.objects.create(username="citizen_9876543210")
        self.citizen1 = Citizen.objects.create(
            user=self.user1,
            mobile="9876543210",
            full_name="Rajesh Kumar",
            is_verified=True
        )
        self.token1 = Token.objects.create(user=self.user1)

        # Create Citizen 2 (for authorization tests)
        self.user2 = User.objects.create(username="citizen_8888888888")
        self.citizen2 = Citizen.objects.create(
            user=self.user2,
            mobile="8888888888",
            full_name="Pooja Sharma",
            is_verified=True
        )
        self.token2 = Token.objects.create(user=self.user2)

    def test_create_application_draft(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.post(
            "/api/applications/",
            {"scheme_id": self.scheme.id, "form_data": {"full_name": "Rajesh Kumar"}},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["application_number"].startswith("YJS-"))
        self.assertEqual(response.data["status"], "DRAFT")

    def test_upload_document_success_and_invalid_type_rejection(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        app = Application.objects.create(
            citizen=self.citizen1,
            scheme=self.scheme,
            status="DRAFT"
        )

        # 1. Invalid file extension (.exe)
        bad_file = SimpleUploadedFile("virus.exe", b"binary content", content_type="application/octet-stream")
        bad_response = self.client.post(
            f"/api/applications/{app.application_number}/documents/",
            {"document_type": "Identity Proof", "file": bad_file},
            format="multipart"
        )
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid file format", bad_response.data["error"])

        # 2. Valid PDF upload
        good_file = SimpleUploadedFile("id_proof.pdf", b"%PDF-1.4 sample content", content_type="application/pdf")
        good_response = self.client.post(
            f"/api/applications/{app.application_number}/documents/",
            {"document_type": "Identity Proof", "file": good_file},
            format="multipart"
        )
        self.assertEqual(good_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(good_response.data["verification_status"], "UPLOADED")
        self.assertEqual(good_response.data["document_type"], "Identity Proof")

    def test_submission_validation_fails_when_fields_or_documents_missing(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        app = Application.objects.create(
            citizen=self.citizen1,
            scheme=self.scheme,
            status="DRAFT",
            form_data={}
        )

        # 1. Missing required fields
        response = self.client.post(
            f"/api/applications/{app.application_number}/submit/",
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("required", response.data["error"])

        # 2. Fill fields but missing documents
        app.form_data = {
            "full_name": "Rajesh Kumar",
            "annual_income": "250000",
            "declaration_consent": True
        }
        app.save()

        response2 = self.client.post(
            f"/api/applications/{app.application_number}/submit/",
            format="json"
        )
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Identity Proof is required", response2.data["error"])

    def test_successful_submission_and_notification(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        app = Application.objects.create(
            citizen=self.citizen1,
            scheme=self.scheme,
            status="DRAFT",
            form_data={
                "full_name": "Rajesh Kumar",
                "annual_income": "250000",
                "declaration_consent": True
            }
        )

        # Attach all 3 required documents
        for doc_name in self.scheme.documents:
            pdf_file = SimpleUploadedFile(f"{doc_name}.pdf", b"%PDF sample", content_type="application/pdf")
            ApplicationDocument.objects.create(
                application=app,
                document_type=doc_name,
                file=pdf_file,
                file_name=f"{doc_name}.pdf",
                file_size=1024,
                verification_status="UPLOADED"
            )

        # Submit application
        res = self.client.post(
            f"/api/applications/{app.application_number}/submit/",
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        app.refresh_from_db()
        self.assertEqual(app.status, "SUBMITTED")
        self.assertIsNotNone(app.submitted_at)

        # Uploaded docs should now be UNDER_REVIEW
        for doc in app.documents.all():
            self.assertEqual(doc.verification_status, "UNDER_REVIEW")

        # Notification should be created
        note = Notification.objects.filter(citizen=self.citizen1, type="application_submitted").first()
        self.assertIsNotNone(note)
        self.assertIn(app.application_number, note.message)

    def test_document_verification_workflow_and_all_verified_notification(self):
        app = Application.objects.create(
            citizen=self.citizen1,
            scheme=self.scheme,
            status="SUBMITTED",
            form_data={"full_name": "Rajesh Kumar"}
        )

        doc1 = ApplicationDocument.objects.create(
            application=app,
            document_type="Identity Proof",
            file=SimpleUploadedFile("id.pdf", b"test"),
            verification_status="UNDER_REVIEW"
        )
        doc2 = ApplicationDocument.objects.create(
            application=app,
            document_type="Residence Proof",
            file=SimpleUploadedFile("res.pdf", b"test"),
            verification_status="UNDER_REVIEW"
        )
        doc3 = ApplicationDocument.objects.create(
            application=app,
            document_type="Income Certificate",
            file=SimpleUploadedFile("inc.pdf", b"test"),
            verification_status="UNDER_REVIEW"
        )

        # Verify Doc 1
        verify_document(doc1, "VERIFIED", remarks="Verified by Demo Review")
        doc1.refresh_from_db()
        self.assertEqual(doc1.verification_status, "VERIFIED")
        self.assertIsNotNone(doc1.verified_at)

        # Verify Doc 1 generated a notification
        note1 = Notification.objects.filter(citizen=self.citizen1, type="document_verified").first()
        self.assertIsNotNone(note1)
        self.assertIn("Identity Proof", note1.message)

        # Verify Doc 2 and 3
        verify_document(doc2, "VERIFIED", remarks="Verified by Demo Review")
        verify_document(doc3, "VERIFIED", remarks="Verified by Demo Review")

        # Now all 3 required documents are verified!
        all_note = Notification.objects.filter(citizen=self.citizen1, type="all_documents_verified").first()
        self.assertIsNotNone(all_note)
        self.assertEqual(all_note.title, "All Documents Verified")

    def test_pdf_downloads_and_cross_citizen_security(self):
        app = Application.objects.create(
            citizen=self.citizen1,
            scheme=self.scheme,
            status="SUBMITTED",
            form_data={"full_name": "Rajesh Kumar", "annual_income": "250000"}
        )

        doc = ApplicationDocument.objects.create(
            application=app,
            document_type="Identity Proof",
            file=SimpleUploadedFile("id.pdf", b"%PDF-1.4 file content"),
            file_name="id.pdf",
            file_type="application/pdf",
            verification_status="VERIFIED"
        )

        # 1. Citizen 1 downloads their own application PDF
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        pdf_res = self.client.get(f"/api/applications/{app.application_number}/pdf/")
        self.assertEqual(pdf_res.status_code, status.HTTP_200_OK)
        self.assertEqual(pdf_res["Content-Type"], "application/pdf")
        self.assertTrue(len(pdf_res.getvalue()) > 500)

        # 2. Blank form PDF download is accessible
        blank_res = self.client.get(f"/api/schemes/{self.scheme.id}/blank-form-pdf/")
        self.assertEqual(blank_res.status_code, status.HTTP_200_OK)
        self.assertEqual(blank_res["Content-Type"], "application/pdf")

        # 3. Cross-citizen security: Citizen 2 attempts to access Citizen 1's application and document
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        cross_app_res = self.client.get(f"/api/applications/{app.application_number}/")
        self.assertEqual(cross_app_res.status_code, status.HTTP_404_NOT_FOUND)

        cross_pdf_res = self.client.get(f"/api/applications/{app.application_number}/pdf/")
        self.assertEqual(cross_pdf_res.status_code, status.HTTP_404_NOT_FOUND)

        cross_doc_res = self.client.get(f"/api/applications/{app.application_number}/documents/{doc.id}/download/")
        self.assertEqual(cross_doc_res.status_code, status.HTTP_404_NOT_FOUND)


# =========================================================
# PHASE 4 — Application Status Endpoint Tests
# =========================================================

class ApplicationStatusEndpointTests(TestCase):
    """
    Tests for GET /api/applications/<application_number>/status/

    Covers:
    - Authenticated citizen retrieving their own application status.
    - Safe fields only (no PII, no form_data in response).
    - Unauthenticated request returns 401.
    - Non-existent application returns 404.
    - Cross-citizen access returns 404 (not 403, to avoid leaking existence).
    - Response shape and status_label / next_step fields are present.
    """

    def setUp(self):
        self.client = APIClient()

        self.scheme = Scheme.objects.create(
            id="pension-001",
            category="Pension",
            title="Senior Citizen Pension Scheme",
            short_description="Monthly pension for senior citizens.",
            description="Full description.",
            eligibility=["Age 60+", "Resident of Karnataka"],
            documents=["Identity Proof", "Age Proof"],
            application_fields=[
                {"name": "full_name", "label": "Full Name", "type": "text", "required": True},
            ]
        )

        # Citizen A — owns the application
        self.user_a = User.objects.create(username="citizen_status_a")
        self.citizen_a = Citizen.objects.create(
            user=self.user_a, mobile="9000000001", full_name="Status Citizen A", is_verified=True
        )
        self.token_a = Token.objects.create(user=self.user_a)

        # Citizen B — unrelated citizen
        self.user_b = User.objects.create(username="citizen_status_b")
        self.citizen_b = Citizen.objects.create(
            user=self.user_b, mobile="9000000002", full_name="Status Citizen B", is_verified=True
        )
        self.token_b = Token.objects.create(user=self.user_b)

        # Application belonging to Citizen A
        self.app = Application.objects.create(
            citizen=self.citizen_a,
            scheme=self.scheme,
            status="SUBMITTED",
            form_data={"full_name": "Status Citizen A", "aadhaar": "1234-5678-9012"},
        )

    def _url(self, app_number=None):
        number = app_number or self.app.application_number
        return f"/api/applications/{number}/status/"

    def test_citizen_can_retrieve_own_application_status(self):
        """Authenticated owner receives status with safe fields only."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_a.key}")
        res = self.client.get(self._url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = res.data
        self.assertEqual(data["application_number"], self.app.application_number)
        self.assertEqual(data["status"], "SUBMITTED")
        self.assertIn("status_label", data)
        self.assertIn("next_step", data)
        self.assertEqual(data["scheme_title"], "Senior Citizen Pension Scheme")

    def test_response_does_not_expose_sensitive_fields(self):
        """Status response must NOT include form_data, citizen PII, or documents."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_a.key}")
        res = self.client.get(self._url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.data

        # Explicitly assert that sensitive keys are absent
        self.assertNotIn("form_data", data)
        self.assertNotIn("citizen", data)
        self.assertNotIn("documents", data)
        self.assertNotIn("id", data)    # internal UUID should not be exposed

    def test_unauthenticated_request_returns_401(self):
        """Request without authentication token must be rejected."""
        self.client.credentials()  # clear credentials
        res = self.client.get(self._url())
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_nonexistent_application_returns_404(self):
        """A request for an application number that does not exist returns 404."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_a.key}")
        res = self.client.get(self._url("YJS-DOESNOTEXIST"))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_cross_citizen_access_returns_404(self):
        """
        Citizen B must not be able to retrieve Citizen A's application status.
        Must return 404 (not 403) to avoid confirming that the application
        exists under a different citizen.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_b.key}")
        res = self.client.get(self._url())
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_status_label_and_next_step_are_populated(self):
        """status_label and next_step must be non-empty strings for every real status."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_a.key}")

        for status_value, expected_label in [
            ("DRAFT", "Draft"),
            ("SUBMITTED", "Submitted"),
            ("UNDER_REVIEW", "Under Review"),
            ("APPROVED", "Approved"),
            ("REJECTED", "Rejected"),
            ("CORRECTION_REQUIRED", "Correction Required"),
        ]:
            self.app.status = status_value
            self.app.save(update_fields=["status"])

            res = self.client.get(self._url())
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data["status_label"], expected_label)
            self.assertIsInstance(res.data["next_step"], str)
            self.assertGreater(len(res.data["next_step"]), 0)

