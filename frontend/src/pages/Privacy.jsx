import { useTranslation } from "../i18n";
import "./Privacy.css";

function Privacy() {
  const { t, language } = useTranslation();

  return (
    <div className="info-page">

      <section className="info-header">
        <div className="container">
          <span className="page-kicker">{t("footer.importantTitle")}</span>
          <h1>{t("footer.privacy")}</h1>
          <p>
            {language === "kn"
              ? "ಈ ಪ್ರಾತ್ಯಕ್ಷಿಕೆ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಗೌಪ್ಯತೆಯ ಬಗ್ಗೆ ಮಾಹಿತಿ."
              : language === "hi"
              ? "इस प्रदर्शन पोर्टल में गोपनीयता के बारे में जानकारी।"
              : "Information about privacy within this demonstration portal."}
          </p>
        </div>
      </section>

      <section className="info-section">
        <div className="container">

          <div className="info-card">
            <h2>{language === "kn" ? "ಪ್ರಾತ್ಯಕ್ಷಿಕೆ ಪರಿಸರ" : language === "hi" ? "प्रदर्शन परिवेश" : "Demonstration Environment"}</h2>
            <p>
              {language === "kn"
                ? "ಈ ಪೋರ್ಟಲ್ ಒಂದು ತಂತ್ರಾಂಶ ಪ್ರಾತ್ಯಕ್ಷಿಕೆಯಾಗಿದೆ. ಇದು ನೈಜ ಸರ್ಕಾರಿ ಡೇಟಾಬೇಸ್‌ಗಳಿಗೆ ಸಂಪರ್ಕ ಹೊಂದಿಲ್ಲ."
                : language === "hi"
                ? "यह पोर्टल एक सॉफ्टवेयर प्रदर्शन है। यह वास्तविक सरकारी डेटाबेस से कनेक्ट नहीं होता है।"
                : "This portal is a software demonstration. It does not connect to live government databases or process real citizen applications."}
            </p>
          </div>

          <div className="info-card">
            <h2>{language === "kn" ? "ಮಾದರಿ ದಾಖಲೆಗಳು" : language === "hi" ? "नमूना दस्तावेज़" : "Mock Documents"}</h2>
            <p>
              {language === "kn"
                ? "ದಾಖಲೆ ಕೇಂದ್ರದಲ್ಲಿ ಪ್ರದರ್ಶಿಸಲಾದ ದಾಖಲೆಗಳು ಪ್ರಾತ್ಯಕ್ಷಿಕೆ ಉದ್ದೇಶಗಳಿಗಾಗಿ ರಚಿಸಲಾದ ಕಾಲ್ಪನಿಕ ಉದಾಹರಣೆಗಳಾಗಿವೆ."
                : language === "hi"
                ? "दस्तावेज़ केंद्र में प्रदर्शित दस्तावेज़ प्रदर्शन उद्देश्यों के लिए बनाए गए काल्पनिक उदाहरण हैं।"
                : "Documents displayed in the Document Centre are fictional examples created for demonstration purposes. Users should not upload real sensitive documents."}
            </p>
          </div>

          <div className="info-card">
            <h2>{language === "kn" ? "ಮಾದರಿ ಮಾಹಿತಿ" : language === "hi" ? "नमूना जानकारी" : "Sample Information"}</h2>
            <p>
              {language === "kn"
                ? "ಪೋರ್ಟಲ್‌ನಲ್ಲಿರುವ ಯೋಜನಾ ಮಾಹಿತಿ, ಅರ್ಹತಾ ಷರತ್ತುಗಳು ಪ್ರಾತ್ಯಕ್ಷಿಕೆ ಡೇಟಾವಾಗಿದೆ."
                : language === "hi"
                ? "पोर्टल पर योजना की जानकारी, पात्रता शर्तें प्रदर्शन डेटा हैं।"
                : "Scheme information, eligibility conditions and contact information used by this version of the portal are demonstration data."}
            </p>
          </div>

          <div className="info-card">
            <h2>{language === "kn" ? "ಭವಿಷ್ಯದ ಉತ್ಪಾದನಾ ಆವೃತ್ತಿ" : language === "hi" ? "भावी उत्पादन संस्करण" : "Future Production Version"}</h2>
            <p>
              {language === "kn"
                ? "ಉತ್ಪಾದನಾ ವ್ಯವಸ್ಥೆಯು ಸೂಕ್ತವಾದ ಭದ್ರತೆ, ದೃಢೀಕರಣ ಮತ್ತು ಗೌಪ್ಯತೆ ಸುರಕ್ಷತೆಗಳನ್ನು ಒಳಗೊಂಡಿರುತ್ತದೆ."
                : language === "hi"
                ? "उत्पादन प्रणाली में उचित सुरक्षा, प्रमाणीकरण और गोपनीयता सुरक्षा उपाय शामिल होंगे।"
                : "A production system would require appropriate security, authentication, authorization, encryption, data retention controls and applicable privacy safeguards."}
            </p>
          </div>

        </div>
      </section>

    </div>
  );
}

export default Privacy;