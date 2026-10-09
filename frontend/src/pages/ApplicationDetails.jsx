import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { useTranslation } from "../i18n";
import "./ApplicationDetails.css";

import {
  demoVerifyAllDocuments,
  downloadApplicationDocument,
  downloadApplicationPdf,
  getApplication,
  getCitizen,
} from "../api";

function ApplicationDetails() {
  const { applicationNumber } = useParams();
  const navigate = useNavigate();
  const citizen = getCitizen();
  const { t, language } = useTranslation();

  const [application, setApplication] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const [downloadingPdf, setDownloadingPdf] = useState(false);
  const [reviewing, setReviewing] = useState(false);
  const [reviewSuccess, setReviewSuccess] = useState("");

  const fetchApplication = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await getApplication(applicationNumber);
      setApplication(data);
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to load application details.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!citizen) {
      navigate("/citizen-access");
      return;
    }
    fetchApplication();
  }, [applicationNumber]);

  const handleCopy = () => {
    navigator.clipboard.writeText(applicationNumber);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadPdf = async () => {
    setDownloadingPdf(true);
    try {
      await downloadApplicationPdf(applicationNumber);
    } catch (err) {
      console.error(err);
      alert("Unable to generate application PDF.");
    } finally {
      setDownloadingPdf(false);
    }
  };

  const handleDownloadDoc = async (docId, fileName) => {
    try {
      await downloadApplicationDocument(applicationNumber, docId, fileName);
    } catch (err) {
      console.error(err);
      alert("Unable to download document.");
    }
  };

  // Demo Review simulation action
  const handleSimulateReview = async () => {
    setReviewing(true);
    setReviewSuccess("");
    try {
      const res = await demoVerifyAllDocuments(applicationNumber);
      setApplication(res.application);
      setReviewSuccess(t("appDetails.reviewSuccessMsg"));
    } catch (err) {
      console.error(err);
      alert(err.message || "Failed to verify documents.");
    } finally {
      setReviewing(false);
    }
  };

  if (loading) {
    return (
      <div className="app-details-loading">
        <div className="spinner"></div>
        <p>{t("common.loading")}</p>
      </div>
    );
  }

  if (error || !application) {
    return (
      <div className="container app-details-error">
        <h2>{t("appDetails.appNotFound")}</h2>
        <p>{error || "The requested application does not exist or you do not have permission."}</p>
        <Link to="/my-services" className="btn-secondary">
          {t("appDetails.backToServices")}
        </Link>
      </div>
    );
  }

  const isSubmitted = ["SUBMITTED", "UNDER_REVIEW", "APPROVED", "REJECTED"].includes(application.status);
  const docsList = application.documents || [];
  const allVerified = application.all_documents_verified;

  return (
    <div className="app-details-page">
      <div className="container">

        {/* Back Link */}
        <div className="app-top-nav">
          <Link to="/my-services" className="back-link">
            {t("appDetails.backToServices")}
          </Link>
        </div>

        {/* Header Application Reference Card */}
        <div className="app-hero-card">
          <div className="app-hero-left">
            <span className="app-category-badge">{application.scheme_category}</span>
            <h1>{application.scheme_title}</h1>
            <div className="app-ref-line">
              <span className="label">{t("appDetails.applicationReference")}</span>
              <strong className="app-num-text">{application.application_number}</strong>
              <button type="button" className="btn-copy-small" onClick={handleCopy}>
                {copied ? t("apply.copied") : t("apply.copy")}
              </button>
            </div>
            <p className="app-submitted-time">
              {t("appDetails.submittedOn")}{" "}
              {application.submitted_at
                ? new Date(application.submitted_at).toLocaleDateString(language === "hi" ? "hi-IN" : language === "kn" ? "kn-IN" : "en-IN", {
                    day: "numeric",
                    month: "long",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  })
                : t("status.DRAFT")}
            </p>
          </div>

          <div className="app-hero-right">
            <div className={`status-large-badge status-${application.status.toLowerCase()}`}>
              {t(`status.${application.status}`, application.status)}
            </div>

            <button
              type="button"
              className="btn-download-pdf-hero"
              onClick={handleDownloadPdf}
              disabled={downloadingPdf}
            >
              {downloadingPdf ? t("appDetails.generatingPdf") : t("appDetails.downloadPdf")}
            </button>
          </div>
        </div>

        {/* Demo Verification Banner (Mock Simulation) */}
        <div className="demo-review-banner">
          <div className="demo-review-info">
            <span className="demo-tag">DEMO REVIEW WORKFLOW</span>
            <h4>{t("appDetails.demoReviewTitle")}</h4>
            <p>
              {t("appDetails.demoReviewDesc")}
            </p>
          </div>
          <div className="demo-review-action">
            <button
              type="button"
              className="btn-demo-verify"
              onClick={handleSimulateReview}
              disabled={reviewing || allVerified}
            >
              {allVerified
                ? t("appDetails.allVerifiedButton")
                : reviewing
                ? t("appDetails.verifyingButton")
                : t("appDetails.simulateButton")}
            </button>
          </div>
        </div>

        {reviewSuccess && (
          <div className="alert-success-banner" role="status">
            <span>✓</span> {reviewSuccess}
          </div>
        )}

        {/* Main Content Grid */}
        <div className="app-content-grid">

          {/* Left Column: Timeline & Documents */}
          <div className="app-col-main">

            {/* Application Timeline Card */}
            <div className="details-card">
              <h3>{t("appDetails.timelineTitle")}</h3>
              <div className="timeline-list">
                <div className="timeline-item completed">
                  <div className="timeline-marker">✓</div>
                  <div className="timeline-text">
                    <strong>{t("appDetails.timelineCreated")}</strong>
                    <small>{new Date(application.created_at).toLocaleDateString(language === "hi" ? "hi-IN" : language === "kn" ? "kn-IN" : "en-IN")}</small>
                  </div>
                </div>

                <div className={`timeline-item ${isSubmitted ? "completed" : "pending"}`}>
                  <div className="timeline-marker">{isSubmitted ? "✓" : "○"}</div>
                  <div className="timeline-text">
                    <strong>{t("appDetails.timelineSubmitted")}</strong>
                    <small>{application.submitted_at ? new Date(application.submitted_at).toLocaleDateString(language === "hi" ? "hi-IN" : language === "kn" ? "kn-IN" : "en-IN") : t("appDetails.pendingSubmission")}</small>
                  </div>
                </div>

                <div className={`timeline-item ${docsList.length > 0 ? "completed" : "pending"}`}>
                  <div className="timeline-marker">{docsList.length > 0 ? "✓" : "○"}</div>
                  <div className="timeline-text">
                    <strong>{t("appDetails.timelineDocsUploaded")}</strong>
                    <small>{docsList.length} {t("appDetails.docsAttachedCount")}</small>
                  </div>
                </div>

                <div className={`timeline-item ${allVerified ? "completed" : isSubmitted ? "active" : "pending"}`}>
                  <div className="timeline-marker">{allVerified ? "✓" : isSubmitted ? "⏳" : "○"}</div>
                  <div className="timeline-text">
                    <strong>{t("appDetails.timelineDocsVerified")}</strong>
                    <small>
                      {allVerified
                        ? t("appDetails.allDocsVerifiedText")
                        : `${application.verified_documents_count || 0} / ${docsList.length} ${t("myServices.verifiedCountSuffix")}`}
                    </small>
                  </div>
                </div>

                <div className={`timeline-item ${application.status === "APPROVED" ? "completed" : "pending"}`}>
                  <div className="timeline-marker">{application.status === "APPROVED" ? "✓" : "○"}</div>
                  <div className="timeline-text">
                    <strong>{t("appDetails.timelineDecision")}</strong>
                    <small>{application.status === "APPROVED" ? t("appDetails.sanctionedText") : t("appDetails.underReviewText")}</small>
                  </div>
                </div>
              </div>
            </div>

            {/* Documents Verification Status Card */}
            <div className="details-card">
              <div className="card-header-flex">
                <h3>{t("appDetails.docStatusTitle")}</h3>
                <span className="doc-count-tag">
                  {application.verified_documents_count || 0} / {docsList.length} {t("myServices.verifiedCountSuffix")}
                </span>
              </div>

              {docsList.length === 0 ? (
                <p className="empty-docs-text">{t("appDetails.noDocsText")}</p>
              ) : (
                <div className="doc-verify-list">
                  {docsList.map((doc) => {
                    const isDocVerified = doc.verification_status === "VERIFIED";

                    return (
                      <div key={doc.id} className={`doc-item-row ${isDocVerified ? "verified" : ""}`}>
                        <div className="doc-item-info">
                          <span className="doc-type-icon">{isDocVerified ? "✓" : "📄"}</span>
                          <div>
                            <h4>{doc.document_type}</h4>
                            <p className="doc-meta">
                              File: <strong>{doc.file_name}</strong> • {(doc.file_size / 1024).toFixed(1)} KB • {new Date(doc.uploaded_at).toLocaleDateString(language === "hi" ? "hi-IN" : language === "kn" ? "kn-IN" : "en-IN")}
                            </p>
                            {doc.remarks && (
                              <p className="doc-remarks">Note: {doc.remarks}</p>
                            )}
                          </div>
                        </div>

                        <div className="doc-item-action">
                          <span className={`status-badge-pill status-${doc.verification_status.toLowerCase()}`}>
                            {isDocVerified
                              ? `✓ ${t("status.VERIFIED")}`
                              : t(`status.${doc.verification_status}`, doc.verification_status)}
                          </span>

                          <button
                            type="button"
                            className="btn-doc-download"
                            onClick={() => handleDownloadDoc(doc.id, doc.file_name)}
                          >
                            {t("appDetails.downloadDoc")}
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}

              {allVerified && (
                <div className="all-verified-callout">
                  <span className="callout-icon">🎉</span>
                  <div>
                    <strong>{t("appDetails.allVerifiedCalloutTitle")}</strong>
                    <p>{t("appDetails.allVerifiedCalloutDesc")}</p>
                  </div>
                </div>
              )}
            </div>

          </div>

          {/* Right Column: Applicant Particulars */}
          <div className="app-col-side">

            {/* Applicant Particulars Card */}
            <div className="details-card">
              <h3>{t("appDetails.applicantParticularsTitle")}</h3>
              <div className="side-info-list">
                <div>
                  <strong>{t("apply.fullName")}:</strong>
                  <span>{application.form_data?.full_name || application.form_data?.applicant_name || citizen.full_name || "Citizen"}</span>
                </div>
                <div>
                  <strong>{t("apply.registeredMobile")}:</strong>
                  <span>+91 {citizen.mobile} ({t("status.VERIFIED")})</span>
                </div>
                <div>
                  <strong>{t("apply.address")}:</strong>
                  <span>{application.form_data?.address || citizen.address || "As provided"}</span>
                </div>
              </div>
            </div>

            {/* Scheme Form Answers Card */}
            <div className="details-card">
              <h3>{t("appDetails.submittedAnswersTitle")}</h3>
              <div className="side-info-list">
                {application.form_data && Object.keys(application.form_data).length > 0 ? (
                  Object.entries(application.form_data).map(([key, val]) => {
                    if (["full_name", "applicant_name", "address", "declaration_consent"].includes(key)) return null;
                    const display = val === true ? "Yes" : val === false ? "No" : String(val);
                    return (
                      <div key={key}>
                        <strong>{key.replace(/_/g, " ").toUpperCase()}:</strong>
                        <span>{display}</span>
                      </div>
                    );
                  })
                ) : (
                  <p>Standard verified citizen credentials</p>
                )}
              </div>
            </div>

            {/* Mock Notice */}
            <div className="mock-disclaimer-box">
              <small>
                <strong>{t("appDetails.demoDisclaimerTitle")}</strong> {t("appDetails.demoDisclaimerDesc")}
              </small>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}

export default ApplicationDetails;
