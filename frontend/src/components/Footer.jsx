import { Link } from "react-router-dom";
import { useTranslation } from "../i18n";
import "./Footer.css";

function Footer() {
  const { t } = useTranslation();

  return (
    <footer className="footer">

      {/* ── Demo Disclaimer Banner in Footer ── */}
      <div className="footer-disclaimer-banner">
        <div className="container">
          <strong>📋 YOJANASAATHI DEMO PORTAL</strong> — This is an educational
          demonstration project, not an official government website. All scheme
          information and application records are for demonstration purposes only.
        </div>
      </div>

      <div className="container">

        <div className="footer-grid">

          {/* ABOUT */}
          <div className="footer-column">
            <h3>{t("footer.brandTitle")}</h3>
            <p>{t("footer.aboutText")}</p>
            <p className="footer-notice">{t("footer.demoText")}</p>
          </div>

          {/* QUICK LINKS */}
          <div className="footer-column">
            <h3>{t("footer.quickLinksTitle")}</h3>
            <Link to="/">{t("nav.home")}</Link>
            <Link to="/schemes">{t("nav.schemes")}</Link>
            <Link to="/documents">{t("nav.documents")}</Link>
            <Link to="/services">{t("nav.services")}</Link>
            <Link to="/my-services">{t("nav.applications")}</Link>
            <Link to="/my-applications">{t("nav.trackApplication")}</Link>
          </div>

          {/* HELP & SUPPORT */}
          <div className="footer-column">
            <h3>{t("footer.helpTitle")}</h3>
            <Link to="/help">{t("footer.faq")}</Link>
            <Link to="/accessibility">{t("footer.accessibility")}</Link>
            <Link to="/contact">{t("footer.contact")}</Link>
            <Link to="/privacy">{t("footer.privacy")}</Link>
            <Link to="/disclaimer">{t("footer.disclaimer")}</Link>
          </div>

          {/* IMPORTANT NOTICE */}
          <div className="footer-column">
            <h3>{t("footer.importantTitle")}</h3>
            <p className="footer-notice">{t("footer.disclaimerText")}</p>
            <p className="footer-notice">
              Scheme information may change. Always verify with the responsible
              government authority before applying.
            </p>
          </div>

        </div>

        <div className="footer-bottom">
          <p>{t("footer.copyright")}</p>
        </div>

      </div>
    </footer>
  );
}

export default Footer;