from django.urls import path

from .views import (
    create_application,
    my_applications,
    application_detail,
    application_status,
    submit_application,
    application_documents,
    delete_document,
    download_document,
    download_application_pdf,
    demo_verify_document,
    demo_verify_all_documents,
)


urlpatterns = [
    path("", create_application),
    path("mine/", my_applications),
    # Status endpoint must appear BEFORE the generic <application_number>/ catch-all
    path("<str:application_number>/status/", application_status),
    path("<str:application_number>/", application_detail),
    path("<str:application_number>/submit/", submit_application),
    path("<str:application_number>/documents/", application_documents),
    path("<str:application_number>/documents/<uuid:document_id>/", delete_document),
    path("<str:application_number>/documents/<uuid:document_id>/download/", download_document),
    path("<str:application_number>/documents/<uuid:document_id>/verify/", demo_verify_document),
    path("<str:application_number>/demo-verify/", demo_verify_all_documents),
    path("<str:application_number>/pdf/", download_application_pdf),
]