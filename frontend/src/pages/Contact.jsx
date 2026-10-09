import { useTranslation } from "../i18n";
import "./Contact.css";

function Contact() {
  const { t, language } = useTranslation();

  return (
    <div className="contact-page">

      <section className="contact-header">
        <div className="container">
          <span className="page-kicker">
            {t("nav.help")}
          </span>

          <h1>{t("footer.contact")}</h1>

          <p>
            {language === "kn"
              ? "ಪ್ರಾತ್ಯಕ್ಷಿಕೆ ಪೋರ್ಟಲ್‌ಗಾಗಿ ಮಾದರಿ ಸಂಪರ್ಕ ಮಾಹಿತಿ."
              : language === "hi"
              ? "प्रदर्शन पोर्टल के लिए नमूना संपर्क जानकारी।"
              : "Sample contact information for the demonstration portal."}
          </p>
        </div>
      </section>

      <section className="contact-section">
        <div className="container">

          <div className="contact-grid">

            <div className="contact-card">
              <h2>{language === "kn" ? "ನಾಗರಿಕ ಬೆಂಬಲ" : language === "hi" ? "नागरिक सहायता" : "Citizen Support"}</h2>

              <p>
                {language === "kn"
                  ? "ಪ್ರಾತ್ಯಕ್ಷಿಕೆ ಉದ್ದೇಶಗಳಿಗಾಗಿ, ಈ ಕೆಳಗಿನ ಸಂಪರ್ಕ ವಿವರಗಳನ್ನು ಮಾದರಿ ಮಾಹಿತಿಯಾಗಿ ಪ್ರದರ್ಶಿಸಲಾಗಿದೆ."
                  : language === "hi"
                  ? "प्रदर्शन उद्देश्यों के लिए, निम्नलिखित संपर्क विवरण नमूना जानकारी के रूप में प्रदर्शित किए गए हैं।"
                  : "For demonstration purposes, the following contact details are displayed as sample information."}
              </p>

              <div className="contact-detail">
                <strong>{language === "kn" ? "ಇಮೇಲ್" : language === "hi" ? "ईमेल" : "Email"}</strong>
                <span>support@example.gov.in</span>
              </div>

              <div className="contact-detail">
                <strong>{language === "kn" ? "ಸಹಾಯವಾಣಿ" : language === "hi" ? "हेल्पलाइन" : "Helpline"}</strong>
                <span>1800-000-0000</span>
              </div>

              <div className="contact-detail">
                <strong>{language === "kn" ? "ಕೆಲಸದ ಸಮಯ" : language === "hi" ? "कार्य समय" : "Working Hours"}</strong>
                <span>Monday – Friday, 9:00 AM – 5:00 PM</span>
              </div>
            </div>

            <div className="contact-card">
              <h2>{language === "kn" ? "ಪೋರ್ಟಲ್ ಪ್ರತಿಕ್ರಿಯೆ" : language === "hi" ? "पोर्टल प्रतिक्रिया" : "Portal Feedback"}</h2>

              <p>
                {language === "kn"
                  ? "ಅಭಿವೃದ್ಧಿಯ ಸಮಯದಲ್ಲಿ ಈ ಪ್ರಾತ್ಯಕ್ಷಿಕೆ ಇಂಟರ್ಫೇಸ್ ಬಗ್ಗೆ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ದಾಖಲಿಸಬಹುದು."
                  : language === "hi"
                  ? "विकास के दौरान इस प्रदर्शन इंटरफ़ेस के बारे में प्रतिक्रिया दर्ज की जा सकती है।"
                  : "Feedback about this demonstration interface can be recorded here during development."}
              </p>

              <div className="contact-detail">
                <strong>{language === "kn" ? "ಉದ್ದೇಶ" : language === "hi" ? "उद्देश्य" : "Purpose"}</strong>
                <span>
                  UI testing, accessibility feedback and feature suggestions.
                </span>
              </div>

              <div className="contact-detail">
                <strong>{language === "kn" ? "ಗಮನಿಸಿ" : language === "hi" ? "सूचना" : "Notice"}</strong>
                <span>
                  {t("footer.demoText")}
                </span>
              </div>
            </div>

          </div>

        </div>
      </section>

    </div>
  );
}

export default Contact;