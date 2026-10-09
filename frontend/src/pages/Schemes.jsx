import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "../i18n";
import "./Schemes.css";
import { getSchemes } from "../api";

function Schemes() {
  const { t, getLocalizedScheme } = useTranslation();
  const [schemes, setSchemes] = useState([]);
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

  if (loading) {
    return (
      <section className="page-section">
        <div className="container">
          <div className="page-heading">
            <span className="section-label">{t("nav.schemes")}</span>
            <h1>{t("schemes.title")}</h1>
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
            <span className="section-label">{t("nav.schemes")}</span>
            <h1>{t("schemes.title")}</h1>
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
          <span className="section-label">{t("nav.schemes")}</span>
          <h1>{t("schemes.title")}</h1>
          <p>
            {t("schemes.subtitle")}
          </p>
        </div>

        <div className="scheme-grid">
          {schemes.map((scheme) => {
            const loc = getLocalizedScheme(scheme);
            return (
              <article className="scheme-card" key={loc.id} data-testid="scheme-card">

                <span className="scheme-category">
                  {loc.category}
                </span>

                <h2>{loc.title}</h2>

                <p>{loc.short_description}</p>

                <Link
                  to={`/schemes/${loc.id}`}
                  className="scheme-button"
                  data-testid={`scheme-view-details-${loc.id}`}
                >
                  {t("home.viewDetails")}
                </Link>

              </article>
            );
          })}
        </div>

      </div>
    </section>
  );
}

export default Schemes;