import { useTranslation } from "../i18n";
import "./Accessibility.css";

function Accessibility() {
  const { t, language } = useTranslation();

  return (
    <div className="accessibility-page">

      <section className="accessibility-header">
        <div className="container">
          <span className="page-kicker">
            {t("header.accessibility")}
          </span>

          <h1>{t("header.accessibility")}</h1>

          <p>
            {language === "kn"
              ? "ಈ ಪ್ರಾತ್ಯಕ್ಷಿಕೆ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಲಭ್ಯವಿರುವ ಪ್ರವೇಶಸಾಧ್ಯತೆಯ ವೈಶಿಷ್ಟ್ಯಗಳ ಬಗ್ಗೆ ಮಾಹಿತಿ."
              : language === "hi"
              ? "इस प्रदर्शन पोर्टल में उपलब्ध अभिगम्यता सुविधाओं के बारे में जानकारी।"
              : "Information about accessibility features available in this demonstration portal."}
          </p>
        </div>
      </section>

      <section className="accessibility-section">
        <div className="container">

          <div className="accessibility-card">
            <h2>{language === "kn" ? "ನಮ್ಮ ಪ್ರವೇಶಸಾಧ್ಯತೆ ವಿಧಾನ" : language === "hi" ? "हमारा अभिगम्यता दृष्टिकोण" : "Our Accessibility Approach"}</h2>
            <p>
              {language === "kn"
                ? "ವಿವಿಧ ಬಳಕೆದಾರರು ಮತ್ತು ಸಾಧನಗಳಿಗೆ ಮಾಹಿತಿ ಮತ್ತು ಸೇವೆಗಳನ್ನು ಸುಲಭವಾಗಿ ಪ್ರವೇಶಿಸಲು ಸಾಧ್ಯವಾಗುವಂತೆ ಈ ಪೋರ್ಟಲ್ ಅನ್ನು ವಿನ್ಯಾಸಗೊಳಿಸಲಾಗಿದೆ."
                : language === "hi"
                ? "यह पोर्टल इस बात को ध्यान में रखकर तैयार किया गया है कि विभिन्न उपयोगकर्ताओं और उपकरणों के लिए सूचना और सेवाओं तक पहुँचना आसान हो।"
                : "This portal is designed with accessibility in mind so that information and services can be easier to access for different users and devices."}
            </p>
          </div>

          <div className="accessibility-grid">
            <div className="accessibility-item">
              <h2>{language === "kn" ? "ಕೀಬೋರ್ಡ್ ನ್ಯಾವಿಗೇಶನ್" : language === "hi" ? "कीबोर्ड नेविगेशन" : "Keyboard Navigation"}</h2>
              <p>
                {language === "kn"
                  ? "ಸಂವಾದಾತ್ಮಕ ನಿಯಂತ್ರಣಗಳು ಕೀಬೋರ್ಡ್ ನ್ಯಾವಿಗೇಶನ್ ಅನ್ನು ಬೆಂಬಲಿಸಲು ವಿನ್ಯಾಸಗೊಳಿಸಲಾಗಿದೆ."
                  : language === "hi"
                  ? "इंटरैक्टिव नियंत्रण कीबोर्ड नेविगेशन का समर्थन करने के लिए डिज़ाइन किए गए हैं।"
                  : "Interactive controls are designed to support keyboard navigation."}
              </p>
            </div>

            <div className="accessibility-item">
              <h2>{language === "kn" ? "ಸ್ಪಷ್ಟ ಓದುವಿಕೆ" : language === "hi" ? "सुपाठ्य सामग्री" : "Readable Content"}</h2>
              <p>
                {language === "kn"
                  ? "ಸ್ಪಷ್ಟ ಮುದ್ರಣಕಲೆ, ಅಂತರ ಮತ್ತು ಬಣ್ಣ ವ್ಯತಿರಿಕ್ತತೆಯನ್ನು ಇಂಟರ್ಫೇಸ್‌ನಾದ್ಯಂತ ಬಳಸಲಾಗುತ್ತದೆ."
                  : language === "hi"
                  ? "पूरे इंटरफ़ेस में स्पष्ट टाइपोग्राफी, स्पेसिंग और कंट्रास्ट का उपयोग किया जाता है।"
                  : "Clear typography, spacing and colour contrast are used throughout the interface."}
              </p>
            </div>

            <div className="accessibility-item">
              <h2>{language === "kn" ? "ರೆಸ್ಪಾನ್ಸಿವ್ ವಿನ್ಯಾಸ" : language === "hi" ? "प्रतिक्रियाशील डिज़ाइन" : "Responsive Design"}</h2>
              <p>
                {language === "kn"
                  ? "ಡೆಸ್ಕ್‌ಟಾಪ್‌ಗಳು, ಟ್ಯಾಬ್ಲೆಟ್‌ಗಳು ಮತ್ತು ಮೊಬೈಲ್ ಪರದೆಗಳಿಗೆ ಹೊಂದಿಕೊಳ್ಳುವಂತೆ ಪುಟಗಳನ್ನು ವಿನ್ಯಾಸಗೊಳಿಸಲಾಗಿದೆ."
                  : language === "hi"
                  ? "पेजों को डेस्कटॉप, टैबलेट और मोबाइल स्क्रीन के अनुकूल डिज़ाइन किया गया है।"
                  : "Pages are designed to adapt to desktops, tablets and smaller screens."}
              </p>
            </div>

            <div className="accessibility-item">
              <h2>{language === "kn" ? "ಭಾಷಾ ಬೆಂಬಲ" : language === "hi" ? "भाषा समर्थन" : "Language Support"}</h2>
              <p>
                {language === "kn"
                  ? "ಪೋರ್ಟಲ್ ಇಂಗ್ಲಿಷ್, ಹಿಂದಿ ಮತ್ತು ಕನ್ನಡ ಇಂಟರ್ಫೇಸ್‌ಗಳನ್ನು ಬೆಂಬಲಿಸುತ್ತದೆ."
                  : language === "hi"
                  ? "पोर्टल अंग्रेज़ी, हिन्दी और कन्नड़ इंटरफेस का समर्थन करता है।"
                  : "The portal supports English, Hindi and Kannada interfaces."}
              </p>
            </div>
          </div>

          <div className="accessibility-card">
            <h2>{language === "kn" ? "ಪ್ರವೇಶಸಾಧ್ಯತೆ ಪ್ರತಿಕ್ರಿಯೆ" : language === "hi" ? "अभिगम्यता प्रतिक्रिया" : "Accessibility Feedback"}</h2>
            <p>
              {language === "kn"
                ? "ಬಳಕೆದಾರರಿಗೆ ಮಾಹಿತಿಯನ್ನು ಪ್ರವೇಶಿಸುವಲ್ಲಿ ಅಥವಾ ಪೋರ್ಟಲ್ ನ್ಯಾವಿಗೇಟ್ ಮಾಡುವಲ್ಲಿ ತೊಂದರೆ ಉಂಟಾದರೆ, ಸಂಪರ್ಕ ಪುಟದ ಮೂಲಕ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ನೀಡಬಹುದು."
                : language === "hi"
                ? "यदि किसी उपयोगकर्ता को जानकारी प्राप्त करने या पोर्टल पर नेविगेट करने में कठिनाई होती है, तो संपर्क पृष्ठ के माध्यम से प्रतिक्रिया दी जा सकती है।"
                : "If a user experiences difficulty accessing information or navigating the demonstration portal, feedback can be provided through the Contact page."}
            </p>
          </div>

        </div>
      </section>

    </div>
  );
}

export default Accessibility;