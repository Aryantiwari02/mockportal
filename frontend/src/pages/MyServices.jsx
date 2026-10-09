import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "../i18n";
import "./MyServices.css";

import {
  getCitizen,
  getMyApplications,
  getNotifications,
  logoutCitizen,
  markAllNotificationsRead,
  markNotificationRead,
} from "../api";

function MyServices() {
  const navigate = useNavigate();
  const citizen = getCitizen();
  const { t, language } = useTranslation();

  const [applications, setApplications] = useState([]);
  const [loadingApps, setLoadingApps] = useState(true);
  const [notifications, setNotifications] = useState([]);
  const [unreadNotesCount, setUnreadNotesCount] = useState(0);
  const [showNotesDrawer, setShowNotesDrawer] = useState(false);

  useEffect(() => {
    if (!citizen) return;

    // Load Applications
    getMyApplications()
      .then((data) => {
        setApplications(data.results || []);
        setLoadingApps(false);
      })
      .catch((err) => {
        console.error("Failed to load applications:", err);
        setLoadingApps(false);
      });

    // Load Notifications
    getNotifications()
      .then((data) => {
        setNotifications(data.results || []);
        setUnreadNotesCount(data.unread_count || 0);
      })
      .catch((err) => {
        console.error("Failed to load notifications:", err);
      });
  }, []);

  const handleLogout = () => {
    logoutCitizen();
    navigate("/");
  };

  const handleMarkAllRead = async () => {
    try {
      await markAllNotificationsRead();
      setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })));
      setUnreadNotesCount(0);
    } catch (err) {
      console.error(err);
    }
  };

  const handleMarkNoteRead = async (noteId) => {
    try {
      await markNotificationRead(noteId);
      setNotifications((prev) =>
        prev.map((n) => (n.id === noteId ? { ...n, is_read: true } : n))
      );
      setUnreadNotesCount((prev) => Math.max(0, prev - 1));
    } catch (err) {
      console.error(err);
    }
  };

  const getNotificationTitle = (note) => {
    const typeKey = (note.type || "").toUpperCase();
    if (typeKey.includes("ALL_DOCUMENTS_VERIFIED")) {
      return t("notifications.ALL_DOCUMENTS_VERIFIED");
    }
    if (typeKey.includes("DOCUMENT_VERIFIED")) {
      return t("notifications.DOCUMENT_VERIFIED");
    }
    if (typeKey.includes("APPLICATION_SUBMITTED")) {
      return t("notifications.APPLICATION_SUBMITTED");
    }
    return note.title;
  };

  const getNotificationMessage = (note) => {
    const typeKey = (note.type || "").toUpperCase();
    if (typeKey.includes("ALL_DOCUMENTS_VERIFIED")) {
      return language === "kn"
        ? `ಅರ್ಜಿ #${note.application_number} ಗಾಗಿ ಎಲ್ಲಾ ಸಲ್ಲಿಸಿದ ದಾಖಲೆಗಳನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಪರಿಶೀಲಿಸಲಾಗಿದೆ.`
        : language === "hi"
        ? `आवेदन #${note.application_number} के लिए सभी जमा किए गए दस्तावेज़ सफलतापूर्वक सत्यापित कर दिए गए हैं।`
        : `All submitted documents for application #${note.application_number} have been successfully verified.`;
    }
    if (typeKey.includes("DOCUMENT_VERIFIED")) {
      return language === "kn"
        ? `ಅರ್ಜಿ #${note.application_number} ಗಾಗಿ ನಿಮ್ಮ ದಾಖಲೆ ಯಶಸ್ವಿಯಾಗಿ ಪರಿಶೀಲಿಸಲಾಗಿದೆ.`
        : language === "hi"
        ? `आवेदन #${note.application_number} के लिए आपका दस्तावेज़ सफलतापूर्वक सत्यापित कर दिया गया है।`
        : `Your document for application #${note.application_number} has been verified.`;
    }
    if (typeKey.includes("APPLICATION_SUBMITTED")) {
      return language === "kn"
        ? `ನಿಮ್ಮ ಅರ್ಜಿ #${note.application_number} ಯಶಸ್ವಿಯಾಗಿ ನೋಂದಾಯಿಸಲ್ಪಟ್ಟಿದೆ.`
        : language === "hi"
        ? `आपका आवेदन #${note.application_number} सफलतापूर्वक पंजीकृत हो गया है।`
        : `Your application #${note.application_number} was successfully submitted.`;
    }
    return note.message;
  };

  if (!citizen) {
    return (
      <section className="page-section">
        <div className="container">
          <div className="empty-state">
            <h2>{t("apply.authGateTitle")}</h2>
            <p>
              {t("apply.authGateDesc")}
            </p>
            <Link to="/citizen-access" className="scheme-button">
              {t("apply.authGateButton")}
            </Link>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="page-section my-services-page">
      <div className="container">

        {/* Header */}
        <div className="my-services-header">
          <div>
            <span className="section-label">{t("header.govPortal")}</span>
            <h1>{t("myServices.title")}</h1>
            <p>
              {t("myServices.subtitle")}
            </p>
          </div>

          <div className="header-actions-group">
            <button
              type="button"
              data-testid="notifications-button"
              className="notification-bell-btn"
              onClick={() => setShowNotesDrawer(!showNotesDrawer)}
            >
              {t("myServices.notifications")}
              {unreadNotesCount > 0 && (
                <span className="bell-badge">{unreadNotesCount}</span>
              )}
            </button>

            <button data-testid="sign-out-button" className="logout-button" onClick={handleLogout}>
              {t("myServices.signOut")}
            </button>
          </div>
        </div>

        {/* Citizen Profile Banner */}
        <div className="citizen-profile-card">
          <div className="profile-icon">👤</div>
          <div className="profile-info-block">
            <h2>{citizen.full_name || "Registered Citizen"}</h2>
            <p>+91 {citizen.mobile}</p>
            <div className="profile-pills">
              <span className="verified-badge">{t("myServices.otpVerified")}</span>
              <span className="profile-sub-badge">{t("myServices.citizenId")} #{citizen.id}</span>
            </div>
          </div>
        </div>

        {/* Notifications Drawer / Box */}
        {showNotesDrawer && (
          <div className="notifications-panel">
            <div className="panel-header">
              <h3>
                {t("myServices.notificationsPanelTitle")}
                {unreadNotesCount > 0 && (
                  <span className="unread-counter">{unreadNotesCount} {t("myServices.newBadge")}</span>
                )}
              </h3>
              {unreadNotesCount > 0 && (
                <button
                  type="button"
                  className="btn-mark-all"
                  onClick={handleMarkAllRead}
                >
                  {t("myServices.markAllRead")}
                </button>
              )}
            </div>

            {notifications.length === 0 ? (
              <p className="no-notes-text">{t("myServices.noNotifications")}</p>
            ) : (
              <div className="notes-list">
                {notifications.map((note) => (
                  <div
                    key={note.id}
                    className={`note-item ${note.is_read ? "read" : "unread"}`}
                    onClick={() => !note.is_read && handleMarkNoteRead(note.id)}
                  >
                    <div className="note-icon">
                      {note.type === "all_documents_verified" ? "🎉" : note.type === "document_verified" ? "✓" : "📋"}
                    </div>
                    <div className="note-content">
                      <div className="note-title-line">
                        <strong>{getNotificationTitle(note)}</strong>
                        <span className="note-time">
                          {new Date(note.created_at).toLocaleDateString(language === "hi" ? "hi-IN" : language === "kn" ? "kn-IN" : "en-IN", {
                            day: "numeric",
                            month: "short",
                            hour: "2-digit",
                            minute: "2-digit",
                          })}
                        </span>
                      </div>
                      <p>{getNotificationMessage(note)}</p>
                      {note.application_number && (
                        <Link
                          to={`/my-applications/${note.application_number}`}
                          className="note-app-link"
                          onClick={(e) => e.stopPropagation()}
                        >
                          {t("myServices.viewAppArrow")}
                        </Link>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Section: My Applications */}
        <div className="applications-section">
          <div className="section-title-row">
            <h2>{t("myServices.mySubmittedApps")} ({applications.length})</h2>
            <Link to="/schemes" className="btn-apply-more">
              {t("myServices.browseApplyMore")}
            </Link>
          </div>

          {loadingApps ? (
            <div className="apps-loading">{t("common.loading")}</div>
          ) : applications.length === 0 ? (
            <div className="empty-apps-card">
              <span className="empty-apps-icon">📋</span>
              <h3>{t("myServices.noAppsTitle")}</h3>
              <p>
                {t("myServices.noAppsDesc")}
              </p>
              <Link to="/schemes" className="btn-primary-inline">
                {t("myServices.exploreSchemesButton")}
              </Link>
            </div>
          ) : (
            <div className="applications-cards-grid">
              {applications.map((app) => {
                const totalReq = app.total_required_documents_count || 0;
                const verifiedCount = app.verified_documents_count || 0;
                const translatedStatus = t(`status.${app.status}`, app.status);

                return (
                  <div key={app.id} className="app-card" data-testid="application-card">
                    <div className="app-card-top">
                      <span className="app-card-cat">{app.scheme_category}</span>
                      <span data-testid="application-status-badge" className={`status-pill-small status-${app.status.toLowerCase()}`}>
                        {translatedStatus}
                      </span>
                    </div>

                    <h3 className="app-card-title">{app.scheme_title}</h3>

                    <div className="app-card-meta">
                      <div>
                        <span className="meta-lbl">{t("myServices.appNoLabel")}</span>
                        <strong className="meta-val monospace">{app.application_number}</strong>
                      </div>
                      <div>
                        <span className="meta-lbl">{t("myServices.submittedDateLabel")}</span>
                        <span className="meta-val">
                          {app.submitted_at
                            ? new Date(app.submitted_at).toLocaleDateString(language === "hi" ? "hi-IN" : language === "kn" ? "kn-IN" : "en-IN", {
                                day: "numeric",
                                month: "short",
                                year: "numeric",
                              })
                            : t("status.DRAFT")}
                        </span>
                      </div>
                    </div>

                    <div className="app-card-doc-stat">
                      <span className="doc-stat-lbl">{t("myServices.docVerificationLabel")}</span>
                      <span className={`doc-stat-val ${app.all_documents_verified ? "all-done" : ""}`}>
                        {app.all_documents_verified ? "✓ " : ""}
                        {verifiedCount} / {totalReq || app.documents_count} {t("myServices.verifiedCountSuffix")}
                      </span>
                    </div>

                    <div className="app-card-bottom">
                      <Link
                        to={`/my-applications/${app.application_number}`}
                        className="btn-view-application"
                        data-testid={`view-application-${app.application_number}`}
                      >
                        {t("myServices.viewAppDetails")}
                      </Link>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Quick Citizen Services Grid */}
        <div className="service-grid-section">
          <h2>{t("myServices.quickUtilitiesTitle")}</h2>
          <div className="service-grid">
            <Link to="/citizen-services/scheme-finder" className="service-card">
              <span className="service-icon">🔎</span>
              <h3>{t("myServices.findSchemesTitle")}</h3>
              <p>{t("myServices.findSchemesDesc")}</p>
            </Link>

            <Link to="/citizen-services/documents" className="service-card">
              <span className="service-icon">📄</span>
              <h3>{t("myServices.docChecklistTitle")}</h3>
              <p>{t("myServices.docChecklistDesc")}</p>
            </Link>
          </div>
        </div>

      </div>
    </section>
  );
}

export default MyServices;