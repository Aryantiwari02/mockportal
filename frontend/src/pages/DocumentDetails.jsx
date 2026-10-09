import { Link, useParams } from "react-router-dom";
import { documents } from "../data/documents";
import { useTranslation } from "../i18n";
import "./DocumentDetails.css";

function DocumentDetails() {
  const { id } = useParams();
  const { t } = useTranslation();

  const document = documents.find(
    (item) => item.id === id
  );

  if (!document) {
    return (
      <div className="container document-not-found">
        <h1>{t("common.error")}</h1>
        <p>The requested document information could not be found.</p>
        <Link to="/documents">
          ← {t("nav.documents")}
        </Link>
      </div>
    );
  }

  return (
    <div className="document-details-page">

      <section className="document-details-header">
        <div className="container">
          <Link
            to="/documents"
            className="back-link"
          >
            ← {t("nav.documents")}
          </Link>

          <span>
            {document.category}
          </span>

          <h1>
            {document.title}
          </h1>

          <p>
            {document.shortDescription}
          </p>
        </div>
      </section>

      <section className="document-details-content">
        <div className="container document-details-layout">
          <main>
            <section className="document-info-card">
              <h2>{document.title}</h2>
              <p>
                {document.shortDescription}
              </p>
            </section>

            <section className="document-info-card">
              <h2>Examples</h2>
              <ul>
                {document.examples.map((example, index) => (
                  <li key={index}>
                    {example}
                  </li>
                ))}
              </ul>
            </section>

            <section className="document-info-card">
              <h2>{t("footer.importantTitle")}</h2>
              <ul>
                <li>Ensure the information is accurate.</li>
                <li>Check whether the document is currently valid.</li>
                <li>Keep a copy for your records.</li>
                <li>Follow the requirements of the specific scheme or service.</li>
              </ul>
            </section>
          </main>

          <aside>
            <div className="document-side-card">
              <span>{t("home.categoriesTitle")}</span>
              <h3>{document.category}</h3>
              <p>
                Requirements can vary depending on the scheme, service and applicable authority.
              </p>
            </div>

            <div className="document-side-warning">
              <strong>{t("footer.importantTitle")}</strong>
              <p>{t("footer.disclaimerText")}</p>
            </div>
          </aside>
        </div>
      </section>

    </div>
  );
}

export default DocumentDetails;