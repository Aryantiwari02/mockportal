import { Link } from "react-router-dom";
import { useTranslation } from "../i18n";
import "./Home.css";

function Home() {
  const { t } = useTranslation();

  return (
    <div className="home-page">

      {/* ── Hero ── */}
      <section className="hero" aria-labelledby="hero-heading">
        <div className="container hero-content">

          <div className="hero-text">
            <span className="hero-label">
              {t("home.heroTag")}
            </span>

            <h1 id="hero-heading">
              {t("home.heroTitle")}
            </h1>

            <p>{t("home.heroSubtitle")}</p>

            <div className="hero-actions">
              <Link
                to="/schemes"
                className="primary-button"
                data-testid="hero-view-schemes-button"
              >
                {t("home.viewAllSchemes")}
              </Link>

              <Link
                to="/citizen-access"
                className="secondary-button"
                data-testid="hero-citizen-access-button"
              >
                🔐 {t("nav.citizenAccess")}
              </Link>
            </div>

            {/* Disclaimer in hero */}
            <p className="hero-disclaimer">
              ⓘ This is a demonstration portal. Not an official government website.
            </p>
          </div>

          <div className="hero-panel" aria-label="Quick access links">
            <h3>{t("home.quickAccess")}</h3>

            <Link to="/schemes?category=health">
              🏥 {t("home.quickHealth")}
            </Link>

            <Link to="/schemes?category=pension">
              🧓 {t("home.quickPension")}
            </Link>

            <Link to="/documents">
              📄 {t("home.quickDocuments")}
            </Link>

            <Link to="/citizen-services/scheme-finder">
              🔎 {t("services.schemeFinderTitle")}
            </Link>

            <Link to="/my-services">
              📋 {t("nav.applications")}
            </Link>
          </div>

        </div>
      </section>


      {/* ── Quick Services ── */}
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
              style={{ textDecoration: "none", color: "inherit" }}
              data-testid="home-service-schemes"
            >
              <span className="service-icon">📋</span>
              <h3>{t("schemes.title")}</h3>
              <p>{t("schemes.subtitle")}</p>
            </Link>

            <Link
              to="/citizen-services/scheme-finder"
              className="service-card"
              style={{ textDecoration: "none", color: "inherit" }}
              data-testid="home-service-finder"
            >
              <span className="service-icon">🔎</span>
              <h3>{t("services.schemeFinderTitle")}</h3>
              <p>{t("services.schemeFinderDesc")}</p>
            </Link>

            <Link
              to="/documents"
              className="service-card"
              style={{ textDecoration: "none", color: "inherit" }}
              data-testid="home-service-documents"
            >
              <span className="service-icon">📄</span>
              <h3>{t("documents.title")}</h3>
              <p>{t("documents.subtitle")}</p>
            </Link>

            <Link
              to="/help"
              className="service-card"
              style={{ textDecoration: "none", color: "inherit" }}
              data-testid="home-service-help"
            >
              <span className="service-icon">❓</span>
              <h3>{t("help.title")}</h3>
              <p>{t("help.subtitle")}</p>
            </Link>

          </div>

        </div>
      </section>


      {/* ── Scheme Categories ── */}
      <section className="category-section" aria-labelledby="categories-heading">
        <div className="container">

          <div className="section-heading">
            <span className="section-label" style={{ background: "rgba(255,255,255,.12)", color: "rgba(255,255,255,.85)" }}>
              {t("home.categoriesTitle")}
            </span>
            <h2 id="categories-heading" style={{ color: "white" }}>
              {t("home.featuredTitle")}
            </h2>
            <p style={{ color: "rgba(255,255,255,.7)" }}>
              {t("home.featuredSubtitle")}
            </p>
          </div>

          <div className="category-grid">

            <Link
              to="/schemes?category=health"
              className="category-card"
              style={{ textDecoration: "none" }}
              data-testid="category-health"
            >
              <span>01</span>
              <h3>{t("home.categoryHealth")}</h3>
              <p>{t("home.categoryHealthDesc")}</p>
            </Link>

            <Link
              to="/schemes?category=pension"
              className="category-card"
              style={{ textDecoration: "none" }}
              data-testid="category-pension"
            >
              <span>02</span>
              <h3>{t("home.categoryPension")}</h3>
              <p>{t("home.categoryPensionDesc")}</p>
            </Link>

            <Link
              to="/services"
              className="category-card"
              style={{ textDecoration: "none" }}
              data-testid="category-services"
            >
              <span>03</span>
              <h3>{t("home.categoryServices")}</h3>
              <p>{t("home.categoryServicesDesc")}</p>
            </Link>

          </div>

        </div>
      </section>


      {/* ── Important Information Box ── */}
      <section className="section" aria-label="Portal information">
        <div className="container">
          <div className="information-box">

            <div>
              <span className="section-label">{t("home.infoBoxLabel")}</span>
              <h2>{t("home.infoBoxTitle")}</h2>
            </div>

            <div className="information-list">
              <p>{t("home.infoBoxDesc")}</p>
              <p className="info-disclaimer">
                All scheme data shown in this portal is for demonstration. Verify
                eligibility and benefit amounts directly with the responsible government
                authority before applying.
              </p>
            </div>

          </div>
        </div>
      </section>

    </div>
  );
}

export default Home;