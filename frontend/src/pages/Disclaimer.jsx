import { useTranslation } from "../i18n";
import "./Privacy.css";

function Disclaimer() {
  const { t, language } = useTranslation();

  return (
    <div className="info-page">

      <section className="info-header">
        <div className="container">
          <span className="page-kicker">{t("footer.importantTitle")}</span>

          <h1>{t("footer.disclaimer")}</h1>

          <p>
            {language === "kn"
              ? "ಈ ಪ್ರಾತ್ಯಕ್ಷಿಕೆ ಪೋರ್ಟಲ್‌ನ ಉದ್ದೇಶ ಮತ್ತು ಮಿತಿಗಳ ಬಗ್ಗೆ ಪ್ರಮುಖ ಮಾಹಿತಿ."
              : language === "hi"
              ? "इस प्रदर्शन पोर्टल के उद्देश्य और सीमाओं के बारे में महत्वपूर्ण जानकारी।"
              : "Important information about the purpose and limitations of this demonstration portal."}
          </p>
        </div>
      </section>

      <section className="info-section">
        <div className="container">

          <div className="info-card">
            <h2>{language === "kn" ? "ಪ್ರಾತ್ಯಕ್ಷಿಕೆ ಮಾತ್ರ" : language === "hi" ? "केवल प्रदर्शन" : "Demonstration Only"}</h2>
            <p>
              {t("footer.demoText")}
            </p>
          </div>

          <div className="info-card">
            <h2>{language === "kn" ? "ಯೋಜನಾ ಮಾಹಿತಿ" : language === "hi" ? "योजना जानकारी" : "Scheme Information"}</h2>
            <p>
              {language === "kn"
                ? "ಈ ಆವೃತ್ತಿಯಲ್ಲಿ ಪ್ರದರ್ಶಿಸಲಾದ ಯೋಜನೆಯ ಹೆಸರುಗಳು, ವಿವರಣೆಗಳು, ಪ್ರಯೋಜನಗಳು, ಅರ್ಹತಾ ಷರತ್ತುಗಳು ಮತ್ತು ಅಪ್ಲಿಕೇಶನ್ ಮಾಹಿತಿಯು ಪ್ರಾತ್ಯಕ್ಷಿಕೆ ಉದ್ದೇಶಗಳಿಗಾಗಿ ಮಾದರಿಯಾಗಿರಬಹುದು."
                : language === "hi"
                ? "इस संस्करण में प्रदर्शित योजना के नाम, विवरण, लाभ, पात्रता शर्तें और आवेदन की जानकारी प्रदर्शन उद्देश्यों के लिए नमूना हो सकती है।"
                : "Scheme names, descriptions, benefits, eligibility conditions and application information displayed in this version may be fictional or simplified for demonstration purposes."}
            </p>
          </div>

          <div className="info-card">
            <h2>{language === "kn" ? "ಅರ್ಹತಾ ಮಾಹಿತಿ" : language === "hi" ? "पात्रता जानकारी" : "Eligibility Information"}</h2>
            <p>
              {language === "kn"
                ? "ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಒದಗಿಸಲಾದ ಫಲಿತಾಂಶಗಳು ಮಾದರಿ ನಿಯಮಗಳನ್ನು ಆಧರಿಸಿವೆ ಮತ್ತು ಅಧಿಕೃತ ನಿರ್ಧಾರವೆಂದು ಪರಿಗಣಿಸಬಾರದು."
                : language === "hi"
                ? "पोर्टल पर दिए गए परिणाम नमूना नियमों पर आधारित हैं और इन्हें आधिकारिक निर्णय नहीं माना जाना चाहिए।"
                : "Results and information produced are based on sample demonstration rules and must not be considered an official determination of eligibility."}
            </p>
          </div>

          <div className="info-card">
            <h2>{language === "kn" ? "ಅಧಿಕೃತ ಮೂಲಗಳು" : language === "hi" ? "आधिकारिक स्रोत" : "Official Sources"}</h2>
            <p>
              {language === "kn"
                ? "ಸರ್ಕಾರಿ ಯೋಜನಾ ಮಾಹಿತಿಯ ಆಧಾರದ ಮೇಲೆ ಕ್ರಮ ಕೈಗೊಳ್ಳುವ ಮೊದಲು, ಬಳಕೆದಾರರು ಸಂಬಂಧಿತ ಅಧಿಕೃತ ಸರ್ಕಾರಿ ಮೂಲದ ಮೂಲಕ ಪ್ರಸ್ತುತ ಅವಶ್ಯಕತೆಗಳು ಮತ್ತು ದಾಖಲೆಗಳನ್ನು ಪರಿಶೀಲಿಸಬೇಕು."
                : language === "hi"
                ? "सरकारी योजना की जानकारी के आधार पर कार्रवाई करने से पहले, उपयोगकर्ताओं को संबंधित आधिकारिक सरकारी स्रोत के माध्यम से वर्तमान आवश्यकताओं और दस्तावेजों को सत्यापित करना चाहिए।"
                : "Before taking action based on government scheme information, users should verify current requirements, eligibility conditions, documents and application procedures through the relevant official government source."}
            </p>
          </div>

        </div>
      </section>

    </div>
  );
}

export default Disclaimer;