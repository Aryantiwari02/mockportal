import { Link } from "react-router-dom";
import { useTranslation } from "../i18n";
import "./CitizenServices.css";

function CitizenServices() {
  const { t } = useTranslation();

  return (
    <div className="citizen-services-page">

      <section className="page-header">
        <div className="container">
          <span className="page-kicker">{t("services.title")}</span>

          <h1>{t("services.title")}</h1>

          <p>
            {t("services.subtitle")}
          </p>
        </div>
      </section>

      <section className="services-section">
        <div className="container">

          <div className="services-grid">

            <div className="service-card">
              <div className="service-icon">🔎</div>

              <h2>{t("services.schemeFinderTitle")}</h2>

              <p>
                {t("services.schemeFinderDesc")}
              </p>

              <Link to="/citizen-services/scheme-finder" className="service-button">
                {t("services.findSchemes")}
              </Link>
            </div>


            <div className="service-card">
              <div className="service-icon">📄</div>

              <h2>{t("services.docChecklistTitle")}</h2>

              <p>
                {t("services.docChecklistDesc")}
              </p>

              <Link to="/citizen-services/documents" className="service-button">
                {t("services.viewChecklist")}
              </Link>
            </div>

          </div>


          <div className="services-notice">

            <strong>{t("footer.importantTitle")}</strong>

            <p>
              {t("footer.disclaimerText")}
            </p>

          </div>

        </div>
      </section>

    </div>
  );
}

export default CitizenServices;