import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "../i18n";
import "./DocumentChecklist.css";
import { getSchemes } from "../api";

const documentMap = {
  "Identity Proof": "identity-proof",
  "Residence Proof": "residence-certificate",
  "Residence Certificate": "residence-certificate",
  "Income Certificate": "income-certificate",
  "Bank Account Details": "bank-proof",
  "Bank Account Proof": "bank-proof",
  "Bank Proof": "bank-proof",
  "Age Proof": "other-documents",
  "Family Details": "other-documents",
  "Medical Documents, where applicable": "other-documents",
  "Age Proof, where applicable": "other-documents",
};

function DocumentChecklist() {
  const { t, getLocalizedScheme } = useTranslation();
  const [schemes, setSchemes] = useState([]);
  const [selectedScheme, setSelectedScheme] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getSchemes()
      .then((data) => {
        setSchemes(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load schemes from the server.");
        setLoading(false);
      });
  }, []);

  const rawScheme = schemes.find(
    (item) => item.id === selectedScheme
  );
  const scheme = getLocalizedScheme(rawScheme);

  if (loading) {
    return (
      <section className="page-section">
        <div className="container">
          <div className="page-heading">
            <span className="section-label">{t("nav.services")}</span>
            <h1>{t("services.docChecklistTitle")}</h1>
            <p>{t("common.loading")}</p>
          </div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="page-section">
        <div className="container">
          <div className="page-heading">
            <span className="section-label">{t("nav.services")}</span>
            <h1>{t("services.docChecklistTitle")}</h1>
            <p className="error-message">{error}</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="page-section">
      <div className="container">

        <div className="page-heading">
          <span className="section-label">{t("nav.services")}</span>
          <h1>{t("services.docChecklistTitle")}</h1>
          <p>{t("services.docChecklistDesc")}</p>
        </div>

        <div className="checklist-selector">
          <label htmlFor="scheme">
            Select Scheme
          </label>

          <select
            id="scheme"
            value={selectedScheme}
            onChange={(event) =>
              setSelectedScheme(event.target.value)
            }
          >
            <option value="">
              -- Select a scheme --
            </option>

            {schemes.map((item) => {
              const loc = getLocalizedScheme(item);
              return (
                <option
                  key={loc.id}
                  value={loc.id}
                >
                  {loc.title}
                </option>
              );
            })}
          </select>
        </div>

        {scheme && (
          <div className="checklist-result">
            <div className="checklist-header">
              <span className="scheme-category">
                {scheme.category}
              </span>

              <h2>{scheme.title}</h2>
              <p>{scheme.short_description}</p>
            </div>

            <div className="document-list">
              {scheme.documents && scheme.documents.map((documentName, index) => {
                const canonicalDocName = rawScheme?.documents?.[index] || documentName;
                const documentId = documentMap[canonicalDocName];

                return (
                  <div
                    className="document-item"
                    key={`${documentName}-${index}`}
                  >
                    <div className="document-number">
                      {index + 1}
                    </div>

                    <div className="document-info">
                      <h3>{documentName}</h3>

                      {documentId ? (
                        <Link
                          to={`/documents/${documentId}`}
                          className="document-link"
                        >
                          {t("documents.viewDetails")} →
                        </Link>
                      ) : (
                        <span className="document-note">
                          {t("apply.requiredDoc")}
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="checklist-note">
              <strong>{t("footer.importantTitle")}</strong>
              <p>{t("footer.disclaimerText")}</p>
            </div>
          </div>
        )}

      </div>
    </section>
  );
}

export default DocumentChecklist;