import datetime
import uuid
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from accounts.models import Citizen
from applications.models import Application, ApplicationDocument, Notification
from schemes.models import Scheme

from agent_api.models import AgentApiKey, AgentAuditLog, CitizenAgentDelegation


class YojanaSaathiAgentIntegrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # 1. Create a test Scheme
        self.scheme = Scheme.objects.create(
            id="health-pmjay",
            category="Health",
            title="Ayushman Bharat PM-JAY",
            short_description="Health assurance of up to Rs. 5 Lakh per family per year.",
            description="Comprehensive national health protection scheme.",
            eligibility=["Resident citizen", "Annual income under 3 Lakhs"],
            eligibility_rules={"max_income": 300000, "resident": True},
            documents=["Aadhaar Card", "Ration Card"],
            application_fields=[
                {"name": "full_name", "label": "Full Name", "type": "text", "required": True},
                {"name": "annual_income", "label": "Annual Income", "type": "number", "required": True},
            ],
            application_process=["Step 1: Check eligibility", "Step 2: Submit application"],
        )

        # 2. Create Citizen 1 (Authorized)
        self.user1 = User.objects.create(username="citizen_9876543210")
        self.citizen1 = Citizen.objects.create(
            user=self.user1,
            mobile="9876543210",
            full_name="Rajesh Kumar",
            is_verified=True,
        )
        self.token1 = Token.objects.create(user=self.user1)

        # 3. Create Citizen 2 (Unauthorized / Isolated)
        self.user2 = User.objects.create(username="citizen_8888888888")
        self.citizen2 = Citizen.objects.create(
            user=self.user2,
            mobile="8888888888",
            full_name="Pooja Sharma",
            is_verified=True,
        )
        self.token2 = Token.objects.create(user=self.user2)

        # 4. Create an Application for Citizen 1
        self.app1 = Application.objects.create(
            citizen=self.citizen1,
            scheme=self.scheme,
            status="DRAFT",
            form_data={"full_name": "Rajesh Kumar", "annual_income": "250000"},
        )
        self.doc1 = ApplicationDocument.objects.create(
            application=self.app1,
            document_type="Aadhaar Card",
            file_name="aadhaar.pdf",
            file_size=10240,
            file_type="application/pdf",
            verification_status="VERIFIED",
            remarks="Verified successfully",
            verified_at=timezone.now(),
        )

        # 5. Create an Application for Citizen 2 (to test cross-citizen boundary)
        self.app2 = Application.objects.create(
            citizen=self.citizen2,
            scheme=self.scheme,
            status="SUBMITTED",
            form_data={"full_name": "Pooja Sharma"},
        )

        # 6. Create Notification for Citizen 1
        self.notif1 = Notification.objects.create(
            citizen=self.citizen1,
            application=self.app1,
            title="Aadhaar Verified",
            message="Your Aadhaar card was verified.",
            type="document_verified",
        )

        # 7. Create Active Agent API Key
        self.agent_key_record, self.raw_agent_key = AgentApiKey.create_key(
            name="Production YojanaSaathi Agent"
        )

        # 8. Create Active Citizen Delegation Token for Citizen 1
        self.delegation1 = CitizenAgentDelegation.create_delegation(
            citizen=self.citizen1,
            scopes=["applications:read", "applications:draft", "notifications:read"],
            duration_hours=24,
        )
        self.raw_delegation_token = self.delegation1.delegation_token

    # ========================================================
    # TASK 1: AGENT AUTHENTICATION TESTS
    # ========================================================

    def test_missing_agent_key_is_rejected(self):
        """Missing X-Agent-API-Key header returns 401 Unauthorized."""
        response = self.client.get("/api/agent/v1/schemes/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_agent_key_is_rejected(self):
        """Tampered or invalid X-Agent-API-Key returns 401 Unauthorized."""
        response = self.client.get(
            "/api/agent/v1/schemes/",
            HTTP_X_AGENT_API_KEY="invalid_agent_key_12345678",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("AGENT_AUTHENTICATION_FAILED", str(response.data))

    def test_revoked_agent_key_is_rejected(self):
        """A revoked agent key is immediately rejected with 401."""
        self.agent_key_record.revoke()
        response = self.client.get(
            "/api/agent/v1/schemes/",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_agent_key_via_bearer_authorization_header(self):
        """Agent can also authenticate via Bearer header with yjs_ag_ key."""
        response = self.client.get(
            "/api/agent/v1/schemes/",
            HTTP_AUTHORIZATION=f"Bearer {self.raw_agent_key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(YOJANASAATHI_AGENT_API_KEY="yjs_ag_env_test_secret_key_1234567890")
    def test_env_agent_key_fallback_authentication(self):
        """Agent key configured in settings/env succeeds via constant-time match."""
        response = self.client.get(
            "/api/agent/v1/schemes/",
            HTTP_X_AGENT_API_KEY="yjs_ag_env_test_secret_key_1234567890",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ========================================================
    # TASK 2: PUBLIC SCHEME ENDPOINTS (M2M AGENT ACCESS)
    # ========================================================

    def test_agent_scheme_list_and_search(self):
        """Agent can search and list schemes with valid agent key."""
        # Query list
        response = self.client.get(
            "/api/agent/v1/schemes/",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data["count"], 1)

        # Search by query
        search_resp = self.client.get(
            "/api/agent/v1/schemes/?q=Ayushman",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
        )
        self.assertEqual(search_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(search_resp.data["count"], 1)

    def test_agent_scheme_detail(self):
        """Agent can retrieve full scheme details."""
        response = self.client.get(
            f"/api/agent/v1/schemes/{self.scheme.id}/",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.scheme.id)
        self.assertEqual(response.data["title"], self.scheme.title)
        self.assertIn("documents", response.data)
        self.assertIn("application_process", response.data)

    def test_agent_scheme_requirements(self):
        """Agent can retrieve form fields and required documents."""
        response = self.client.get(
            f"/api/agent/v1/schemes/{self.scheme.id}/requirements/",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("application_fields", response.data)
        self.assertIn("required_documents", response.data)
        self.assertEqual(response.data["required_documents"], ["Aadhaar Card", "Ration Card"])

    def test_agent_scheme_eligibility(self):
        """Agent can retrieve eligibility criteria and rules."""
        response = self.client.get(
            f"/api/agent/v1/schemes/{self.scheme.id}/eligibility/",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("eligibility_criteria", response.data)
        self.assertIn("eligibility_rules", response.data)
        self.assertIn("application_process", response.data)

    # ========================================================
    # TASK 3: CITIZEN CONSENT & DELEGATION AUTHORIZATION
    # ========================================================

    def test_citizen_can_create_delegation_via_otp_token(self):
        """Citizen authenticated via standard Token can grant delegation to agent."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.client.post(
            "/api/auth/agent-delegation/",
            {
                "duration_hours": 12,
                "scopes": ["applications:read", "applications:draft"],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["delegation_token"].startswith("yjs_del_"))
        self.assertIn("expires_at", response.data)

    def test_citizen_can_list_and_revoke_delegation(self):
        """Citizen can view their delegations and revoke one."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")

        # List
        list_resp = self.client.get("/api/auth/agent-delegations/")
        self.assertEqual(list_resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(list_resp.data["count"], 1)

        # Revoke
        del_id = list_resp.data["results"][0]["id"]
        revoke_resp = self.client.post(f"/api/auth/agent-delegation/{del_id}/revoke/")
        self.assertEqual(revoke_resp.status_code, status.HTTP_200_OK)

        # Verify delegation is now invalid
        delegation = CitizenAgentDelegation.objects.get(id=del_id)
        self.assertFalse(delegation.is_valid())

    def test_private_citizen_operation_rejected_without_delegation_token(self):
        """Agent cannot access private citizen endpoints without delegation token (403)."""
        response = self.client.get(
            "/api/agent/v1/citizen/applications/",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("DELEGATION_TOKEN_REQUIRED", str(response.data))

    def test_expired_or_revoked_delegation_rejected(self):
        """Expired or revoked citizen delegation is rejected."""
        self.delegation1.revoke()
        response = self.client.get(
            "/api/agent/v1/citizen/applications/",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
            HTTP_X_CITIZEN_DELEGATION_TOKEN=self.raw_delegation_token,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("DELEGATION_TOKEN_INVALID", str(response.data))

    def test_delegation_scope_enforcement(self):
        """Delegation without required scope is rejected with 403."""
        limited_del = CitizenAgentDelegation.create_delegation(
            citizen=self.citizen1,
            scopes=["applications:read"],  # No draft scope
            duration_hours=1,
        )
        response = self.client.post(
            "/api/agent/v1/citizen/applications/draft/",
            {"scheme_id": self.scheme.id, "form_data": {"full_name": "Test"}},
            format="json",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
            HTTP_X_CITIZEN_DELEGATION_TOKEN=limited_del.delegation_token,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("DELEGATION_SCOPE_INSUFFICIENT", str(response.data))

    # ========================================================
    # TASK 2 & 3: CITIZEN OPERATIONS ON BEHALF OF CITIZEN
    # ========================================================

    def test_agent_can_create_or_update_draft_application(self):
        """Agent can create/update draft application with valid delegation."""
        response = self.client.post(
            "/api/agent/v1/citizen/applications/draft/",
            {
                "scheme_id": self.scheme.id,
                "form_data": {"full_name": "Rajesh Kumar Updated", "annual_income": "280000"},
            },
            format="json",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
            HTTP_X_CITIZEN_DELEGATION_TOKEN=self.raw_delegation_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["application"]["status"], "DRAFT")
        self.assertEqual(
            response.data["application"]["form_data"]["full_name"],
            "Rajesh Kumar Updated",
        )

    def test_agent_can_retrieve_citizen_applications(self):
        """Agent can retrieve the delegated citizen's applications and statuses."""
        response = self.client.get(
            "/api/agent/v1/citizen/applications/",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
            HTTP_X_CITIZEN_DELEGATION_TOKEN=self.raw_delegation_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["application_number"], self.app1.application_number)

    def test_citizen_boundary_agent_cannot_access_other_citizen_application(self):
        """Agent cannot access an application belonging to Citizen 2 (returns 404)."""
        response = self.client.get(
            f"/api/agent/v1/citizen/applications/{self.app2.application_number}/",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
            HTTP_X_CITIZEN_DELEGATION_TOKEN=self.raw_delegation_token,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_agent_can_retrieve_document_verification_statuses(self):
        """Agent can retrieve verification status but cannot download documents."""
        response = self.client.get(
            f"/api/agent/v1/citizen/applications/{self.app1.application_number}/documents/",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
            HTTP_X_CITIZEN_DELEGATION_TOKEN=self.raw_delegation_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_documents"], 1)
        self.assertEqual(response.data["verified_documents"], 1)
        # Verify no file binary URL is leaked
        doc_entry = response.data["results"][0]
        self.assertEqual(doc_entry["document_type"], "Aadhaar Card")
        self.assertEqual(doc_entry["verification_status"], "VERIFIED")
        self.assertNotIn("download_url", doc_entry)
        self.assertNotIn("file_path", doc_entry)

    def test_agent_can_retrieve_application_history_and_notifications(self):
        """Agent can retrieve application timeline and notifications."""
        # Application history
        hist_resp = self.client.get(
            f"/api/agent/v1/citizen/applications/{self.app1.application_number}/history/",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
            HTTP_X_CITIZEN_DELEGATION_TOKEN=self.raw_delegation_token,
        )
        self.assertEqual(hist_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(hist_resp.data["application_number"], self.app1.application_number)
        self.assertIn("documents_summary", hist_resp.data)

        # Notifications
        notif_resp = self.client.get(
            "/api/agent/v1/citizen/notifications/",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
            HTTP_X_CITIZEN_DELEGATION_TOKEN=self.raw_delegation_token,
        )
        self.assertEqual(notif_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(notif_resp.data["count"], 1)
        self.assertEqual(notif_resp.data["results"][0]["title"], "Aadhaar Verified")

    # ========================================================
    # TASK 4: SECURITY & AUDIT LOGGING TESTS
    # ========================================================

    def test_agent_requests_are_logged_to_audit_log(self):
        """All agent operations generate an AgentAuditLog entry."""
        initial_count = AgentAuditLog.objects.count()
        response = self.client.get(
            "/api/agent/v1/schemes/",
            HTTP_X_AGENT_API_KEY=self.raw_agent_key,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AgentAuditLog.objects.count(), initial_count + 1)

        log_entry = AgentAuditLog.objects.latest("created_at")
        self.assertEqual(log_entry.action, "schemes_list")
        self.assertEqual(log_entry.status_code, 200)

    def test_openapi_endpoints_available(self):
        """OpenAPI spec and interactive docs are available."""
        json_resp = self.client.get("/api/agent/v1/openapi.json")
        self.assertEqual(json_resp.status_code, status.HTTP_200_OK)
        self.assertIn("paths", json_resp.json())

        docs_resp = self.client.get("/api/agent/v1/docs/")
        self.assertEqual(docs_resp.status_code, status.HTTP_200_OK)
        self.assertIn("SwaggerUIBundle", docs_resp.content.decode("utf-8"))
