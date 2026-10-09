import { useState } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { useTranslation } from "../i18n";
import { getCitizen, logoutCitizen } from "../api";
import Emblem from "./Emblem";
import "./Header.css";

function Header() {
  const { language, setLanguage, t } = useTranslation();
  const navigate = useNavigate();

  const citizen = getCitizen();
  const [search, setSearch] = useState("");

  const handleLogout = () => {
    logoutCitizen();
    navigate("/");
  };

  const handleSearch = (event) => {
    event.preventDefault();
    const query = search.trim();
    navigate(query ? `/schemes?q=${encodeURIComponent(query)}` : "/schemes");
  };

  const tabClass = ({ isActive }) => (isActive ? "nav-link active" : "nav-link");

  return (
    <header className="site-header">

      {/* ── Demonstration Notice ── */}
      <div className="demo-disclaimer-bar" role="note" aria-label="Demonstration notice">
        <span>
          <strong>YOJANASAATHI</strong> — Demonstration portal for scheme information.
          This is not an official government website.
        </span>
      </div>

      {/* ── Government Utility Bar ── */}
      <div className="gov-topbar">
        <div className="container gov-topbar-inner">
          <span className="topbar-left">
            <span className="topbar-lang">भारत</span>
            <span className="topbar-divider" aria-hidden="true">|</span>
            <span>{t("header.govPortal")}</span>
          </span>

          <div className="topbar-right">
            <a href="#main-content" className="skip-link">
              {t("header.skipToContent")}
            </a>

            <div className="font-size-control" role="group" aria-label={t("header.textSize")}>
              <button type="button" aria-label="Decrease text size" onClick={() => { document.documentElement.style.fontSize = "14px"; }}>A-</button>
              <button type="button" aria-label="Default text size" onClick={() => { document.documentElement.style.fontSize = "15px"; }}>A</button>
              <button type="button" aria-label="Increase text size" onClick={() => { document.documentElement.style.fontSize = "17px"; }}>A+</button>
            </div>

            <span className="topbar-divider" aria-hidden="true">|</span>

            <label className="language-inline">
              <span className="sr-only">{t("header.language")}</span>
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
            </label>
          </div>
        </div>
      </div>

      {/* ── Branding & Search ── */}
      <div className="branding">
        <div className="container branding-inner">

          <Link to="/" className="brand" aria-label="YojanaSaathi Home">
            <Emblem size={58} />
            <div className="brand-text">
              <div className="brand-title">{t("header.brandTitle")}</div>
              <div className="brand-subtitle">{t("header.brandSubtitle")}</div>
            </div>
          </Link>

          <div className="header-actions">

            <form className="header-search" onSubmit={handleSearch} role="search">
              <label className="sr-only" htmlFor="header-search-input">
                {t("home.searchButton")}
              </label>
              <input
                id="header-search-input"
                type="search"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder={t("header.searchPlaceholder")}
                autoComplete="off"
              />
              <button type="submit" aria-label={t("home.searchButton")}>
                {t("home.searchButton")}
              </button>
            </form>

            {citizen ? (
              <div className="citizen-header-controls">
                <Link
                  to="/my-services"
                  className="citizen-dash-link"
                  data-testid="citizen-dashboard-link"
                >
                  {citizen.full_name || t("nav.myServices")}
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
                {t("nav.citizenAccess")}
              </Link>
            )}

          </div>

        </div>
      </div>

      {/* ── Main Tab Navigation ── */}
      <nav className="main-nav" aria-label="Main navigation">
        <div className="container nav-inner">

          <NavLink to="/" end className={tabClass} data-testid="nav-home">
            {t("nav.home")}
          </NavLink>

          <div className="nav-item has-dropdown">
            <NavLink to="/schemes" className={tabClass} data-testid="nav-schemes">
              {t("nav.schemes")}
              <span className="caret" aria-hidden="true">▾</span>
            </NavLink>

            <div className="nav-dropdown" role="menu" aria-label={t("nav.schemes")}>
              <Link to="/schemes" role="menuitem">{t("schemes.allCategories")}</Link>
              <Link to="/schemes?category=Health" role="menuitem">{t("schemes.categoryHealth")}</Link>
              <Link to="/schemes?category=Pension" role="menuitem">{t("schemes.categoryPension")}</Link>
            </div>
          </div>

          <NavLink to="/documents" className={tabClass} data-testid="nav-documents">
            {t("nav.documents")}
          </NavLink>

          <div className="nav-item has-dropdown">
            <NavLink to="/services" className={tabClass} data-testid="nav-services">
              {t("nav.services")}
              <span className="caret" aria-hidden="true">▾</span>
            </NavLink>

            <div className="nav-dropdown" role="menu" aria-label={t("nav.services")}>
              <Link to="/services" role="menuitem">{t("services.title")}</Link>
              <Link to="/citizen-services/scheme-finder" role="menuitem">{t("services.schemeFinderTitle")}</Link>
              <Link to="/citizen-services/documents" role="menuitem">{t("services.docChecklistTitle")}</Link>
            </div>
          </div>

          <NavLink to="/my-services" className={tabClass} data-testid="nav-applications">
            {t("nav.applications")}
          </NavLink>

          <NavLink to="/my-applications" className={tabClass} data-testid="nav-track-application">
            {t("nav.trackApplication")}
          </NavLink>

          <NavLink to="/help" className={tabClass} data-testid="nav-help">
            {t("nav.help")}
          </NavLink>

          <NavLink to="/disclaimer" className={tabClass} data-testid="nav-about">
            {t("nav.about")}
          </NavLink>

        </div>
      </nav>
    </header>
  );
}

export default Header;
