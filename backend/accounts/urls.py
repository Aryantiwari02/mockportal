from django.urls import path

from agent_api.views import (
    citizen_create_delegation,
    citizen_list_delegations,
    citizen_revoke_delegation,
)
from .views import request_otp, verify_otp


urlpatterns = [
    path("request-otp/", request_otp),
    path("verify-otp/", verify_otp),

    # YojanaSaathi AI Agent delegation management for citizens
    path("agent-delegation/", citizen_create_delegation),
    path("agent-delegations/", citizen_list_delegations),
    path("agent-delegation/<uuid:delegation_id>/revoke/", citizen_revoke_delegation),
]