import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "../i18n";
import { getCitizen, logoutCitizen } from "../api";
import "./Header.css";

function Header() {
  const { language, setLanguage, t } = useTranslation();
  const navigate = useNavigate();
  const citizen = getCitizen();

  const handleLogout = () => {
    logoutCitizen();
    navigate("/");
  };

  return (
    <header>

      {/* ── Demo Portal Disclaimer ── */}
      <div className="demo-disclaimer-bar" role="banner" aria-label="Demo notice">
        <span>
          ⚠ <strong>YOJANASAATHI DEMO PORTAL</strong> — This is an educational
          demonstration project, not an official government website.
        </span>
      </div>

      {/* ── Government Utility Bar ── */}
      <div className="gov-topbar">
        <div className="container gov-topbar-inner">
          <span>{t("header.govPortal")}</span>

          <div className="topbar-right">
            <a href="#main-content" className="skip-link">
              {t("header.skipToContent")}
            </a>
            <button type="button" aria-label="Decrease text size">A-</button>
            <button type="button" aria-label="Default text size">A</button>
            <button type="button" aria-label="Increase text size">A+</button>
          </div>
        </div>
      </div>

      {/* ── Branding ── */}
      <div className="branding">
        <div className="container branding-inner">

          <Link to="/" className="brand" aria-label="YojanaSaathi Home">
            <div className="emblem-placeholder" aria-hidden="true">
              🇮🇳
            </div>

            <div>
              <div className="brand-title">
                {t("header.brandTitle")}
              </div>

              <div className="brand-subtitle">
                {t("header.brandSubtitle")}
              </div>
            </div>
          </Link>

          <div className="header-actions">

            <div className="language-control">
              <label htmlFor="language-select">
                {t("header.language")}
              </label>

              <select
                id="language-select"
                data-testid="language-selector"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                aria-label={t("header.language")}
              >
                <option value="en">English</option>
                <option value="kn">ಕನ್ನಡ</option>
                <option value="hi">हिन्दी</option>
              </select>
            </div>

            {citizen ? (
              <div className="citizen-header-controls">
                <Link
                  to="/my-services"
                  className="citizen-dash-link"
                  data-testid="citizen-dashboard-link"
                >
                  👤 {citizen.full_name || t("nav.myServices")}
                </Link>
                <button
                  type="button"
                  className="btn-logout-header"
                  data-testid="header-sign-out-button"
                  onClick={handleLogout}
                >
                  {t("myServices.signOut")}
                </button>
              </div>
            ) : (
              <Link
                to="/citizen-access"
                className="citizen-access-link"
                data-testid="citizen-access-link"
              >
                🔐 {t("nav.citizenAccess")}
              </Link>
            )}

          </div>

        </div>
      </div>

      {/* ── Main Navigation ── */}
      <nav className="main-nav" aria-label="Main navigation">
        <div className="container nav-inner">

          <Link to="/" data-testid="nav-home">{t("nav.home")}</Link>

          <Link to="/schemes" data-testid="nav-schemes">
            {t("nav.schemes")}
          </Link>

          <Link to="/documents" data-testid="nav-documents">
            {t("nav.documents")}
          </Link>

          <Link to="/services" data-testid="nav-services">
            {t("nav.services")}
          </Link>

          <Link to="/my-services" data-testid="nav-applications">
            {t("nav.applications")}
          </Link>

          <Link to="/my-applications" data-testid="nav-track-application">
            {t("nav.trackApplication")}
          </Link>

          <Link to="/help" data-testid="nav-help">
            {t("nav.help")}
          </Link>

          <Link to="/disclaimer" data-testid="nav-about">
            {t("nav.about")}
          </Link>

        </div>
      </nav>
    </header>
  );
}

export default Header;