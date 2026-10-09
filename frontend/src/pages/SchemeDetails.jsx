import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useTranslation } from "../i18n";
import "./SchemeDetails.css";

import { getScheme, downloadBlankFormPdf } from "../api";

const TAB_ORDER = ["overview", "eligibility", "documents", "process"];

const STATUS_STAGES = [
  { key: "DRAFT", desc: "Application saved but not yet submitted." },
  { key: "SUBMITTED", desc: "Application received by the portal." },
  { key: "UNDER_REVIEW", desc: "Documents and details are being reviewed." },
  { key: "CORRECTION_REQUIRED", desc: "Additional or corrected information is required." },
  { key: "APPROVED", desc: "Application approved by the authority." },
  { key: "REJECTED", desc: "Application not approved. Contact the authority for reasons." },
];

function SchemeDetails() {
  const { id } = useParams();
  const { t, getLocalizedScheme } = useTranslation();

  const [rawScheme, setRawScheme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [downloadingBlank, setDownloadingBlank] = useState(false);
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    getScheme(id)
      .then((data) => {
        setRawScheme(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load the scheme details.");
        setLoading(false);
      });
  }, [id]);

  const scheme = getLocalizedScheme(rawScheme);

  const handleDownloadBlank = async () => {
    if (!scheme) return;
    setDownloadingBlank(true);
    try {
      await downloadBlankFormPdf(scheme.id, scheme.title);
    } catch (err) {
      console.error(err);
      alert("Unable to download blank form at this moment.");
    } finally {
      setDownloadingBlank(false);
    }
  };

  if (loading) {
    return (
      <div className="scheme-details-page">
        <div className="container loading-state">
          <p>{t("common.loading")}</p>
        </div>
      </div>
    );
  }

  if (error || !scheme) {
    return (
      <div className="scheme-details-page">
        <div className="container empty-state">
          <h1>{t("schemes.schemeNotFound")}</h1>
          <p>{error}</p>
          <Link to="/schemes" className="scheme-button">{t("schemes.backToSchemes")}</Link>
        </div>
      </div>
    );
  }

  const rules = scheme.eligibility_rules || {};
  const formFields = (scheme.application_fields || []).filter(
    (field) => field.type !== "checkbox"
  );

  const tabLabels = {
    overview: t("schemes.tabOverview"),
    eligibility: t("schemes.tabEligibility"),
    documents: t("schemes.tabDocuments"),
    process: t("schemes.tabProcess"),
  };

  return (
    <div className="scheme-details-page" data-testid="scheme-details-page">

      {/* ── Breadcrumb ── */}
      <div className="scheme-details-breadcrumb">
        <div className="container">
          <nav className="breadcrumb" aria-label="Breadcrumb">
            <Link to="/">{t("nav.home")}</Link>
            <span className="sep" aria-hidden="true">›</span>
            <Link to="/schemes">{t("nav.schemes")}</Link>
            <span className="sep" aria-hidden="true">›</span>
            <span aria-current="page">{scheme.title}</span>
          </nav>
        </div>
      </div>

      {/* ── Scheme Header Banner ── */}
      <div className="details-header" data-testid="scheme-details-header">
        <div className="container">
          <span className="details-category">{scheme.category}</span>

          <h1>{scheme.title}</h1>

          <p className="scheme-short-desc">{scheme.short_description}</p>

          <ul className="details-facts">
            <li>
              <span className="fact-label">{t("schemes.eligibilityCriteria")}</span>
              <span className="fact-value">
                {scheme.eligibility?.length || 0} {t("schemes.eligibilityPoints")}
              </span>
            </li>
            <li>
              <span className="fact-label">{t("schemes.mandatoryDocuments")}</span>
              <span className="fact-value">
                {scheme.documents?.length || 0} {t("schemes.documentsLabel")}
              </span>
            </li>
            <li>
              <span className="fact-label">{t("schemes.applicationModeLabel")}</span>
              <span className="fact-value">{t("schemes.applicationMode")}</span>
            </li>
          </ul>
        </div>
      </div>

      {/* ── Main Content Layout ── */}
      <div className="details-content">
        <div className="container">
          <div className="details-layout">

            {/* ── Left: Tabbed Scheme Information ── */}
            <div className="details-main">

              <div className="details-tabs" role="tablist" aria-label={scheme.title}>
                {TAB_ORDER.map((tab) => (
                  <button
                    key={tab}
                    type="button"
                    role="tab"
                    id={`tab-${tab}`}
                    aria-selected={activeTab === tab}
                    aria-controls={`panel-${tab}`}
                    className={activeTab === tab ? "details-tab active" : "details-tab"}
                    onClick={() => setActiveTab(tab)}
                  >
                    {tabLabels[tab]}
                  </button>
                ))}
              </div>

              {/* Overview */}
              {activeTab === "overview" && (
                <section
                  id="panel-overview"
                  role="tabpanel"
                  aria-labelledby="tab-overview"
                  className="detail-section"
                  data-testid="scheme-about-section"
                >
                  <h2>{t("schemes.aboutScheme")}</h2>
                  <p>{scheme.description}</p>

                  <h3 className="detail-subheading">{t("schemes.keyBenefits")}</h3>
                  {scheme.benefits && scheme.benefits.length > 0 ? (
                    <ul className="detail-list detail-list--benefits">
                      {scheme.benefits.map((item, index) => (
                        <li key={index}>{item}</li>
                      ))}
                    </ul>
                  ) : (
                    <p className="detail-placeholder">
                      Benefit details to be verified. Please refer to the official scheme guidelines.
                    </p>
                  )}

                  {formFields.length > 0 && (
                    <>
                      <h3 className="detail-subheading">{t("schemes.whatYouNeed")}</h3>
                      <p className="detail-hint">{t("schemes.whatYouNeedDesc")}</p>
                      <ul className="field-chips">
                        {formFields.map((field) => (
                          <li key={field.name}>{field.label}</li>
                        ))}
                      </ul>
                    </>
                  )}
                </section>
              )}

              {/* Eligibility */}
              {activeTab === "eligibility" && (
                <section
                  id="panel-eligibility"
                  role="tabpanel"
                  aria-labelledby="tab-eligibility"
                  className="detail-section"
                  data-testid="scheme-eligibility-section"
                >
                  <h2>{t("schemes.eligibilityCriteria")}</h2>
                  {scheme.eligibility && scheme.eligibility.length > 0 ? (
                    <ul className="detail-list">
                      {scheme.eligibility.map((item, index) => (
                        <li key={index}>{item}</li>
                      ))}
                    </ul>
                  ) : (
                    <p className="detail-placeholder">
                      Eligibility criteria to be updated. Please check the official scheme notification.
                    </p>
                  )}

                  {(rules.min_age != null || rules.max_income != null) && (
                    <>
                      <h3 className="detail-subheading">{t("schemes.eligibilityRules")}</h3>
                      <div className="rules-grid">
                        {rules.min_age != null && (
                          <div className="rule-card">
                            <span>{t("schemes.minAge")}</span>
                            <strong>{rules.min_age} {t("schemes.years")}</strong>
                          </div>
                        )}
                        {rules.max_income != null && (
                          <div className="rule-card">
                            <span>{t("schemes.maxIncome")}</span>
                            <strong>₹{Number(rules.max_income).toLocaleString("en-IN")}</strong>
                          </div>
                        )}
                      </div>
                    </>
                  )}
                </section>
              )}

              {/* Required Documents */}
              {activeTab === "documents" && (
                <section
                  id="panel-documents"
                  role="tabpanel"
                  aria-labelledby="tab-documents"
                  className="detail-section"
                  data-testid="scheme-documents-section"
                >
                  <h2>{t("schemes.mandatoryDocuments")}</h2>
                  {scheme.documents && scheme.documents.length > 0 ? (
                    <>
                      <ul className="doc-list">
                        {scheme.documents.map((item, index) => (
                          <li key={index}>
                            <span className="doc-check" aria-hidden="true">✓</span>
                            <strong>{item}</strong>
                          </li>
                        ))}
                      </ul>
                      <p className="doc-note">{t("schemes.documentsNote")}</p>
                    </>
                  ) : (
                    <p className="detail-placeholder">
                      Document requirements to be confirmed with the scheme authority.
                    </p>
                  )}
                </section>
              )}

              {/* Application Process */}
              {activeTab === "process" && (
                <section
                  id="panel-process"
                  role="tabpanel"
                  aria-labelledby="tab-process"
                  className="detail-section"
                  data-testid="scheme-process-section"
                >
                  <h2>{t("schemes.applicationProcess")}</h2>
                  {scheme.application_process && scheme.application_process.length > 0 ? (
                    <ol className="detail-list detail-list--steps">
                      {scheme.application_process.map((item, index) => (
                        <li key={index}>{item}</li>
                      ))}
                    </ol>
                  ) : (
                    <ol className="detail-list detail-list--steps">
                      <li>Log in using your mobile number and OTP via the Citizen Access page.</li>
                      <li>Click <strong>Apply for this Scheme</strong> on this page.</li>
                      <li>Fill in the applicant details and scheme-specific fields in the form.</li>
                      <li>Upload all required supporting documents (PDF, JPG, or PNG).</li>
                      <li>Review all entered details, accept the declaration, and submit.</li>
                      <li>Note your <strong>Application Reference Number</strong> for tracking.</li>
                      <li>Track your application status from the My Applications dashboard.</li>
                    </ol>
                  )}

                  <h3 className="detail-subheading">{t("schemes.statusStagesTitle")}</h3>
                  <div className="status-info-grid">
                    {STATUS_STAGES.map(({ key, desc }) => (
                      <div key={key} className="status-info-item">
                        <strong>{t(`status.${key}`)}</strong>
                        <p>{desc}</p>
                      </div>
                    ))}
                  </div>
                </section>
              )}

            </div>

            {/* ── Right: Action Sidebar ── */}
            <aside className="details-sidebar" data-testid="scheme-sidebar">

              {/* Apply Box */}
              <div className="apply-box" data-testid="apply-box">
                <span className="apply-box-label">{t("schemes.onlineApplication")}</span>
                <h3>{t("schemes.applyOnline")}</h3>
                <p>{t("schemes.applyOnlineDesc")}</p>

                <Link
                  to={`/apply/${scheme.id}`}
                  className="scheme-button apply-btn"
                  data-testid="apply-scheme-button"
                >
                  {t("schemes.applyButton")}
                </Link>

                <button
                  type="button"
                  onClick={handleDownloadBlank}
                  disabled={downloadingBlank}
                  className="btn-download-blank"
                  data-testid="download-blank-form-button"
                >
                  {downloadingBlank ? t("schemes.downloadingBlank") : t("schemes.downloadBlankForm")}
                </button>
              </div>

              {/* Quick Info */}
              <div className="quick-info" data-testid="scheme-quick-info">
                <h3>{t("schemes.quickInfo")}</h3>

                <div className="info-row">
                  <span className="info-lbl">{t("schemes.schemeId")}</span>
                  <span className="info-val monospace">{scheme.id.toUpperCase()}</span>
                </div>

                <div className="info-row">
                  <span className="info-lbl">{t("schemes.categoryLabel")}</span>
                  <span className="info-val">{scheme.category}</span>
                </div>

                <div className="info-row">
                  <span className="info-lbl">{t("schemes.mandatoryDocuments")}</span>
                  <span className="info-val">
                    {scheme.documents ? scheme.documents.length : 0}
                  </span>
                </div>

                <div className="info-row">
                  <span className="info-lbl">{t("schemes.applicationModeLabel")}</span>
                  <span className="info-val">{t("schemes.applicationMode")}</span>
                </div>
              </div>

              {/* Demo Notice */}
              <div className="sidebar-demo-notice">
                <strong>{t("schemes.demoNotice")}</strong>
              </div>

            </aside>

          </div>
        </div>
      </div>

    </div>
  );
}

export default SchemeDetails;
