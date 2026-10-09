import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { useTranslation } from "../i18n";
import "./ApplyScheme.css";

import {
  createApplication,
  downloadApplicationPdf,
  downloadBlankFormPdf,
  getApplicationDocuments,
  getCitizen,
  getScheme,
  submitApplication,
  uploadApplicationDocument,
  deleteApplicationDocument,
} from "../api";

function ApplyScheme() {
  const { schemeId } = useParams();
  const navigate = useNavigate();
  const { t, language, getLocalizedScheme } = useTranslation();

  const citizen = getCitizen();

  // Core state
  const [rawScheme, setRawScheme] = useState(null);
  const [application, setApplication] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [formData, setFormData] = useState({});

  // UI state
  const [step, setStep] = useState(1); // 1: Applicant, 2: Scheme Fields, 3: Documents, 4: Review, 5: Confirmation
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [uploadingDoc, setUploadingDoc] = useState({});
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState({});
  const [copiedAppNo, setCopiedAppNo] = useState(false);
  const [downloadingBlank, setDownloadingBlank] = useState(false);
  const [downloadingPdf, setDownloadingPdf] = useState(false);

  const scheme = getLocalizedScheme(rawScheme);

  // 1. Fetch Scheme and existing Draft Application
  useEffect(() => {
    let isMounted = true;

    async function loadData() {
      try {
        setLoading(true);
        setError("");

        const schemeData = await getScheme(schemeId);
        if (!isMounted) return;
        setRawScheme(schemeData);

        if (citizen) {
          // Create or retrieve draft application
          try {
            const appData = await createApplication(schemeId, {});
            if (isMounted) {
              setApplication(appData);
              setFormData(appData.form_data || {});

              // Fetch existing documents for this draft
              const docs = await getApplicationDocuments(appData.application_number);
              setDocuments(docs || []);

              // If already submitted, jump to confirmation or details
              if (appData.status !== "DRAFT" && appData.status !== "CORRECTION_REQUIRED") {
                setStep(5);
              }
            }
          } catch (appErr) {
            console.error("Draft application error:", appErr);
          }
        }
      } catch (err) {
        console.error(err);
        if (isMounted) {
          setError(t("schemes.schemeNotFound"));
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    loadData();

    return () => {
      isMounted = false;
    };
  }, [schemeId]);

  // Handle Form Input changes
  const handleInputChange = (fieldName, value) => {
    setFormData((prev) => ({
      ...prev,
      [fieldName]: value,
    }));

    if (fieldErrors[fieldName]) {
      setFieldErrors((prev) => {
        const updated = { ...prev };
        delete updated[fieldName];
        return updated;
      });
    }
  };

  // Step 1 Validation (Applicant details)
  const validateStep1 = () => {
    return true;
  };

  // Step 2 Validation (Scheme fields)
  const validateStep2 = () => {
    const errors = {};
    const schemeFields = scheme?.application_fields || [];

    for (const field of schemeFields) {
      if (field.required) {
        const val = formData[field.name];
        if (val === undefined || val === null || (typeof val === "string" && !val.trim()) || val === false) {
          errors[field.name] = `${field.label || field.name} ${t("common.required")}`;
        }
      }
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Build canonical & localized document list
  const docList = (rawScheme?.documents || []).map((canonicalName, idx) => {
    const localizedName = scheme?.documents?.[idx] || canonicalName;
    return {
      canonicalName,
      localizedName,
      isOptional: canonicalName.toLowerCase().includes("where applicable"),
    };
  });

  // Step 3 Validation (Documents)
  const validateStep3 = () => {
    const uploadedTypes = new Set(documents.map((d) => d.document_type));

    for (const doc of docList) {
      if (doc.isOptional) continue;
      if (!uploadedTypes.has(doc.canonicalName)) {
        setError(`${t("common.required")}: "${doc.localizedName}"`);
        return false;
      }
    }

    setError("");
    return true;
  };

  // Navigation handlers
  const handleNextStep = () => {
    setError("");
    if (step === 1) {
      if (validateStep1()) setStep(2);
    } else if (step === 2) {
      if (validateStep2()) setStep(3);
    } else if (step === 3) {
      if (validateStep3()) setStep(4);
    }
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handlePrevStep = () => {
    setError("");
    if (step > 1) {
      setStep(step - 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  // Document Upload Handler
  const handleFileUpload = async (canonicalDocType, file) => {
    if (!file || !application) return;

    if (file.size > 5 * 1024 * 1024) {
      alert("File size exceeds 5MB limit. Please upload a smaller file.");
      return;
    }

    const validExts = [".pdf", ".jpg", ".jpeg", ".png"];
    const fileExt = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();
    if (!validExts.includes(fileExt)) {
      alert("Invalid file format. Allowed formats: PDF, JPG, JPEG, PNG.");
      return;
    }

    setUploadingDoc((prev) => ({ ...prev, [canonicalDocType]: true }));
    setError("");

    try {
      const savedDoc = await uploadApplicationDocument(
        application.application_number,
        canonicalDocType,
        file
      );

      setDocuments((prev) => {
        const filtered = prev.filter((d) => d.document_type !== canonicalDocType);
        return [...filtered, savedDoc];
      });
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to upload document.");
    } finally {
      setUploadingDoc((prev) => ({ ...prev, [canonicalDocType]: false }));
    }
  };

  // Remove Document Handler
  const handleRemoveDoc = async (canonicalDocType, locDocName) => {
    const docObj = documents.find((d) => d.document_type === canonicalDocType);
    if (!docObj || !application) return;

    if (!window.confirm(`${t("common.cancel")} ${locDocName}?`)) {
      return;
    }

    try {
      await deleteApplicationDocument(application.application_number, docObj.id);
      setDocuments((prev) => prev.filter((d) => d.id !== docObj.id));
    } catch (err) {
      console.error(err);
      alert("Unable to remove document.");
    }
  };

  // Submit Application Handler
  const handleSubmitApplication = async () => {
    if (!application) return;

    setError("");
    setSubmitting(true);

    try {
      const response = await submitApplication(
        application.application_number,
        formData
      );

      setApplication(response.application);
      setStep(5); // Confirmation
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      console.error(err);
      setError(err.message || "Submission failed. Please check required fields.");
    } finally {
      setSubmitting(false);
    }
  };

  // Copy Application Number
  const handleCopyAppNo = () => {
    if (!application?.application_number) return;
    navigator.clipboard.writeText(application.application_number);
    setCopiedAppNo(true);
    setTimeout(() => setCopiedAppNo(false), 2500);
  };

  // Download PDF
  const handleDownloadPdf = async () => {
    if (!application?.application_number) return;
    setDownloadingPdf(true);
    try {
      await downloadApplicationPdf(application.application_number);
    } catch (err) {
      console.error(err);
      alert("Unable to generate PDF.");
    } finally {
      setDownloadingPdf(false);
    }
  };

  // Download Blank Form
  const handleDownloadBlank = async () => {
    if (!scheme) return;
    setDownloadingBlank(true);
    try {
      await downloadBlankFormPdf(scheme.id, scheme.title);
    } catch (err) {
      console.error(err);
      alert("Unable to download blank form.");
    } finally {
      setDownloadingBlank(false);
    }
  };

  if (loading) {
    return (
      <div className="apply-page-loading">
        <div className="spinner"></div>
        <p>{t("common.loading")}</p>
      </div>
    );
  }

  if (error && !scheme) {
    return (
      <div className="container apply-error-container">
        <h2>{t("schemes.schemeNotFound")}</h2>
        <p>{error}</p>
        <Link to="/schemes" className="btn-secondary">
          {t("schemes.backToSchemes")}
        </Link>
      </div>
    );
  }

  // Not logged in gate
  if (!citizen) {
    return (
      <div className="apply-page-wrapper">
        <div className="container">
          <div className="auth-gate-card">
            <div className="auth-gate-icon">🔐</div>
            <h2>{t("apply.authGateTitle")}</h2>
            <p>
              {t("apply.authGateDesc")}
            </p>
            <div className="auth-gate-actions">
              <Link to="/citizen-access" className="btn-primary">
                {t("apply.authGateButton")}
              </Link>
              <button
                type="button"
                className="btn-secondary"
                onClick={handleDownloadBlank}
                disabled={downloadingBlank}
              >
                {downloadingBlank ? t("schemes.downloadingBlank") : t("apply.blankPdfButton")}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const uploadedDocMap = {};
  documents.forEach((d) => {
    uploadedDocMap[d.document_type] = d;
  });

  return (
    <div className="apply-page-wrapper">
      <div className="container">

        {/* Top Header Banner */}
        <div className="apply-header-banner" data-testid="apply-header-banner">
          <div className="apply-header-info">
            <span className="apply-category-tag">{scheme.category}</span>
            <h1>{t("apply.pageTitle")} {scheme.title}</h1>
            <p>{scheme.short_description}</p>
          </div>
          <div className="apply-header-actions">
            <button
              type="button"
              className="btn-blank-pdf"
              data-testid="apply-download-blank-btn"
              onClick={handleDownloadBlank}
              disabled={downloadingBlank}
            >
              {downloadingBlank ? t("schemes.downloadingBlank") : t("apply.blankPdfButton")}
            </button>
          </div>
        </div>

        {/* Stepper Progress Bar */}
        {step < 5 && (
          <div className="stepper-container" data-testid="apply-stepper">
            <div className={`step-item ${step === 1 ? "active" : step > 1 ? "completed" : ""}`} data-testid="step-1-indicator">
              <div className="step-circle">{step > 1 ? "✓" : "1"}</div>
              <div className="step-label">{t("apply.step1")}</div>
            </div>
            <div className="step-line"></div>
            <div className={`step-item ${step === 2 ? "active" : step > 2 ? "completed" : ""}`} data-testid="step-2-indicator">
              <div className="step-circle">{step > 2 ? "✓" : "2"}</div>
              <div className="step-label">{t("apply.step2")}</div>
            </div>
            <div className="step-line"></div>
            <div className={`step-item ${step === 3 ? "active" : step > 3 ? "completed" : ""}`} data-testid="step-3-indicator">
              <div className="step-circle">{step > 3 ? "✓" : "3"}</div>
              <div className="step-label">{t("apply.step3")}</div>
            </div>
            <div className="step-line"></div>
            <div className={`step-item ${step === 4 ? "active" : step > 4 ? "completed" : ""}`} data-testid="step-4-indicator">
              <div className="step-circle">{step > 4 ? "✓" : "4"}</div>
              <div className="step-label">{t("apply.step4")}</div>
            </div>
          </div>
        )}

        {/* Global Error Banner */}
        {error && (
          <div className="alert-error" role="alert" data-testid="apply-error-banner">
            <span>⚠</span> {error}
          </div>
        )}

        {/* Form Container */}
        <div className="apply-form-card">

          {/* =========================================================
              STEP 1: APPLICANT DETAILS
          ========================================================= */}
          {step === 1 && (
            <div className="step-content">
              <div className="step-header">
                <h2>{t("apply.step1Title")}</h2>
                <p>
                  {t("apply.step1Desc")}
                </p>
              </div>

              <div className="info-grid">
                <div className="info-box">
                  <label>{t("apply.registeredMobile")}</label>
                  <div className="info-value verified-value">
                    +91 {citizen.mobile} <span className="pill-verified">{t("apply.verifiedBadge")}</span>
                  </div>
                </div>

                <div className="info-box">
                  <label htmlFor="apply-full-name">{t("apply.fullName")}</label>
                  <input
                    id="apply-full-name"
                    type="text"
                    data-testid="apply-full-name-input"
                    value={formData.full_name || citizen.full_name || ""}
                    onChange={(e) => handleInputChange("full_name", e.target.value)}
                    placeholder={t("apply.fullNamePlaceholder")}
                    className="form-input"
                    aria-label={t("apply.fullName")}
                  />
                </div>

                <div className="info-box">
                  <label htmlFor="apply-email">{t("apply.email")}</label>
                  <input
                    id="apply-email"
                    type="email"
                    data-testid="apply-email-input"
                    value={formData.email || citizen.email || ""}
                    onChange={(e) => handleInputChange("email", e.target.value)}
                    placeholder={t("apply.emailPlaceholder")}
                    className="form-input"
                    aria-label={t("apply.email")}
                  />
                </div>

                <div className="info-box full-width">
                  <label htmlFor="apply-address">{t("apply.address")}</label>
                  <textarea
                    id="apply-address"
                    rows={3}
                    data-testid="apply-address-input"
                    value={formData.address || citizen.address || ""}
                    onChange={(e) => handleInputChange("address", e.target.value)}
                    placeholder={t("apply.addressPlaceholder")}
                    className="form-textarea"
                    aria-label={t("apply.address")}
                  />
                </div>
              </div>

              <div className="scheme-eligibility-summary">
                <h3>{t("apply.eligibilitySummaryTitle")}</h3>
                <ul>
                  {scheme.eligibility && scheme.eligibility.map((el, i) => (
                    <li key={i}>{el}</li>
                  ))}
                </ul>
              </div>

              <div className="form-buttons-row">
                <Link to={`/schemes/${scheme.id}`} className="btn-secondary" data-testid="apply-step1-cancel-btn">
                  {t("apply.cancel")}
                </Link>
                <button type="button" className="btn-primary" data-testid="apply-step1-next-btn" onClick={handleNextStep}>
                  {t("apply.nextSchemeDetails")}
                </button>
              </div>
            </div>
          )}

          {/* =========================================================
              STEP 2: SCHEME SPECIFIC FIELDS
          ========================================================= */}
          {step === 2 && (
            <div className="step-content">
              <div className="step-header">
                <h2>{t("apply.step2Title")}</h2>
                <p>
                  {t("apply.step2Desc")} (<strong>{scheme.title}</strong>)
                </p>
              </div>

              <div className="dynamic-fields-grid">
                {scheme.application_fields && scheme.application_fields.length > 0 ? (
                  scheme.application_fields.map((field) => {
                    const fieldVal = formData[field.name] !== undefined ? formData[field.name] : "";
                    const hasError = !!fieldErrors[field.name];

                    return (
                      <div
                        key={field.name}
                        className={`field-group ${field.type === "textarea" ? "full-width" : ""}`}
                      >
                        <label className="field-label">
                          {field.label || field.name}
                          {field.required && <span className="req-star">*</span>}
                        </label>

                        {field.help_text && (
                          <span className="field-help">{field.help_text}</span>
                        )}

                        {/* SELECT */}
                        {field.type === "select" && (
                          <select
                            id={`field-${field.name}`}
                            className={`form-select ${hasError ? "input-err" : ""}`}
                            data-testid={`apply-field-${field.name}`}
                            value={fieldVal}
                            onChange={(e) => handleInputChange(field.name, e.target.value)}
                            aria-label={field.label || field.name}
                            aria-required={field.required}
                          >
                            <option value="">{t("apply.selectOption")}</option>
                            {field.options && field.options.map((opt) => (
                              <option key={opt} value={opt}>{opt}</option>
                            ))}
                          </select>
                        )}

                        {/* RADIO */}
                        {field.type === "radio" && (
                          <div className="radio-group" role="radiogroup" aria-label={field.label || field.name}>
                            {field.options && field.options.map((opt) => (
                              <label key={opt} className="radio-option">
                                <input
                                  type="radio"
                                  name={field.name}
                                  value={opt}
                                  data-testid={`apply-field-${field.name}-${opt}`}
                                  checked={fieldVal === opt}
                                  onChange={() => handleInputChange(field.name, opt)}
                                />
                                <span>{opt}</span>
                              </label>
                            ))}
                          </div>
                        )}

                        {/* CHECKBOX */}
                        {field.type === "checkbox" && (
                          <label className="checkbox-option">
                            <input
                              type="checkbox"
                              data-testid={`apply-field-${field.name}`}
                              checked={!!fieldVal}
                              onChange={(e) => handleInputChange(field.name, e.target.checked)}
                              aria-label={field.label}
                            />
                            <span>{field.label}</span>
                          </label>
                        )}

                        {/* TEXTAREA */}
                        {field.type === "textarea" && (
                          <textarea
                            id={`field-${field.name}`}
                            rows={3}
                            data-testid={`apply-field-${field.name}`}
                            className={`form-textarea ${hasError ? "input-err" : ""}`}
                            placeholder={field.placeholder || ""}
                            value={fieldVal}
                            onChange={(e) => handleInputChange(field.name, e.target.value)}
                            aria-label={field.label || field.name}
                            aria-required={field.required}
                          />
                        )}

                        {/* INPUT TYPES (text, number, date, tel, email) */}
                        {["text", "number", "date", "tel", "email"].includes(field.type) && (
                          <input
                            id={`field-${field.name}`}
                            type={field.type}
                            data-testid={`apply-field-${field.name}`}
                            className={`form-input ${hasError ? "input-err" : ""}`}
                            placeholder={field.placeholder || ""}
                            value={fieldVal}
                            onChange={(e) => handleInputChange(field.name, e.target.value)}
                            aria-label={field.label || field.name}
                            aria-required={field.required}
                          />
                        )}

                        {hasError && (
                          <span className="err-msg">{fieldErrors[field.name]}</span>
                        )}
                      </div>
                    );
                  })
                ) : (
                  <div className="default-fields-notice">
                    <p>{t("common.loading")}</p>
                  </div>
                )}
              </div>

              <div className="form-buttons-row">
                <button type="button" className="btn-secondary" data-testid="apply-step2-back-btn" onClick={handlePrevStep}>
                  {t("apply.backApplicant")}
                </button>
                <button type="button" className="btn-primary" data-testid="apply-step2-next-btn" onClick={handleNextStep}>
                  {t("apply.nextDocuments")}
                </button>
              </div>
            </div>
          )}

          {/* =========================================================
              STEP 3: DOCUMENT UPLOADS
          ========================================================= */}
          {step === 3 && (
            <div className="step-content">
              <div className="step-header">
                <h2>{t("apply.step3Title")}</h2>
                <p>
                  {t("apply.step3Desc")}
                </p>
              </div>

              <div className="documents-upload-list">
                {docList.map((doc) => {
                  const uploaded = uploadedDocMap[doc.canonicalName];
                  const isUploading = !!uploadingDoc[doc.canonicalName];

                  return (
                    <div key={doc.canonicalName} className={`doc-upload-card ${uploaded ? "uploaded" : ""}`}
                      data-testid={`doc-upload-card-${doc.canonicalName.replace(/\s+/g, "-").toLowerCase()}`}
                    >
                      <div className="doc-card-info">
                        <div className="doc-title-row">
                          <span className="doc-icon">{uploaded ? "📄" : "📁"}</span>
                          <div>
                            <h4>
                              {doc.localizedName}
                              {doc.isOptional ? (
                                <span className="doc-optional-badge">{t("apply.optionalDoc")}</span>
                              ) : (
                                <span className="doc-req-star">{t("apply.requiredDoc")}</span>
                              )}
                            </h4>
                            <p className="doc-desc">
                              {uploaded ? (
                                <>
                                  File: <strong>{uploaded.file_name}</strong> • {(uploaded.file_size / 1024).toFixed(1)} KB • Status: <span className="status-tag status-uploaded">{t(`status.${uploaded.verification_status}`, uploaded.verification_status)}</span>
                                </>
                              ) : (
                                doc.localizedName
                              )}
                            </p>
                          </div>
                        </div>
                      </div>

                      <div className="doc-card-action">
                        {isUploading ? (
                          <div className="uploading-spinner">{t("common.loading")}</div>
                        ) : uploaded ? (
                          <div className="uploaded-actions">
                            <span className="upload-success-badge" data-testid={`doc-uploaded-badge-${doc.canonicalName.replace(/\s+/g, "-").toLowerCase()}`}>{t("apply.uploaded")}</span>
                            <button
                              type="button"
                              className="btn-remove-doc"
                              data-testid={`doc-remove-btn-${doc.canonicalName.replace(/\s+/g, "-").toLowerCase()}`}
                              onClick={() => handleRemoveDoc(doc.canonicalName, doc.localizedName)}
                            >
                              {t("apply.replaceRemove")}
                            </button>
                          </div>
                        ) : (
                          <label
                            className="btn-upload-label"
                            data-testid={`doc-upload-label-${doc.canonicalName.replace(/\s+/g, "-").toLowerCase()}`}
                          >
                            {t("apply.uploadFile")}
                            <input
                              type="file"
                              accept=".pdf,.jpg,.jpeg,.png"
                              aria-label={`Upload ${doc.localizedName}`}
                              data-testid={`doc-file-input-${doc.canonicalName.replace(/\s+/g, "-").toLowerCase()}`}
                              style={{ display: "none" }}
                              onChange={(e) => {
                                if (e.target.files && e.target.files[0]) {
                                  handleFileUpload(doc.canonicalName, e.target.files[0]);
                                }
                              }}
                            />
                          </label>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="form-buttons-row">
                <button type="button" className="btn-secondary" data-testid="apply-step3-back-btn" onClick={handlePrevStep}>
                  {t("apply.backSchemeDetails")}
                </button>
                <button type="button" className="btn-primary" data-testid="apply-step3-next-btn" onClick={handleNextStep}>
                  {t("apply.nextReview")}
                </button>
              </div>
            </div>
          )}

          {/* =========================================================
              STEP 4: REVIEW BEFORE SUBMISSION
          ========================================================= */}
          {step === 4 && (
            <div className="step-content">
              <div className="step-header">
                <h2>{t("apply.step4Title")}</h2>
                <p>
                  {t("apply.step4Desc")}
                </p>
              </div>

              {/* Review Section 1: Applicant Details */}
              <div className="review-section">
                <div className="review-section-header">
                  <h3>{t("apply.applicantSection")}</h3>
                  <button type="button" className="btn-edit-step" onClick={() => setStep(1)}>
                    {t("apply.edit")}
                  </button>
                </div>
                <div className="review-grid">
                  <div>
                    <strong>{t("apply.fullName")}:</strong>
                    <span>{formData.full_name || citizen.full_name || "N/A"}</span>
                  </div>
                  <div>
                    <strong>{t("apply.registeredMobile")}:</strong>
                    <span>+91 {citizen.mobile}</span>
                  </div>
                  <div>
                    <strong>{t("apply.email")}:</strong>
                    <span>{formData.email || citizen.email || "N/A"}</span>
                  </div>
                  <div>
                    <strong>{t("apply.address")}:</strong>
                    <span>{formData.address || citizen.address || "N/A"}</span>
                  </div>
                </div>
              </div>

              {/* Review Section 2: Scheme Specific Particulars */}
              <div className="review-section">
                <div className="review-section-header">
                  <h3>{t("apply.schemeSection")}</h3>
                  <button type="button" className="btn-edit-step" onClick={() => setStep(2)}>
                    {t("apply.edit")}
                  </button>
                </div>
                <div className="review-grid">
                  {scheme.application_fields && scheme.application_fields.map((f) => {
                    const val = formData[f.name];
                    const display = val === true ? "Yes" : val === false ? "No" : val || "N/A";
                    return (
                      <div key={f.name}>
                        <strong>{f.label || f.name}:</strong>
                        <span>{display}</span>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Review Section 3: Uploaded Documents */}
              <div className="review-section">
                <div className="review-section-header">
                  <h3>{t("apply.docsSection")}</h3>
                  <button type="button" className="btn-edit-step" onClick={() => setStep(3)}>
                    {t("apply.edit")}
                  </button>
                </div>
                <ul className="review-docs-list">
                  {docList.map((doc) => {
                    const uploaded = uploadedDocMap[doc.canonicalName];
                    return (
                      <li key={doc.canonicalName}>
                        {uploaded ? (
                          <span className="doc-ok">✓ <strong>{doc.localizedName}</strong> ({uploaded.file_name})</span>
                        ) : (
                          <span className="doc-missing">⚠ <strong>{doc.localizedName}</strong> ({t("apply.requiredDoc")})</span>
                        )}
                      </li>
                    );
                  })}
                </ul>
              </div>

              {/* Declaration Checkbox */}
              <div className="declaration-card">
                <label className="declaration-label">
                  <input
                    type="checkbox"
                    id="apply-declaration-consent"
                    data-testid="apply-declaration-checkbox"
                    checked={!!formData.declaration_consent}
                    onChange={(e) => handleInputChange("declaration_consent", e.target.checked)}
                    aria-label="Statutory declaration consent"
                  />
                  <span>
                    <strong>{t("apply.statutoryDeclaration")}</strong> {t("apply.declarationText")}
                  </span>
                </label>
              </div>

              <div className="form-buttons-row">
                <button type="button" className="btn-secondary" data-testid="apply-step4-back-btn" onClick={handlePrevStep}>
                  {t("apply.backDocs")}
                </button>
                <button
                  type="button"
                  className="btn-submit"
                  data-testid="apply-submit-btn"
                  disabled={submitting || !formData.declaration_consent}
                  onClick={handleSubmitApplication}
                  aria-disabled={submitting || !formData.declaration_consent}
                >
                  {submitting ? t("apply.submittingButton") : t("apply.submitButton")}
                </button>
              </div>
            </div>
          )}

          {/* =========================================================
              STEP 5: CONFIRMATION / SUBMISSION SUCCESS
          ========================================================= */}
          {step === 5 && application && (
            <div className="confirmation-content">
              <div className="confirmation-badge">✓</div>
              <h2>{t("apply.successTitle")}</h2>
              <p className="confirmation-sub">
                {t("apply.successSub")} (<strong>{scheme.title}</strong>).
              </p>

              {/* Application Reference Banner */}
              <div className="app-ref-card" data-testid="apply-confirmation-ref-card">
                <span className="ref-title">{t("apply.referenceNumber")}</span>
                <div className="ref-number-row">
                  <span className="ref-code" data-testid="apply-confirmation-app-number">{application.application_number}</span>
                  <button type="button" className="btn-copy" data-testid="apply-copy-app-number-btn" onClick={handleCopyAppNo}>
                    {copiedAppNo ? t("apply.copied") : t("apply.copy")}
                  </button>
                </div>
                <p className="ref-note">
                  {t("apply.preserveNote")}
                </p>
              </div>

              {/* Application Details Summary */}
              <div className="confirmation-summary-box">
                <div className="sum-item">
                  <strong>Scheme:</strong>
                  <span>{scheme.title} ({scheme.category})</span>
                </div>
                <div className="sum-item">
                  <strong>Applicant:</strong>
                  <span>{formData.full_name || citizen.full_name || "Registered Citizen"}</span>
                </div>
                <div className="sum-item">
                  <strong>{t("apply.submissionDate")}</strong>
                  <span>{new Date().toLocaleDateString(language === "hi" ? "hi-IN" : language === "kn" ? "kn-IN" : "en-IN", { day: "numeric", month: "long", year: "numeric" })}</span>
                </div>
                <div className="sum-item">
                  <strong>{t("apply.applicationStatus")}</strong>
                  <span className="status-pill status-submitted">{t(`status.${application.status}`, application.status)}</span>
                </div>
                <div className="sum-item">
                  <strong>{t("apply.documentsUploaded")}</strong>
                  <span>{documents.length} / {docList.length}</span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="confirmation-actions">
                <button
                  type="button"
                  className="btn-download-pdf"
                  data-testid="apply-confirmation-download-pdf-btn"
                  onClick={handleDownloadPdf}
                  disabled={downloadingPdf}
                >
                  {downloadingPdf ? t("common.loading") : t("apply.downloadPdfButton")}
                </button>

                <button
                  type="button"
                  className="btn-view-app"
                  data-testid="apply-confirmation-track-btn"
                  onClick={() => navigate(`/my-applications/${application.application_number}`)}
                >
                  {t("apply.trackStatusButton")}
                </button>

                <button
                  type="button"
                  className="btn-back-services"
                  data-testid="apply-confirmation-return-btn"
                  onClick={() => navigate("/my-services")}
                >
                  {t("apply.returnMyServices")}
                </button>
              </div>

              <div className="mock-disclosure-footer">
                <small>
                  ℹ {t("apply.demoDisclosure")}
                </small>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}

export default ApplyScheme;
