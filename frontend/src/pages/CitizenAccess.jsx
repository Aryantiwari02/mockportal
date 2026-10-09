import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "../i18n";
import "./CitizenAccess.css";

import {
  requestOTP,
  verifyOTP,
  saveCitizenSession,
} from "../api";

function CitizenAccess() {
  const navigate = useNavigate();
  const { t } = useTranslation();

  const [mobile, setMobile] = useState("");
  const [otp, setOtp] = useState("");

  const [step, setStep] = useState("mobile");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  /* =========================
     SEND OTP
  ========================= */

  const handleSendOTP = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");

    const cleanedMobile = mobile.replace(/\D/g, "");

    if (cleanedMobile.length !== 10) {
      setError(t("citizenAccess.invalidMobileError"));
      return;
    }

    setLoading(true);

    try {
      const data = await requestOTP(cleanedMobile);

      setMobile(cleanedMobile);
      setOtp("");
      setStep("otp");

      setSuccess(t("citizenAccess.otpSentSuccess"));

      console.log("OTP request status:", data.status);
    } catch (err) {
      setError(
        err.message ||
        "Unable to send OTP. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  /* =========================
     VERIFY OTP
  ========================= */

  const handleVerifyOTP = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");

    if (otp.length !== 6 || !/^\d{6}$/.test(otp)) {
      setError(t("citizenAccess.invalidOtpError"));
      return;
    }

    setLoading(true);

    try {
      const data = await verifyOTP(mobile, otp);

      /*
       * Save the authenticated citizen
       */
      saveCitizenSession(data);

      setSuccess(t("citizenAccess.mobileVerifiedSuccess"));

      /*
       * Open citizen dashboard
       */
      navigate("/my-services");
    } catch (err) {
      setError(
        err.message ||
        "Incorrect or expired OTP."
      );
    } finally {
      setLoading(false);
    }
  };

  /* =========================
     RESEND OTP
  ========================= */

  const handleResendOTP = async () => {
    setOtp("");
    setError("");
    setSuccess("");

    setLoading(true);

    try {
      const data = await requestOTP(mobile);

      setSuccess(t("citizenAccess.otpSentSuccess"));
      console.log("OTP resend status:", data.status);
    } catch (err) {
      setError(
        err.message ||
        "Unable to resend OTP. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  /* =========================
     CHANGE MOBILE NUMBER
  ========================= */

  const handleChangeNumber = () => {
    setMobile("");
    setOtp("");
    setError("");
    setSuccess("");
    setStep("mobile");
  };

  return (
    <div className="citizen-access-page">

      <div className="citizen-access-card">

        {/* =========================
            HEADER
        ========================= */}

        <div className="citizen-access-header">

          <div className="citizen-access-icon">
            🔐
          </div>

          <h1>{t("citizenAccess.title")}</h1>

          <p>{t("citizenAccess.subtitle")}</p>

        </div>

        {/* =========================
            MOBILE NUMBER STEP
        ========================= */}

        {step === "mobile" && (
          <form
            className="citizen-access-form"
            onSubmit={handleSendOTP}
          >

            <label htmlFor="mobile">
              {t("citizenAccess.mobileLabel")}
            </label>

            <div className="mobile-input-wrapper">

              <span className="country-code">
                +91
              </span>

              <input
                id="mobile"
                data-testid="otp-mobile-input"
                type="tel"
                inputMode="numeric"
                autoComplete="tel"
                maxLength={10}
                placeholder={t("citizenAccess.mobilePlaceholder")}
                value={mobile}
                onChange={(event) => {
                  const value = event.target.value.replace(/\D/g, "");
                  setMobile(value);
                }}
                disabled={loading}
              />

            </div>

            <button
              type="submit"
              data-testid="otp-send-button"
              className="citizen-primary-button"
              disabled={loading}
            >
              {loading
                ? t("citizenAccess.sendingOtp")
                : t("citizenAccess.sendOtp")
              }
            </button>

          </form>
        )}

        {/* =========================
            OTP VERIFICATION STEP
        ========================= */}

        {step === "otp" && (
          <form
            className="citizen-access-form"
            onSubmit={handleVerifyOTP}
          >

            <div className="otp-sent-message">

              <strong>
                {t("citizenAccess.otpSentSuccess")}
              </strong>

              <p>
                {t("citizenAccess.otpSentMsg")}
              </p>

              <strong>
                +91 {mobile}
              </strong>

            </div>

            <label htmlFor="otp">
              {t("citizenAccess.enterOtpLabel")}
            </label>

            <input
              id="otp"
              data-testid="otp-code-input"
              type="text"
              inputMode="numeric"
              autoComplete="one-time-code"
              maxLength={6}
              placeholder={t("citizenAccess.otpPlaceholder")}
              value={otp}
              onChange={(event) => {
                const value = event.target.value.replace(/\D/g, "");
                setOtp(value);
              }}
              disabled={loading}
              autoFocus
            />

            <button
              type="submit"
              data-testid="otp-submit-button"
              className="citizen-primary-button"
              disabled={loading}
            >
              {loading
                ? t("citizenAccess.verifying")
                : t("citizenAccess.verifyOtp")
              }
            </button>

            <div className="otp-actions">

              <button
                type="button"
                data-testid="otp-resend-button"
                className="text-button"
                onClick={handleResendOTP}
                disabled={loading}
              >
                {t("citizenAccess.resendOtp")}
              </button>

              <button
                type="button"
                data-testid="otp-change-number-button"
                className="text-button"
                onClick={handleChangeNumber}
                disabled={loading}
              >
                {t("citizenAccess.changeNumber")}
              </button>

            </div>

          </form>
        )}

        {/* =========================
            ERROR MESSAGE
        ========================= */}

        {error && (
          <div
            data-testid="otp-error-message"
            className="citizen-error"
            role="alert"
          >
            {error}
          </div>
        )}

        {/* =========================
            SUCCESS MESSAGE
        ========================= */}

        {success && (
          <div
            data-testid="otp-success-message"
            className="citizen-success"
            role="status"
          >
            {success}
          </div>
        )}

        {/* =========================
            SECURITY NOTICE
        ========================= */}

        <div className="citizen-access-notice">

          <strong>
            {t("citizenAccess.secureNoticeTitle")}
          </strong>

          <p>
            {t("citizenAccess.secureNoticeDesc")}
          </p>

        </div>

      </div>

    </div>
  );
}

export default CitizenAccess;