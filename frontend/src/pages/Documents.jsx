import { useState } from "react";
import { useTranslation } from "../i18n";
import "./Documents.css";

const DOCUMENT_TYPES = [
  {
    id: "identity",
    icon: "🪪",
    category: "Identity",
    examples: ["Aadhaar Card", "Voter ID Card", "PAN Card", "Passport", "Driving Licence"],
    acceptedBy: "Most welfare, health, pension schemes",
    issuedBy: "UIDAI / Election Commission / Income Tax Dept / MEA / RTO",
  },
  {
    id: "income",
    icon: "💰",
    category: "Income",
    examples: ["Income Certificate", "BPL Card", "Ration Card", "Salary Slip / Form 16"],
    acceptedBy: "Means-tested subsidy and pension schemes",
    issuedBy: "Tehsildar / Revenue Dept / FPS / Employer",
  },
  {
    id: "residence",
    icon: "🏠",
    category: "Residence",
    examples: ["Domicile Certificate", "Utility Bill (Electricity / Water)", "Rent Agreement", "Bank Passbook (address page)"],
    acceptedBy: "State-specific and location-restricted schemes",
    issuedBy: "Revenue Dept / DISCOM / Landlord / Bank",
  },
  {
    id: "bank",
    icon: "🏦",
    category: "Bank",
    examples: ["Bank Passbook (first page)", "Cancelled Cheque", "Bank Account Statement"],
    acceptedBy: "DBT / direct benefit transfer schemes",
    issuedBy: "Scheduled Bank",
  },
  {
    id: "caste",
    icon: "📜",
    category: "Caste / Community",
    examples: ["Caste Certificate (SC/ST/OBC)", "Community Certificate", "Non-Creamy Layer Certificate"],
    acceptedBy: "Reserved-category and social welfare schemes",
    issuedBy: "Tehsildar / Revenue Dept",
  },
  {
    id: "disability",
    icon: "♿",
    category: "Disability",
    examples: ["Disability Certificate (UDID)", "Medical Certificate from Govt Hospital"],
    acceptedBy: "Divyangjan welfare schemes",
    issuedBy: "Designated Medical Authority / UDID Portal",
  },
  {
    id: "age",
    icon: "📅",
    category: "Age / Birth Proof",
    examples: ["Birth Certificate", "School Leaving Certificate / Marksheet", "Aadhaar (age proxy)"],
    acceptedBy: "Senior citizen pension, child welfare schemes",
    issuedBy: "Municipal Authority / School Board / UIDAI",
  },
  {
    id: "photo",
    icon: "📷",
    category: "Photograph",
    examples: ["Recent passport-size photograph (colour, plain background)"],
    acceptedBy: "Nearly all schemes require recent photo",
    issuedBy: "Self / Photo studio",
  },
];

const UPLOAD_TIPS = [
  "Scan or photograph documents in good lighting — text must be clearly readable.",
  "Accepted formats: PDF, JPG, JPEG, PNG. Maximum size: 5 MB per file.",
  "Ensure all four corners of the document are visible in the upload.",
  "Do NOT upload expired documents. Certificates must be issued within validity period.",
  "Self-attested copies may be required — sign and write 'True Copy' on the copy.",
  "Never share your Aadhaar OTP, bank PIN, or passwords with any portal representative.",
];

function Documents() {
  const { t, language } = useTranslation();
  const [activeCategory, setActiveCategory] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");

  const filtered = DOCUMENT_TYPES.filter((doc) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (
      doc.category.toLowerCase().includes(q) ||
      doc.examples.some((ex) => ex.toLowerCase().includes(q)) ||
      doc.issuedBy.toLowerCase().includes(q)
    );
  });

  return (
    <div className="documents-page">

      {/* ── Header ── */}
      <section className="documents-header">
        <div className="container">
          <span className="documents-label">{t("home.quickDocuments")}</span>
          <h1>{t("documents.title")}</h1>
          <p>{t("documents.subtitle")}</p>

          {/* Search */}
          <div className="doc-search-bar">
            <span className="doc-search-icon">🔎</span>
            <input
              type="text"
              id="document-search"
              data-testid="document-search-input"
              placeholder={t("documents.searchPlaceholder")}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              aria-label="Search documents"
            />
            {searchQuery && (
              <button
                type="button"
                className="doc-search-clear"
                onClick={() => setSearchQuery("")}
                aria-label="Clear search"
              >
                ✕
              </button>
            )}
          </div>
        </div>
      </section>

      {/* ── Upload Guidelines ── */}
      <section className="doc-guidelines-section">
        <div className="container">
          <div className="doc-guidelines-card">
            <div className="doc-guideline-header">
              <span className="doc-guideline-icon">📋</span>
              <div>
                <h2>Document Upload Guidelines</h2>
                <p>Follow these rules to ensure your documents are accepted by the system.</p>
              </div>
            </div>
            <div className="doc-tips-grid">
              {UPLOAD_TIPS.map((tip, i) => (
                <div key={i} className="doc-tip-item">
                  <span className="doc-tip-num">{String(i + 1).padStart(2, "0")}</span>
                  <p>{tip}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── Document Types Reference ── */}
      <section className="doc-types-section">
        <div className="container">

          <div className="section-heading" style={{ textAlign: "left", marginBottom: "24px" }}>
            <span className="section-label">REQUIRED DOCUMENT TYPES</span>
            <h2>Documents Commonly Required for Government Schemes</h2>
            <p>
              Click any category to see which documents are accepted, who issues them, and
              which types of schemes require them.
            </p>
          </div>

          {filtered.length === 0 && (
            <div className="doc-no-results">
              <p>No documents matched "<strong>{searchQuery}</strong>".</p>
            </div>
          )}

          <div className="doc-type-grid" data-testid="document-type-grid">
            {filtered.map((doc) => (
              <div
                key={doc.id}
                className={`doc-type-card ${activeCategory === doc.id ? "expanded" : ""}`}
                data-testid={`doc-type-card-${doc.id}`}
              >
                {/* Card Header — always visible */}
                <button
                  type="button"
                  className="doc-type-header"
                  data-testid={`doc-type-toggle-${doc.id}`}
                  onClick={() => setActiveCategory(activeCategory === doc.id ? null : doc.id)}
                  aria-expanded={activeCategory === doc.id}
                >
                  <span className="doc-type-icon">{doc.icon}</span>
                  <span className="doc-type-name">{doc.category}</span>
                  <span className="doc-type-chevron">
                    {activeCategory === doc.id ? "▲" : "▼"}
                  </span>
                </button>

                {/* Expanded Detail */}
                {activeCategory === doc.id && (
                  <div className="doc-type-detail" data-testid={`doc-type-detail-${doc.id}`}>

                    <div className="doc-detail-row">
                      <span className="doc-detail-label">Accepted Documents</span>
                      <ul className="doc-detail-list">
                        {doc.examples.map((ex, i) => (
                          <li key={i}>📄 {ex}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="doc-detail-row">
                      <span className="doc-detail-label">
                        {t("documents.issuingAuthority")}
                      </span>
                      <p className="doc-detail-value">{doc.issuedBy}</p>
                    </div>

                    <div className="doc-detail-row">
                      <span className="doc-detail-label">
                        {t("documents.requiredFor")}
                      </span>
                      <p className="doc-detail-value">{doc.acceptedBy}</p>
                    </div>

                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Checklist Builder ── */}
      <section className="doc-checklist-section">
        <div className="container">
          <div className="doc-checklist-card">

            <div className="doc-checklist-header">
              <span>✅</span>
              <div>
                <h2>Pre-Application Checklist</h2>
                <p>Verify you have these ready before starting any scheme application.</p>
              </div>
            </div>

            <div className="checklist-grid">
              {[
                { label: "Valid photo identity proof (Aadhaar / Voter ID)", note: "Must not be expired. Name must match exactly." },
                { label: "Income / financial eligibility document", note: "Usually valid for 1 year from date of issue." },
                { label: "Proof of residence in the scheme's applicable state/district", note: "Utility bill or domicile certificate." },
                { label: "Recent passport-size colour photograph", note: "Plain background, full face, taken within 3 months." },
                { label: "Bank account details (passbook / cancelled cheque)", note: "Required for DBT — account must be in applicant's name." },
                { label: "Mobile number linked to Aadhaar", note: "Required for OTP-based verification on this portal." },
              ].map((item, i) => (
                <div key={i} className="checklist-item" data-testid={`checklist-item-${i}`}>
                  <div className="checklist-checkbox" aria-hidden="true">☐</div>
                  <div>
                    <strong>{item.label}</strong>
                    <p>{item.note}</p>
                  </div>
                </div>
              ))}
            </div>

          </div>
        </div>
      </section>

      {/* ── Security Notice ── */}
      <section className="doc-security-section">
        <div className="container">
          <div className="doc-security-notice">
            <span className="security-icon">🔒</span>
            <div>
              <strong>Document Privacy &amp; Security</strong>
              <p>
                Documents uploaded through this portal are stored securely in the local
                demonstration database and are accessible only to the verified citizen who
                submitted them. Do not upload real government-issued identity documents to this
                demo environment. This portal is for demonstration purposes only.
              </p>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
}

export default Documents;