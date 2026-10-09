import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "../i18n";
import "./SchemeFinder.css";

import { getSchemes } from "../api";

function SchemeFinder() {
  const { t, getLocalizedScheme } = useTranslation();
  const [schemes, setSchemes] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [category, setCategory] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    setError("");

    getSchemes({
      q: searchTerm,
      category: category,
    })
      .then((data) => {
        setSchemes(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load schemes from the server.");
        setLoading(false);
      });
  }, [searchTerm, category]);

  if (loading) {
    return (
      <section className="page-section">
        <div className="container">
          <div className="page-heading">
            <span className="section-label">{t("nav.services")}</span>
            <h1>{t("services.schemeFinderTitle")}</h1>
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
            <h1>{t("services.schemeFinderTitle")}</h1>
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
          <span className="section-label">
            {t("nav.services")}
          </span>

          <h1>{t("services.schemeFinderTitle")}</h1>

          <p>
            {t("services.schemeFinderDesc")}
          </p>
        </div>

        <div className="finder-controls">

          <input
            type="text"
            placeholder={t("schemes.searchPlaceholder")}
            value={searchTerm}
            onChange={(event) =>
              setSearchTerm(event.target.value)
            }
          />

          <select
            value={category}
            onChange={(event) =>
              setCategory(event.target.value)
            }
          >
            <option value="All">
              {t("schemes.allCategories")}
            </option>

            <option value="Health">
              {t("schemes.categoryHealth")}
            </option>

            <option value="Pension">
              {t("schemes.categoryPension")}
            </option>
          </select>

        </div>

        {schemes.length === 0 ? (
          <div className="empty-state">
            <h2>{t("schemes.noResults")}</h2>
          </div>
        ) : (
          <div className="scheme-grid">

            {schemes.map((item) => {
              const scheme = getLocalizedScheme(item);
              return (
                <article
                  className="scheme-card"
                  key={scheme.id}
                >

                  <span className="scheme-category">
                    {scheme.category}
                  </span>

                  <h2>{scheme.title}</h2>

                  <p>{scheme.short_description}</p>

                  <Link
                    to={`/schemes/${scheme.id}`}
                    className="scheme-button"
                  >
                    {t("home.viewDetails")}
                  </Link>

                </article>
              );
            })}

          </div>
        )}

      </div>
    </section>
  );
}

export default SchemeFinder;