import { useState } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "../i18n";
import "./Help.css";

function Help() {
  const { t, language } = useTranslation();
  const [openIndex, setOpenIndex] = useState(null);

  const faqs = [
    {
      question: language === "kn"
        ? "ಈ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ನಾನು ಏನು ಮಾಡಬಹುದು?"
        : language === "hi"
        ? "मैं इस पोर्टल पर क्या कर सकता हूँ?"
        : "What can I do on this portal?",
      answer: language === "kn"
        ? "ಈ ಪೋರ್ಟಲ್ ಮೂಲಕ ಬಳಕೆದಾರರು ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಅನ್ವೇಷಿಸಬಹುದು, ಅರ್ಹತಾ ಮಾನದಂಡಗಳು ಮತ್ತು ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ಪರಿಶೀಲಿಸಬಹುದು ಮತ್ತು ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಬಹುದು."
        : language === "hi"
        ? "यह पोर्टल उपयोगकर्ताओं को सरकारी योजनाओं का पता लगाने, पात्रता मानदंडों और आवश्यक दस्तावेजों की जांच करने और ऑनलाइन आवेदन करने की सुविधा देता है।"
        : "This demonstration portal allows users to explore government schemes, verify eligibility criteria, check required documents, and submit applications online."
    },
    {
      question: language === "kn"
        ? "ಯೋಜನೆಯನ್ನು ಹೇಗೆ ಕಂಡುಹಿಡಿಯುವುದು?"
        : language === "hi"
        ? "मैं कोई योजना कैसे खोजूँ?"
        : "How do I find a scheme?",
      answer: language === "kn"
        ? "ನಾಗರಿಕ ಸೇವೆಗಳಿಂದ ಯೋಜನಾ ಶೋಧಕವನ್ನು ತೆರೆಯಿರಿ ಅಥವಾ ಯೋಜನೆಗಳ ಡೈರೆಕ್ಟರಿಯಿಂದ ವರ್ಗದ ಪ್ರಕಾರ ಬ್ರೌಸ್ ಮಾಡಿ."
        : language === "hi"
        ? "नागरिक सेवाओं से योजना खोजक खोलें या योजना निर्देशिका से श्रेणी के आधार पर ब्राउज़ करें।"
        : "Open Scheme Finder from Citizen Services or browse the Schemes directory by category or keyword."
    },
    {
      question: language === "kn"
        ? "ಅಗತ್ಯವಿರುವ ದಾಖಲೆಗಳನ್ನು ನಾನು ಎಲ್ಲಿ ನೋಡಬಹುದು?"
        : language === "hi"
        ? "मैं आवश्यक दस्तावेज़ कहाँ देख सकता हूँ?"
        : "Where can I see required documents?",
      answer: language === "kn"
        ? "ದಾಖಲೆ ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ ಅಥವಾ ನಾಗರಿಕ ಸೇವೆಗಳ ಅಡಿಯಲ್ಲಿ ದಾಖಲೆ ಪರಿಶೀಲನಾ ಪಟ್ಟಿಯನ್ನು ಬಳಸಿ."
        : language === "hi"
        ? "दस्तावेज़ केंद्र पर जाएं या नागरिक सेवाओं के अंतर्गत दस्तावेज़ चेकलिस्ट का उपयोग करें।"
        : "Visit the Document Centre or use the Document Checklist under Citizen Services to view requirements."
    },
    {
      question: language === "kn"
        ? "ಯಾವ ಭಾಷೆಗಳನ್ನು ಬೆಂಬಲಿಸಲಾಗುತ್ತದೆ?"
        : language === "hi"
        ? "किन भाषाओं का समर्थन है?"
        : "Which languages are supported?",
      answer: language === "kn"
        ? "ಈ ಪೋರ್ಟಲ್ ಇಂಗ್ಲಿಷ್, ಕನ್ನಡ ಮತ್ತು ಹಿಂದಿ ಭಾಷೆಗಳನ್ನು ಬೆಂಬಲಿಸುತ್ತದೆ. ಹೆಡರ್‌ನಲ್ಲಿರುವ ಭಾಷಾ ಆಯ್ಕೆಯ ಮೂಲಕ ನೀವು ಭಾಷೆಯನ್ನು ಬದಲಾಯಿಸಬಹುದು."
        : language === "hi"
        ? "यह पोर्टल अंग्रेज़ी, कन्नड़ और हिन्दी का समर्थन करता है। आप हेडर में भाषा चयनकर्ता का उपयोग करके भाषा बदल सकते हैं।"
        : "The portal supports English, Kannada, and Hindi. You can switch languages anytime using the language selector in the header."
    },
  ];

  const toggleFaq = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="help-page">

      <section className="help-header">
        <div className="container">

          <span className="page-kicker">
            {t("help.title")}
          </span>

          <h1>{t("help.title")}</h1>

          <p>
            {t("help.subtitle")}
          </p>

        </div>
      </section>


      <section className="help-section">
        <div className="container">

          <div className="help-grid">

            <div className="help-main">

              <div className="section-heading">
                <h2>{t("footer.faq")}</h2>

                <p>
                  {t("help.subtitle")}
                </p>
              </div>


              <div className="faq-list">

                {faqs.map((faq, index) => (

                  <div
                    className={`faq-item ${
                      openIndex === index ? "open" : ""
                    }`}
                    key={index}
                  >

                    <button
                      type="button"
                      className="faq-question"
                      onClick={() => toggleFaq(index)}
                      aria-expanded={openIndex === index}
                    >

                      <span>{faq.question}</span>

                      <span className="faq-icon">
                        {openIndex === index ? "−" : "+"}
                      </span>

                    </button>


                    {openIndex === index && (
                      <div className="faq-answer">
                        <p>{faq.answer}</p>
                      </div>
                    )}

                  </div>

                ))}

              </div>

            </div>


            <aside className="help-sidebar">

              <div className="help-card">

                <h2>{t("help.quickLinks")}</h2>

                <Link to="/schemes">
                  {t("nav.schemes")}
                </Link>

                <Link to="/documents">
                  {t("nav.documents")}
                </Link>

                <Link to="/citizen-services/scheme-finder">
                  {t("services.schemeFinderTitle")}
                </Link>

                <Link to="/citizen-services/documents">
                  {t("services.docChecklistTitle")}
                </Link>

              </div>


              <div className="help-card">

                <h2>{t("help.contactSupport")}</h2>

                <p>
                  {t("help.contactSupportDesc")}
                </p>

                <Link to="/contact" className="help-button">
                  {t("footer.contact")}
                </Link>

              </div>

            </aside>

          </div>

        </div>
      </section>

    </div>
  );
}

export default Help;