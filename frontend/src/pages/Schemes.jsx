import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { useTranslation } from "../i18n";
import { getSchemes } from "../api";
import "./Schemes.css";

function Schemes() {
  const { t, getLocalizedScheme } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();

  const categoryParam = searchParams.get("category") || "All";
  const queryParam = searchParams.get("q") || "";

  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchInput, setSearchInput] = useState(queryParam);

  useEffect(() => {
    setSearchInput(queryParam);
  }, [queryParam]);

  useEffect(() => {
    getSchemes()
      .then((data) => {
        setSchemes(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load schemes from the server.");
        setLoading(false);
      });
  }, []);

  const localized = useMemo(
    () => schemes.map((scheme) => getLocalizedScheme(scheme)),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [schemes]
  );

  const categories = useMemo(
    () => Array.from(new Set(localized.map((scheme) => scheme.category).filter(Boolean))),
    [localized]
  );

  const filtered = useMemo(() => {
    const q = queryParam.trim().toLowerCase();
    return localized.filter((scheme) => {
      const matchesCategory =
        categoryParam === "All" || scheme.category === categoryParam;
      const matchesQuery =
        !q ||
        scheme.title?.toLowerCase().includes(q) ||
        scheme.short_description?.toLowerCase().includes(q) ||
        scheme.description?.toLowerCase().includes(q);
      return matchesCategory && matchesQuery;
    });
  }, [localized, categoryParam, queryParam]);

  const selectCategory = (category) => {
    const next = new URLSearchParams(searchParams);
    if (category === "All") {
      next.delete("category");
    } else {
      next.set("category", category);
    }
    setSearchParams(next, { replace: true });
  };

  const handleSearch = (event) => {
    event.preventDefault();
    const next = new URLSearchParams(searchParams);
    const q = searchInput.trim();
    if (q) {
      next.set("q", q);
    } else {
      next.delete("q");
    }
    setSearchParams(next, { replace: true });
  };

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
          <p>{t("schemes.subtitle")}</p>
        </div>

        {/* ── Toolbar: search + category tabs ── */}
        <div className="schemes-toolbar">
          <form className="schemes-search" onSubmit={handleSearch} role="search">
            <label className="sr-only" htmlFor="schemes-search-input">
              {t("schemes.searchPlaceholder")}
            </label>
            <input
              id="schemes-search-input"
              type="search"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              placeholder={t("schemes.searchPlaceholder")}
              autoComplete="off"
            />
            <button type="submit">{t("home.searchButton")}</button>
          </form>

          <div className="filter-tabs" role="tablist" aria-label={t("schemes.allCategories")}>
            <button
              type="button"
              role="tab"
              aria-selected={categoryParam === "All"}
              className={categoryParam === "All" ? "filter-tab active" : "filter-tab"}
              onClick={() => selectCategory("All")}
            >
              {t("schemes.allCategories")}
            </button>

            {categories.map((category) => (
              <button
                key={category}
                type="button"
                role="tab"
                aria-selected={categoryParam === category}
                className={categoryParam === category ? "filter-tab active" : "filter-tab"}
                onClick={() => selectCategory(category)}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        <p className="results-count" aria-live="polite">
          {filtered.length} {t("schemes.schemesFound")}
        </p>

        {filtered.length === 0 ? (
          <p className="empty-message">{t("schemes.noResults")}</p>
        ) : (
          <div className="scheme-grid">
            {filtered.map((scheme) => (
              <article className="scheme-card" key={scheme.id} data-testid="scheme-card">

                <span className="scheme-category">{scheme.category}</span>

                <h3 className="scheme-card-title">{scheme.title}</h3>

                <p>{scheme.short_description}</p>

                <ul className="scheme-card-meta">
                  <li>{scheme.eligibility?.length || 0} {t("schemes.eligibilityPoints")}</li>
                  <li>{scheme.documents?.length || 0} {t("schemes.documentsLabel")}</li>
                </ul>

                <div className="scheme-card-actions">
                  <Link
                    to={`/schemes/${scheme.id}`}
                    className="text-link"
                    data-testid={`scheme-view-details-${scheme.id}`}
                  >
                    {t("home.viewDetails")}
                  </Link>
                  <Link to={`/apply/${scheme.id}`} className="scheme-button">
                    {t("home.applyNow")}
                  </Link>
                </div>

              </article>
            ))}
          </div>
        )}

      </div>
    </section>
  );
}

export default Schemes;
