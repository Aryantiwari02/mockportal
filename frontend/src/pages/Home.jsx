import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "../i18n";
import { getSchemes } from "../api";
import "./Home.css";

const HOW_TO_APPLY = [
  { title: "Check Eligibility", desc: "Review the eligibility criteria listed for the scheme." },
  { title: "Prepare Documents", desc: "Keep identity, residence, income and scheme-specific proofs ready." },
  { title: "Fill the Application", desc: "Complete the scheme-specific online application form." },
  { title: "Submit & Track", desc: "Submit the form, save the reference number and track the status." },
];

function Home() {
  const { t, getLocalizedScheme } = useTranslation();
  const navigate = useNavigate();

  const [query, setQuery] = useState("");
  const [schemes, setSchemes] = useState([]);
  const [loadingSchemes, setLoadingSchemes] = useState(true);
  const [activeCategory, setActiveCategory] = useState("All");

  useEffect(() => {
    getSchemes()
      .then((data) => setSchemes(Array.isArray(data) ? data : []))
      .catch((err) => {
        console.error(err);
        setSchemes([]);
      })
      .finally(() => setLoadingSchemes(false));
  }, []);

  const handleSearch = (event) => {
    event.preventDefault();
    const q = query.trim();
    navigate(q ? `/schemes?q=${encodeURIComponent(q)}` : "/schemes");
  };

  const localized = schemes.map((scheme) => getLocalizedScheme(scheme));
  const categories = Array.from(
    new Set(localized.map((scheme) => scheme.category).filter(Boolean))
  );
  const visibleSchemes =
    activeCategory === "All"
      ? localized
      : localized.filter((scheme) => scheme.category === activeCategory);

  return (
    <div className="home-page">

      {/* ── Hero ── */}
      <section className="home-hero" aria-labelledby="hero-heading">
        <div className="container home-hero-inner">

          <div className="home-hero-text">
            <span className="hero-label">{t("home.heroTag")}</span>

            <h1 id="hero-heading">{t("home.heroTitle")}</h1>

            <p>{t("home.heroSubtitle")}</p>

            <form className="hero-search" onSubmit={handleSearch} role="search">
              <label className="sr-only" htmlFor="hero-search-input">
                {t("home.searchButton")}
              </label>
              <input
                id="hero-search-input"
                type="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={t("home.searchPlaceholder")}
                autoComplete="off"
              />
              <button type="submit">{t("home.searchButton")}</button>
            </form>

            <div className="hero-links">
              <Link to="/schemes">{t("home.viewAllSchemes")}</Link>
              <Link to="/citizen-services/scheme-finder">{t("services.schemeFinderTitle")}</Link>
              <Link to="/documents">{t("nav.documents")}</Link>
            </div>
          </div>

          <aside className="home-hero-aside" aria-label="How to apply">
            <h2>{t("home.howToApply")}</h2>
            <ol className="how-steps">
              {HOW_TO_APPLY.map((step, index) => (
                <li key={step.title}>
                  <span className="how-step-num">{index + 1}</span>
                  <span>
                    <strong>{step.title}</strong>
                    <em>{step.desc}</em>
                  </span>
                </li>
              ))}
            </ol>
          </aside>

        </div>
      </section>

      {/* ── Citizen Services ── */}
      <section className="section" aria-labelledby="services-heading">
        <div className="container">

          <div className="section-heading">
            <span className="section-label">{t("home.quickAccess")}</span>
            <h2 id="services-heading">{t("nav.services")}</h2>
            <p>{t("services.subtitle")}</p>
          </div>

          <div className="service-grid">

            <Link
              to="/schemes"
              className="service-card"
              data-testid="home-service-schemes"
            >
              <span className="service-card-index">01</span>
              <h3>{t("schemes.title")}</h3>
              <p>{t("schemes.subtitle")}</p>
            </Link>

            <Link
              to="/citizen-services/scheme-finder"
              className="service-card"
              data-testid="home-service-finder"
            >
              <span className="service-card-index">02</span>
              <h3>{t("services.schemeFinderTitle")}</h3>
              <p>{t("services.schemeFinderDesc")}</p>
            </Link>

            <Link
              to="/documents"
              className="service-card"
              data-testid="home-service-documents"
            >
              <span className="service-card-index">03</span>
              <h3>{t("documents.title")}</h3>
              <p>{t("documents.subtitle")}</p>
            </Link>

            <Link
              to="/help"
              className="service-card"
              data-testid="home-service-help"
            >
              <span className="service-card-index">04</span>
              <h3>{t("help.title")}</h3>
              <p>{t("help.subtitle")}</p>
            </Link>

          </div>

        </div>
      </section>

      {/* ── Browse Schemes ── */}
      <section className="section section-alternate" aria-labelledby="browse-heading">
        <div className="container">

          <div className="section-heading">
            <span className="section-label">{t("home.categoriesTitle")}</span>
            <h2 id="browse-heading">{t("home.featuredTitle")}</h2>
            <p>{t("home.featuredSubtitle")}</p>
          </div>

          <div className="filter-tabs" role="tablist" aria-label={t("home.categoriesTitle")}>
            <button
              type="button"
              role="tab"
              aria-selected={activeCategory === "All"}
              className={activeCategory === "All" ? "filter-tab active" : "filter-tab"}
              onClick={() => setActiveCategory("All")}
            >
              {t("schemes.allCategories")}
            </button>

            {categories.map((category) => (
              <button
                key={category}
                type="button"
                role="tab"
                aria-selected={activeCategory === category}
                className={activeCategory === category ? "filter-tab active" : "filter-tab"}
                onClick={() => setActiveCategory(category)}
              >
                {category}
              </button>
            ))}
          </div>

          {loadingSchemes ? (
            <p className="home-loading">{t("common.loading")}</p>
          ) : visibleSchemes.length === 0 ? (
            <p className="home-loading">{t("schemes.noResults")}</p>
          ) : (
            <div className="scheme-grid">
              {visibleSchemes.map((scheme) => (
                <article className="scheme-card" key={scheme.id}>

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

          <div className="browse-footer">
            <Link to="/schemes" className="secondary-button">
              {t("home.viewAllSchemes")}
            </Link>
          </div>

        </div>
      </section>

      {/* ── Notice ── */}
      <section className="section" aria-label="Portal notice">
        <div className="container">
          <div className="information-box">
            <div>
              <span className="section-label">{t("home.infoBoxLabel")}</span>
              <h2>{t("home.infoBoxTitle")}</h2>
            </div>
            <div className="information-list">
              <p>{t("home.infoBoxDesc")}</p>
              <p className="info-disclaimer">{t("footer.disclaimerText")}</p>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
}

export default Home;
