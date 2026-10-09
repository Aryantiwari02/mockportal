import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { documents } from "../data/documents";
import { useTranslation } from "../i18n";
import "./Search.css";

import { getSchemes } from "../api";

function Search() {
  const { t, getLocalizedScheme } = useTranslation();
  const [schemes, setSchemes] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const services = [
    {
      id: "scheme-finder",
      title: t("services.schemeFinderTitle"),
      description: t("services.schemeFinderDesc"),
      path: "/citizen-services/scheme-finder",
      type: "service",
    },
    {
      id: "document-checklist",
      title: t("services.docChecklistTitle"),
      description: t("services.docChecklistDesc"),
      path: "/citizen-services/documents",
      type: "service",
    },
  ];

  useEffect(() => {
    getSchemes()
      .then((data) => {
        setSchemes(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load search data from the server.");
        setLoading(false);
      })
  }, []);

  const query = searchTerm.trim().toLowerCase();

  const localizedSchemes = schemes.map(getLocalizedScheme);

  const schemeResults = localizedSchemes.filter((scheme) => {
    if (!query) return false;

    const searchableText = [
      scheme.title,
      scheme.category,
      scheme.short_description,
      scheme.description,
      ...(scheme.eligibility || []),
      ...(scheme.benefits || []),
      ...(scheme.documents || []),
      ...(scheme.application_process || []),
    ]
      .join(" ")
      .toLowerCase();

    return searchableText.includes(query);
  });

  const documentResults = documents.filter((document) => {
    if (!query) return false;

    const searchableText = [
      document.title,
      document.category,
      document.shortDescription,
      ...(document.examples || []),
    ]
      .join(" ")
      .toLowerCase();

    return searchableText.includes(query);
  });

  const serviceResults = services.filter((service) => {
    if (!query) return false;

    const searchableText = [
      service.title,
      service.description,
    ]
      .join(" ")
      .toLowerCase();

    return searchableText.includes(query);
  });

  const totalResults =
    schemeResults.length +
    documentResults.length +
    serviceResults.length;

  return (
    <section className="page-section">
      <div className="container">

        <div className="page-heading">
          <span className="section-label">
            {t("search.title")}
          </span>

          <h1>{t("search.title")}</h1>

          <p>
            {t("search.subtitle")}
          </p>
        </div>

        <div className="search-box-wrapper">

          <input
            type="text"
            value={searchTerm}
            onChange={(event) =>
              setSearchTerm(event.target.value)
            }
            placeholder={t("search.placeholder")}
            className="search-input"
          />

        </div>

        {loading && (
          <div className="search-message">
            {t("common.loading")}
          </div>
        )}

        {error && (
          <div className="search-message error-message">
            {error}
          </div>
        )}

        {!loading && !error && query === "" && (
          <div className="search-message">
            {t("search.placeholder")}
          </div>
        )}

        {!loading &&
          !error &&
          query !== "" &&
          totalResults === 0 && (
            <div className="search-message">
              <h2>{t("search.noResults")}</h2>
            </div>
          )}

        {!loading &&
          !error &&
          query !== "" &&
          totalResults > 0 && (
            <div className="search-results">

              <p className="result-count">
                {totalResults} {t("search.resultsFound")}
              </p>

              {schemeResults.length > 0 && (
                <section className="search-result-section">

                  <h2>{t("nav.schemes")}</h2>

                  <div className="search-result-grid">

                    {schemeResults.map((scheme) => (
                      <article
                        className="search-result-card"
                        key={scheme.id}
                      >

                        <span className="scheme-category">
                          {scheme.category}
                        </span>

                        <h3>{scheme.title}</h3>

                        <p>
                          {scheme.short_description}
                        </p>

                        <Link
                          to={`/schemes/${scheme.id}`}
                          className="search-result-link"
                        >
                          {t("home.viewDetails")}
                        </Link>

                      </article>
                    ))}

                  </div>

                </section>
              )}

              {documentResults.length > 0 && (
                <section className="search-result-section">

                  <h2>{t("nav.documents")}</h2>

                  <div className="search-result-grid">

                    {documentResults.map((document) => (
                      <article
                        className="search-result-card"
                        key={document.id}
                      >

                        <span className="scheme-category">
                          {document.category}
                        </span>

                        <h3>{document.title}</h3>

                        <p>
                          {document.shortDescription}
                        </p>

                        <Link
                          to={`/documents/${document.id}`}
                          className="search-result-link"
                        >
                          {t("documents.viewDetails")} →
                        </Link>

                      </article>
                    ))}

                  </div>

                </section>
              )}

              {serviceResults.length > 0 && (
                <section className="search-result-section">

                  <h2>{t("nav.services")}</h2>

                  <div className="search-result-grid">

                    {serviceResults.map((service) => (
                      <article
                        className="search-result-card"
                        key={service.id}
                      >

                        <h3>{service.title}</h3>

                        <p>
                          {service.description}
                        </p>

                        <Link
                          to={service.path}
                          className="search-result-link"
                        >
                          {t("home.viewDetails")}
                        </Link>

                      </article>
                    ))}

                  </div>

                </section>
              )}

            </div>
          )}

      </div>
    </section>
  );
}

export default Search;