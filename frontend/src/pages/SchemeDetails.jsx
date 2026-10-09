import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useTranslation } from "../i18n";
import "./SchemeDetails.css";

import { getScheme, downloadBlankFormPdf } from "../api";

function SchemeDetails() {
  const { id } = useParams();
  const { t, getLocalizedScheme } = useTranslation();

  const [rawScheme, setRawScheme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [downloadingBlank, setDownloadingBlank] = useState(false);

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
          <span className="scheme-govt-level">
            {scheme.govt_level || "Government Scheme"} &nbsp;|&nbsp; {scheme.ministry || scheme.category}
          </span>

          <span className="details-category">{scheme.category}</span>

          <h1>{scheme.title}</h1>

          {scheme.short_name && (
            <span className="scheme-acronym">{scheme.short_name}</span>
          )}

          <p className="scheme-short-desc">{scheme.short_description}</p>
        </div>
      </div>

      {/* ── Main Content Layout ── */}
      <div className="details-content">
        <div className="container">
          <div className="details-layout">

            {/* ── Left: Scheme Information ── */}
            <div className="details-main">

              {/* About */}
              <section className="detail-section" data-testid="scheme-about-section">
                <h2>{t("schemes.aboutScheme")}</h2>
                <p>{scheme.description}</p>

                {scheme.purpose && (
                  <div className="alert alert-info">
                    <strong>Purpose: </strong>{scheme.purpose}
                  </div>
                )}
              </section>

              {/* Eligibility */}
              <section className="detail-section" data-testid="scheme-eligibility-section">
                <h2>{t("schemes.eligibilityCriteria")}</h2>
                {scheme.eligibility && scheme.eligibility.length > 0 ? (
                  <ul className="detail-list">
                    {scheme.eligibility.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="detail-placeholder">Eligibility criteria to be updated. Please check the official scheme notification.</p>
                )}
              </section>

              {/* Benefits */}
              <section className="detail-section" data-testid="scheme-benefits-section">
                <h2>{t("schemes.keyBenefits")}</h2>
                {scheme.benefits && scheme.benefits.length > 0 ? (
                  <ul className="detail-list detail-list--benefits">
                    {scheme.benefits.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="detail-placeholder">Benefit details to be verified. Please refer to the official scheme guidelines.</p>
                )}
              </section>

              {/* Required Documents */}
              <section className="detail-section" data-testid="scheme-documents-section">
                <h2>{t("schemes.mandatoryDocuments")}</h2>
                {scheme.documents && scheme.documents.length > 0 ? (
                  <>
                    <ul className="detail-list detail-list--docs">
                      {scheme.documents.map((item, index) => (
                        <li key={index}>
                          <span className="doc-bullet">📄</span>
                          <strong>{item}</strong>
                        </li>
                      ))}
                    </ul>
                    <p className="doc-note">
                      Documents may be uploaded through the online application form below.
                      Accepted formats: PDF, JPG, JPEG, PNG (max 5 MB per document).
                    </p>
                  </>
                ) : (
                  <p className="detail-placeholder">Document requirements to be confirmed with the scheme authority.</p>
                )}
              </section>

              {/* Application Process */}
              <section className="detail-section" data-testid="scheme-process-section">
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
                    <li>Review all entered details, check the declaration box, and submit.</li>
                    <li>Note your <strong>Application Reference Number</strong> for tracking.</li>
                    <li>Track your application status from the <em>My Applications</em> dashboard.</li>
                  </ol>
                )}
              </section>

              {/* Status Information */}
              <section className="detail-section">
                <h2>Application Status Information</h2>
                <div className="status-info-grid">
                  {[
                    { label: "Draft", desc: "Application is saved but not yet submitted." },
                    { label: "Submitted", desc: "Application has been received by the portal." },
                    { label: "Under Review", desc: "Documents and details are being reviewed." },
                    { label: "Correction Required", desc: "Additional or corrected information is needed." },
                    { label: "Approved", desc: "Application has been approved by the authority." },
                    { label: "Rejected", desc: "Application was not approved. Contact the authority for reasons." },
                  ].map(({ label, desc }) => (
                    <div key={label} className="status-info-item">
                      <strong>{label}</strong>
                      <p>{desc}</p>
                    </div>
                  ))}
                </div>
              </section>

              {/* Official Sources Notice */}
              <section className="detail-section scheme-source-notice">
                <h2>Official Sources &amp; Verification</h2>
                {scheme.official_url && (
                  <p>
                    <strong>Official Website: </strong>
                    <a href={scheme.official_url} target="_blank" rel="noopener noreferrer">{scheme.official_url}</a>
                  </p>
                )}
                <div className="alert alert-warning">
                  <strong>ⓘ Important: </strong>
                  This portal displays information for demonstration purposes. Scheme eligibility
                  rules, benefit amounts, and document requirements may change. Always verify the
                  current rules with the responsible government authority before applying.
                </div>
              </section>

            </div>

            {/* ── Right: Action Sidebar ── */}
            <aside className="details-sidebar" data-testid="scheme-sidebar">

              {/* Apply Box */}
              <div className="apply-box" data-testid="apply-box">
                <span className="apply-box-label">CITIZEN ONLINE APPLICATION</span>
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
                  <span className="info-lbl">Scheme ID</span>
                  <span className="info-val monospace">{scheme.id.toUpperCase()}</span>
                </div>

                <div className="info-row">
                  <span className="info-lbl">Category</span>
                  <span className="info-val">{scheme.category}</span>
                </div>

                {scheme.ministry && (
                  <div className="info-row">
                    <span className="info-lbl">Ministry</span>
                    <span className="info-val">{scheme.ministry}</span>
                  </div>
                )}

                {scheme.govt_level && (
                  <div className="info-row">
                    <span className="info-lbl">Level</span>
                    <span className="info-val">{scheme.govt_level}</span>
                  </div>
                )}

                <div className="info-row">
                  <span className="info-lbl">Documents Required</span>
                  <span className="info-val">
                    {scheme.documents ? scheme.documents.length : 0} {t("schemes.itemsCount")}
                  </span>
                </div>

                <div className="info-row">
                  <span className="info-lbl">Mode</span>
                  <span className="info-val">{t("schemes.applicationMode")}</span>
                </div>
              </div>

              {/* Demo Notice */}
              <div className="sidebar-demo-notice">
                <strong>ⓘ {t("schemes.demoNotice")}</strong>
              </div>

            </aside>

          </div>
        </div>
      </div>

    </div>
  );
}

export default SchemeDetails;