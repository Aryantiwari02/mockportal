from django.core.management.base import BaseCommand
from schemes.models import Scheme


class Command(BaseCommand):
    help = "Seed demonstration government schemes into the database with multilingual translations"

    def handle(self, *args, **kwargs):

        schemes = [
            {
                "id": "health-001",
                "category": "Health",
                "title": "National Health Support Scheme",
                "short_description": "Healthcare assistance for eligible citizens requiring support for medical treatment.",
                "description": "This demonstration scheme provides financial and healthcare assistance to eligible citizens for specified medical treatment and healthcare needs.",
                "eligibility": [
                    "Applicant must be a resident citizen.",
                    "Applicant must satisfy the applicable income criteria.",
                    "Applicant must provide the required supporting documents.",
                    "Additional conditions may apply depending on the type of assistance."
                ],
                "eligibility_rules": {
                    "max_income": 500000
                },
                "benefits": [
                    "Financial assistance for eligible healthcare expenses.",
                    "Support for specified medical treatments.",
                    "Access to participating healthcare facilities.",
                    "Reduced financial burden for eligible families."
                ],
                "documents": [
                    "Identity Proof",
                    "Residence Proof",
                    "Income Certificate",
                    "Bank Account Details",
                    "Medical Documents, where applicable"
                ],
                "application_fields": [
                    {
                        "name": "full_name",
                        "label": "Full Name of Patient / Beneficiary",
                        "type": "text",
                        "required": True,
                        "placeholder": "Enter full name as per Govt ID",
                        "help_text": "Must match the identity proof document."
                    },
                    {
                        "name": "dob",
                        "label": "Date of Birth",
                        "type": "date",
                        "required": True,
                        "help_text": "Beneficiary date of birth."
                    },
                    {
                        "name": "gender",
                        "label": "Gender",
                        "type": "select",
                        "required": True,
                        "options": ["Male", "Female", "Other"]
                    },
                    {
                        "name": "annual_income",
                        "label": "Annual Family Income (INR)",
                        "type": "number",
                        "required": True,
                        "placeholder": "e.g. 240000",
                        "help_text": "Must not exceed ₹5,00,000 for full benefit."
                    },
                    {
                        "name": "hospital_name",
                        "label": "Hospital / Medical Center Name",
                        "type": "text",
                        "required": True,
                        "placeholder": "e.g. AIIMS / District Civil Hospital"
                    },
                    {
                        "name": "medical_condition",
                        "label": "Medical Diagnosis / Ailment",
                        "type": "textarea",
                        "required": True,
                        "placeholder": "Briefly describe the illness or treatment required"
                    },
                    {
                        "name": "bank_account_number",
                        "label": "Bank Account Number for DBT",
                        "type": "text",
                        "required": True,
                        "placeholder": "Account number for direct assistance"
                    },
                    {
                        "name": "bank_ifsc",
                        "label": "Bank IFSC Code",
                        "type": "text",
                        "required": True,
                        "placeholder": "e.g. SBIN0001234"
                    },
                    {
                        "name": "address",
                        "label": "Residential Address",
                        "type": "textarea",
                        "required": True,
                        "placeholder": "Complete residential address with District & PIN Code"
                    },
                    {
                        "name": "declaration_consent",
                        "label": "I hereby certify that all information submitted is accurate and medical documents are genuine.",
                        "type": "checkbox",
                        "required": True
                    }
                ],
                "application_process": [
                    "Check your eligibility.",
                    "Prepare the required documents.",
                    "Complete the application form.",
                    "Submit the application through the designated channel.",
                    "Track the application status."
                ],
                "translations": {
                    "kn": {
                        "title": "ರಾಷ್ಟ್ರೀಯ ಆರೋಗ್ಯ ಬೆಂಬಲ ಯೋಜನೆ",
                        "category": "ಆರೋಗ್ಯ",
                        "short_description": "ವೈದ್ಯಕೀಯ ಚಿಕಿತ್ಸೆಗಾಗಿ ಬೆಂಬಲ ಅಗತ್ಯವಿರುವ ಅರ್ಹ ನಾಗರಿಕರಿಗೆ ಆರೋಗ್ಯ ನೆರವು.",
                        "description": "ಈ ಪ್ರದರ್ಶನ ಯೋಜನೆಯು ನಿರ್ದಿಷ್ಟ ವೈದ್ಯಕೀಯ ಚಿಕಿತ್ಸೆ ಮತ್ತು ಆರೋಗ್ಯ ಅಗತ್ಯಗಳಿಗಾಗಿ ಅರ್ಹ ನಾಗರಿಕರಿಗೆ ಆರ್ಥಿಕ ಮತ್ತು ಆರೋಗ್ಯ ನೆರವನ್ನು ಒದಗಿಸುತ್ತದೆ.",
                        "eligibility": [
                            "ಅರ್ಜಿದಾರರು ಭಾರತದ ನಿವಾಸಿ ನಾಗರಿಕರಾಗಿರಬೇಕು.",
                            "ಅರ್ಜಿದಾರರು ಅನ್ವಯವಾಗುವ ಆದಾಯ ಮಾನದಂಡಗಳನ್ನು ಪೂರೈಸಬೇಕು.",
                            "ಅರ್ಜಿದಾರರು ಅಗತ್ಯವಿರುವ ಪೂರಕ ದಾಖಲೆಗಳನ್ನು ಒದಗಿಸಬೇಕು.",
                            "ಸಹಾಯದ ಪ್ರಕಾರವನ್ನು ಆಧರಿಸಿ ಹೆಚ್ಚುವರಿ ಷರತ್ತುಗಳು ಅನ್ವಯಿಸಬಹುದು."
                        ],
                        "benefits": [
                            "ಅರ್ಹ ಆರೋಗ್ಯ ವೆಚ್ಚಗಳಿಗೆ ಆರ್ಥಿಕ ನೆರವು.",
                            "ನಿರ್ದಿಷ್ಟ ವೈದ್ಯಕೀಯ ಚಿಕಿತ್ಸೆಗಳಿಗೆ ಬೆಂಬಲ.",
                            "ಭಾಗವಹಿಸುವ ಆರೋಗ್ಯ ಸೌಲಭ್ಯಗಳಿಗೆ ಪ್ರವೇಶ.",
                            "ಅರ್ಹ ಕುಟುಂಬಗಳಿಗೆ ಆರ್ಥಿಕ ಹೊರೆ ಕಡಿತ."
                        ],
                        "documents": [
                            "ಗುರುತಿನ ಪುರಾವೆ",
                            "ನಿವಾಸ ಪುರಾವೆ",
                            "ಆದಾಯ ಪ್ರಮಾಣಪತ್ರ",
                            "ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರಗಳು",
                            "ವೈದ್ಯಕೀಯ ದಾಖಲೆಗಳು (ಅನ್ವಯಿಸಿದಲ್ಲಿ)"
                        ],
                        "application_process": [
                            "ನಿಮ್ಮ ಅರ್ಹತೆಯನ್ನು ಪರಿಶೀಲಿಸಿ.",
                            "ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ಸಿದ್ಧಪಡಿಸಿ.",
                            "ಅರ್ಜಿ ನಮೂನೆಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ.",
                            "ನಿಯೋಜಿತ ಚಾನಲ್ ಮೂಲಕ ಅರ್ಜಿಯನ್ನು ಸಲ್ಲಿಸಿ.",
                            "ಅರ್ಜಿಯ ಸ್ಥಿತಿಯನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಿ."
                        ],
                        "application_fields": [
                            {"name": "full_name", "label": "ರೋಗಿ / ಫಲಾನುಭವಿಯ ಪೂರ್ಣ ಹೆಸರು", "placeholder": "ಸರ್ಕಾರಿ ಗುರುತಿನ ಚೀಟಿಯ ಪ್ರಕಾರ ಪೂರ್ಣ ಹೆಸರು ನಮೂದಿಸಿ"},
                            {"name": "dob", "label": "ಹುಟ್ಟಿದ ದಿನಾಂಕ"},
                            {"name": "gender", "label": "ಲಿಂಗ", "options": ["ಪುರುಷ", "ಮಹಿಳೆ", "ಇತರ"]},
                            {"name": "annual_income", "label": "ವಾರ್ಷಿಕ ಕುಟುಂಬ ಆದಾಯ (ರೂ.)", "placeholder": "ಉದಾ. 240000"},
                            {"name": "hospital_name", "label": "ಆಸ್ಪತ್ರೆ / ವೈದ್ಯಕೀಯ ಕೇಂದ್ರದ ಹೆಸರು", "placeholder": "ಉದಾ. ಏಮ್ಸ್ / ಜಿಲ್ಲಾ ನಾಗರಿಕ ಆಸ್ಪತ್ರೆ"},
                            {"name": "medical_condition", "label": "ವೈದ್ಯಕೀಯ ರೋಗನಿರ್ಣಯ / ಕಾಯಿಲೆ", "placeholder": "ಅಗತ್ಯವಿರುವ ಚಿಕಿತ್ಸೆಯನ್ನು ಸಂಕ್ಷಿಪ್ತವಾಗಿ ವಿವರಿಸಿ"},
                            {"name": "bank_account_number", "label": "ನೇರ ಪ್ರಯೋಜನಕ್ಕಾಗಿ ಬ್ಯಾಂಕ್ ಖಾತೆ ಸಂಖ್ಯೆ", "placeholder": "ಬ್ಯಾಂಕ್ ಖಾತೆ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ"},
                            {"name": "bank_ifsc", "label": "ಬ್ಯಾಂಕ್ IFSC ಕೋಡ್", "placeholder": "ಉದಾ. SBIN0001234"},
                            {"name": "address", "label": "ವಸತಿ ವಿಳಾಸ", "placeholder": "ಜಿಲ್ಲೆ ಮತ್ತು ಪಿನ್‌ಕೋಡ್‌ನೊಂದಿಗೆ ಸಂಪೂರ್ಣ ವಸತಿ ವಿಳಾಸ"},
                            {"name": "declaration_consent", "label": "ಸಲ್ಲಿಸಿದ ಎಲ್ಲಾ ಮಾಹಿತಿಯು ನಿಖರವಾಗಿದೆ ಮತ್ತು ವೈದ್ಯಕೀಯ ದಾಖಲೆಗಳು ನೈಜವಾಗಿವೆ ಎಂದು ನಾನು ಪ್ರಮಾಣೀಕರಿಸುತ್ತೇನೆ."}
                        ]
                    },
                    "hi": {
                        "title": "राष्ट्रीय स्वास्थ्य सहायता योजना",
                        "category": "स्वास्थ्य",
                        "short_description": "चिकित्सा उपचार के लिए सहायता चाहने वाले पात्र नागरिकों के लिए स्वास्थ्य सहायता।",
                        "description": "यह प्रदर्शन योजना निर्दिष्ट चिकित्सा उपचार और स्वास्थ्य देखभाल आवश्यकताओं के लिए पात्र नागरिकों को वित्तीय और स्वास्थ्य सहायता प्रदान करती है।",
                        "eligibility": [
                            "आवेदक निवासी नागरिक होना चाहिए।",
                            "आवेदक को लागू आय मानदंडों को पूरा करना चाहिए।",
                            "आवेदक को आवश्यक सहायक दस्तावेज उपलब्ध कराने होंगे।",
                            "सहायता के प्रकार के आधार पर अतिरिक्त शर्तें लागू हो सकती हैं।"
                        ],
                        "benefits": [
                            "पात्र स्वास्थ्य देखभाल खर्चों के लिए वित्तीय सहायता।",
                            "निर्दिष्ट चिकित्सा उपचारों के लिए समर्थन।",
                            "भाग लेने वाले स्वास्थ्य केंद्रों तक पहुंच।",
                            "पात्र परिवारों के लिए वित्तीय बोझ में कमी।"
                        ],
                        "documents": [
                            "पहचान प्रमाण",
                            "निवास प्रमाण",
                            "आय प्रमाण पत्र",
                            "बैंक खाता विवरण",
                            "चिकित्सा दस्तावेज (जहां लागू हो)"
                        ],
                        "application_process": [
                            "अपनी पात्रता जांचें।",
                            "आवश्यक दस्तावेज तैयार करें।",
                            "आवेदन पत्र पूरा भरें।",
                            "निर्दिष्ट माध्यम से आवेदन जमा करें।",
                            "आवेदन की स्थिति को ट्रैक करें।"
                        ],
                        "application_fields": [
                            {"name": "full_name", "label": "मरीज / लाभार्थी का पूरा नाम", "placeholder": "सरकारी पहचान पत्र के अनुसार पूरा नाम दर्ज करें"},
                            {"name": "dob", "label": "जन्म तिथि"},
                            {"name": "gender", "label": "लिंग", "options": ["पुरुष", "महिला", "अन्य"]},
                            {"name": "annual_income", "label": "वार्षिक पारिवारिक आय (रु.)", "placeholder": "उदा. 240000"},
                            {"name": "hospital_name", "label": "अस्पताल / चिकित्सा केंद्र का नाम", "placeholder": "उदा. एम्स / जिला नागरिक अस्पताल"},
                            {"name": "medical_condition", "label": "चिकित्सा निदान / बीमारी", "placeholder": "आवश्यक उपचार का संक्षिप्त विवरण दें"},
                            {"name": "bank_account_number", "label": "डीबीटी हेतु बैंक खाता संख्या", "placeholder": "बैंक खाता संख्या दर्ज करें"},
                            {"name": "bank_ifsc", "label": "बैंक आईएफएससी कोड", "placeholder": "उदा. SBIN0001234"},
                            {"name": "address", "label": "निवास का पता", "placeholder": "जिले और पिन कोड के साथ पूरा आवासीय पता"},
                            {"name": "declaration_consent", "label": "मैं प्रमाणित करता/करती हूँ कि प्रस्तुत जानकारी सत्य है और चिकित्सा दस्तावेज प्रामाणिक हैं।"}
                        ]
                    }
                }
            },

            {
                "id": "health-002",
                "category": "Health",
                "title": "Family Healthcare Assistance",
                "short_description": "Healthcare support information for eligible families.",
                "description": "A demonstration scheme providing healthcare-related assistance to eligible families based on defined eligibility conditions.",
                "eligibility": [
                    "Applicant must meet the applicable family eligibility criteria.",
                    "Applicant must provide valid identity and residence proof.",
                    "Income-related conditions may apply."
                ],
                "eligibility_rules": {
                    "max_income": 400000
                },
                "benefits": [
                    "Healthcare assistance.",
                    "Support for eligible medical expenses.",
                    "Access to applicable healthcare services."
                ],
                "documents": [
                    "Identity Proof",
                    "Residence Proof",
                    "Income Certificate",
                    "Family Details",
                    "Bank Account Details"
                ],
                "application_fields": [
                    {
                        "name": "applicant_name",
                        "label": "Head of Household / Applicant Name",
                        "type": "text",
                        "required": True,
                        "placeholder": "Full name of the family head"
                    },
                    {
                        "name": "dob",
                        "label": "Date of Birth",
                        "type": "date",
                        "required": True
                    },
                    {
                        "name": "gender",
                        "label": "Gender",
                        "type": "select",
                        "required": True,
                        "options": ["Male", "Female", "Other"]
                    },
                    {
                        "name": "family_members_count",
                        "label": "Number of Dependent Family Members",
                        "type": "number",
                        "required": True,
                        "placeholder": "e.g. 4"
                    },
                    {
                        "name": "ration_card_category",
                        "label": "Ration / Food Security Card Category",
                        "type": "select",
                        "required": True,
                        "options": ["BPL (Below Poverty Line)", "AAY (Antyodaya Anna)", "APL (State Ration Card)"]
                    },
                    {
                        "name": "annual_income",
                        "label": "Annual Household Income (INR)",
                        "type": "number",
                        "required": True,
                        "placeholder": "e.g. 180000"
                    },
                    {
                        "name": "coverage_preference",
                        "label": "Assistance Type Needed",
                        "type": "radio",
                        "required": True,
                        "options": ["In-Patient Hospitalization", "Outpatient Chronic Disease Care", "Diagnostic Support"]
                    },
                    {
                        "name": "bank_account_number",
                        "label": "Primary Bank Account Number",
                        "type": "text",
                        "required": True,
                        "placeholder": "Bank account number for DBT"
                    },
                    {
                        "name": "bank_ifsc",
                        "label": "Bank IFSC Code",
                        "type": "text",
                        "required": True,
                        "placeholder": "e.g. PUNB0123400"
                    },
                    {
                        "name": "address",
                        "label": "Family Residence Address",
                        "type": "textarea",
                        "required": True,
                        "placeholder": "Full home address with District & PIN Code"
                    },
                    {
                        "name": "declaration_consent",
                        "label": "I declare that the family members listed are dependent residents of the household.",
                        "type": "checkbox",
                        "required": True
                    }
                ],
                "application_process": [
                    "Review the eligibility conditions.",
                    "Collect the required documents.",
                    "Fill in the application.",
                    "Submit the application.",
                    "Wait for verification and processing."
                ],
                "translations": {
                    "kn": {
                        "title": "ಕುಟುಂಬ ಆರೋಗ್ಯ ನೆರವು ಯೋಜನೆ",
                        "category": "ಆರೋಗ್ಯ",
                        "short_description": "ಅರ್ಹ ಕುಟುಂಬಗಳಿಗೆ ಆರೋಗ್ಯ ಬೆಂಬಲ ಮಾಹಿತಿ ಮತ್ತು ನೆರವು.",
                        "description": "ವ್ಯಾಖ್ಯಾನಿಸಲಾದ ಅರ್ಹತಾ ಷರತ್ತುಗಳ ಆಧಾರದ ಮೇಲೆ ಅರ್ಹ ಕುಟುಂಬಗಳಿಗೆ ಆರೋಗ್ಯ ಸಂಬಂಧಿತ ನೆರವು ನೀಡುವ ಪ್ರದರ್ಶನ ಯೋಜನೆ.",
                        "eligibility": [
                            "ಅರ್ಜಿದಾರರು ಅನ್ವಯವಾಗುವ ಕುಟುಂಬ ಅರ್ಹತಾ ಮಾನದಂಡಗಳನ್ನು ಪೂರೈಸಬೇಕು.",
                            "ಅರ್ಜಿದಾರರು ಮಾನ್ಯವಾದ ಗುರುತು ಮತ್ತು ವಾಸಸ್ಥಳದ ಪುರಾವೆಯನ್ನು ಒದಗಿಸಬೇಕು.",
                            "ಆದಾಯ-ಸಂಬಂಧಿತ ಷರತ್ತುಗಳು ಅನ್ವಯಿಸಬಹುದು."
                        ],
                        "benefits": [
                            "ಕುಟುಂಬ ಆರೋಗ್ಯ ನೆರವು.",
                            "ಅರ್ಹ ವೈದ್ಯಕೀಯ ವೆಚ್ಚಗಳಿಗೆ ಬೆಂಬಲ.",
                            "ಆರೋಗ್ಯ ಸೇವೆಗಳಿಗೆ ಪ್ರವೇಶ."
                        ],
                        "documents": [
                            "ಗುರುತಿನ ಪುರಾವೆ",
                            "ನಿವಾಸ ಪುರಾವೆ",
                            "ಆದಾಯ ಪ್ರಮಾಣಪತ್ರ",
                            "ಕುಟುಂಬದ ವಿವರಗಳು",
                            "ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರಗಳು"
                        ],
                        "application_process": [
                            "ಅರ್ಹತಾ ಷರತ್ತುಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
                            "ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ಸಂಗ್ರಹಿಸಿ.",
                            "ಅರ್ಜಿಯನ್ನು ಭರ್ತಿ ಮಾಡಿ.",
                            "ಅರ್ಜಿಯನ್ನು ಸಲ್ಲಿಸಿ.",
                            "ಪರಿಶೀಲನೆ ಮತ್ತು ಪ್ರಕ್ರಿಯೆಗಾಗಿ ನಿರೀಕ್ಷಿಸಿ."
                        ],
                        "application_fields": [
                            {"name": "applicant_name", "label": "ಕುಟುಂಬದ ಮುಖ್ಯಸ್ಥ / ಅರ್ಜಿದಾರರ ಹೆಸರು", "placeholder": "ಕುಟುಂಬದ ಮುಖ್ಯಸ್ಥರ ಪೂರ್ಣ ಹೆಸರು"},
                            {"name": "dob", "label": "ಹುಟ್ಟಿದ ದಿನಾಂಕ"},
                            {"name": "gender", "label": "ಲಿಂಗ", "options": ["ಪುರುಷ", "ಮಹಿಳೆ", "ಇತರ"]},
                            {"name": "family_members_count", "label": "ಅವಲಂಬಿತ ಕುಟುಂಬ ಸದಸ್ಯರ ಸಂಖ್ಯೆ", "placeholder": "ಉದಾ. 4"},
                            {"name": "ration_card_category", "label": "ಪಡಿತರ ಚೀಟಿ ವರ್ಗ", "options": ["ಬಿಪಿಎಲ್ (ಬಡತನ ರೇಖೆಗಿಂತ ಕೆಳಗೆ)", "ಅಂತ್ಯೋದಯ", "ಎಪಿಎಲ್"]},
                            {"name": "annual_income", "label": "ವಾರ್ಷಿಕ ಕುಟುಂಬ ಆದಾಯ (ರೂ.)", "placeholder": "ಉದಾ. 180000"},
                            {"name": "coverage_preference", "label": "ಅಗತ್ಯವಿರುವ ನೆರವಿನ ವಿಧ", "options": ["ಒಳರೋಗಿ ಆಸ್ಪತ್ರೆ ದಾಖಲಾತಿ", "ಹೊರರೋಗಿ ಆರೈಕೆ", "ರೋಗನಿರ್ಣಯ ಬೆಂಬಲ"]},
                            {"name": "bank_account_number", "label": "ಪ್ರಾಥಮಿಕ ಬ್ಯಾಂಕ್ ಖಾತೆ ಸಂಖ್ಯೆ", "placeholder": "ಬ್ಯಾಂಕ್ ಖಾತೆ ಸಂಖ್ಯೆ"},
                            {"name": "bank_ifsc", "label": "ಬ್ಯಾಂಕ್ IFSC ಕೋಡ್", "placeholder": "ಉದಾ. PUNB0123400"},
                            {"name": "address", "label": "ಕುಟುಂಬದ ವಾಸಸ್ಥಳ ವಿಳಾಸ", "placeholder": "ಪೂರ್ಣ ವಿಳಾಸ"},
                            {"name": "declaration_consent", "label": "ಪಟ್ಟಿಯಲ್ಲಿರುವ ಕುಟುಂಬದ ಸದಸ್ಯರು ಮನೆಯ ಅವಲಂಬಿತ ನಿವಾಸಿಗಳಾಗಿದ್ದಾರೆ ಎಂದು ನಾನು ಘೋಷಿಸುತ್ತೇನೆ."}
                        ]
                    },
                    "hi": {
                        "title": "पारिवारिक स्वास्थ्य सहायता योजना",
                        "category": "स्वास्थ्य",
                        "short_description": "पात्र परिवारों के लिए स्वास्थ्य सेवा सहायता जानकारी।",
                        "description": "निर्धारित पात्रता शर्तों के आधार पर पात्र परिवारों को स्वास्थ्य संबंधी सहायता प्रदान करने वाली एक प्रदर्शन योजना।",
                        "eligibility": [
                            "आवेदक को लागू परिवार पात्रता मानदंडों को पूरा करना होगा।",
                            "आवेदक को वैध पहचान और निवास प्रमाण पत्र प्रदान करना होगा।",
                            "आय संबंधी शर्तें लागू हो सकती हैं।"
                        ],
                        "benefits": [
                            "स्वास्थ्य देखभाल सहायता।",
                            "पात्र चिकित्सा खर्चों के लिए सहायता।",
                            "लागू स्वास्थ्य सेवाओं तक पहुंच।"
                        ],
                        "documents": [
                            "पहचान प्रमाण",
                            "निवास प्रमाण",
                            "आय प्रमाण पत्र",
                            "पारिवारिक विवरण",
                            "बैंक खाता विवरण"
                        ],
                        "application_process": [
                            "पात्रता शर्तों की समीक्षा करें।",
                            "आवश्यक दस्तावेज एकत्र करें।",
                            "आवेदन भरें।",
                            "आवेदन जमा करें।",
                            "सत्यापन और प्रसंस्करण की प्रतीक्षा करें।"
                        ],
                        "application_fields": [
                            {"name": "applicant_name", "label": "परिवार के मुखिया / आवेदक का नाम", "placeholder": "परिवार के मुखिया का पूरा नाम"},
                            {"name": "dob", "label": "जन्म तिथि"},
                            {"name": "gender", "label": "लिंग", "options": ["पुरुष", "महिला", "अन्य"]},
                            {"name": "family_members_count", "label": "आश्रित परिवार के सदस्यों की संख्या", "placeholder": "उदा. 4"},
                            {"name": "ration_card_category", "label": "राशन कार्ड श्रेणी", "options": ["बीपीएल (गरीबी रेखा से नीचे)", "अंत्योदय अन्न", "एपीएल राशन कार्ड"]},
                            {"name": "annual_income", "label": "वार्षिक पारिवारिक आय (रु.)", "placeholder": "उदा. 180000"},
                            {"name": "coverage_preference", "label": "आवश्यक सहायता प्रकार", "options": ["अस्पताल में भर्ती सहायता", "ओपीडी पुरानी बीमारी देखभाल", "नैदानिक सहायता"]},
                            {"name": "bank_account_number", "label": "प्राथमिक बैंक खाता संख्या", "placeholder": "बैंक खाता संख्या दर्ज करें"},
                            {"name": "bank_ifsc", "label": "बैंक आईएफएससी कोड", "placeholder": "उदा. PUNB0123400"},
                            {"name": "address", "label": "पारिवारिक निवास का पता", "placeholder": "पूरा आवासीय पता"},
                            {"name": "declaration_consent", "label": "मैं घोषणा करता/करती हूँ कि सूचीबद्ध सदस्य परिवार के आश्रित निवासी हैं।"}
                        ]
                    }
                }
            },

            {
                "id": "pension-001",
                "category": "Pension",
                "title": "Senior Citizen Pension Scheme",
                "short_description": "Pension assistance information for eligible senior citizens.",
                "description": "This demonstration scheme provides information about pension assistance available to eligible senior citizens.",
                "eligibility": [
                    "Applicant must satisfy the prescribed age requirement.",
                    "Applicant must meet applicable income or social security conditions.",
                    "Applicant must be a resident citizen.",
                    "Required documents must be provided."
                ],
                "eligibility_rules": {
                    "min_age": 60,
                    "max_income": 300000
                },
                "benefits": [
                    "Regular pension assistance for eligible beneficiaries.",
                    "Financial support for senior citizens.",
                    "Support for basic living expenses."
                ],
                "documents": [
                    "Identity Proof",
                    "Age Proof",
                    "Residence Proof",
                    "Income Certificate",
                    "Bank Account Details"
                ],
                "application_fields": [
                    {
                        "name": "full_name",
                        "label": "Senior Citizen Applicant Full Name",
                        "type": "text",
                        "required": True,
                        "placeholder": "Full legal name as per Age/ID Proof"
                    },
                    {
                        "name": "dob",
                        "label": "Date of Birth (Must be 60 years or older)",
                        "type": "date",
                        "required": True
                    },
                    {
                        "name": "gender",
                        "label": "Gender",
                        "type": "select",
                        "required": True,
                        "options": ["Male", "Female", "Other"]
                    },
                    {
                        "name": "marital_status",
                        "label": "Marital Status",
                        "type": "select",
                        "required": True,
                        "options": ["Married", "Widowed", "Single / Unmarried", "Divorced"]
                    },
                    {
                        "name": "annual_income",
                        "label": "Current Annual Income from All Sources (INR)",
                        "type": "number",
                        "required": True,
                        "placeholder": "e.g. 60000"
                    },
                    {
                        "name": "disbursement_mode",
                        "label": "Preferred Pension Disbursement Channel",
                        "type": "radio",
                        "required": True,
                        "options": ["Direct Bank Transfer (DBT)", "Post Office Savings Bank (POSB)"]
                    },
                    {
                        "name": "bank_account_number",
                        "label": "Pension Bank / Post Office Account Number",
                        "type": "text",
                        "required": True,
                        "placeholder": "Active Savings Account Number"
                    },
                    {
                        "name": "bank_ifsc",
                        "label": "Branch IFSC / Postal Code",
                        "type": "text",
                        "required": True,
                        "placeholder": "e.g. IPOS0000001 or Bank IFSC"
                    },
                    {
                        "name": "nominee_name",
                        "label": "Nominee / Guardian Full Name",
                        "type": "text",
                        "required": True,
                        "placeholder": "Name of legal nominee"
                    },
                    {
                        "name": "address",
                        "label": "Permanent Address",
                        "type": "textarea",
                        "required": True,
                        "placeholder": "Full residential address with PIN Code"
                    },
                    {
                        "name": "declaration_consent",
                        "label": "I solemnly affirm that I am not drawing any other central/state government pension.",
                        "type": "checkbox",
                        "required": True
                    }
                ],
                "application_process": [
                    "Check the age and eligibility requirements.",
                    "Prepare the required documents.",
                    "Complete the application form.",
                    "Submit the application to the designated authority.",
                    "Track the application status."
                ],
                "translations": {
                    "kn": {
                        "title": "ಹಿರಿಯ ನಾಗರಿಕರ ಪಿಂಚಣಿ ಯೋಜನೆ",
                        "category": "ಪಿಂಚಣಿ",
                        "short_description": "ಅರ್ಹ ಹಿರಿಯ ನಾಗರಿಕರಿಗೆ ಮಾಸಿಕ ಪಿಂಚಣಿ ನೆರವು ಮಾಹಿತಿ.",
                        "description": "ಅರ್ಹ ಹಿರಿಯ ನಾಗರಿಕರಿಗೆ ಲಭ್ಯವಿರುವ ಪಿಂಚಣಿ ಸಹಾಯದ ಬಗ್ಗೆ ಮಾಹಿತಿಯನ್ನು ಒದಗಿಸುವ ಪ್ರದರ್ಶನ ಯೋಜನೆ.",
                        "eligibility": [
                            "ಅರ್ಜಿದಾರರು ನಿಗದಿತ ವಯಸ್ಸಿನ ಮಿತಿಯನ್ನು (೬೦ ವರ್ಷ ಅಥವಾ ಮೇಲ್ಪಟ್ಟು) ಪೂರೈಸಬೇಕು.",
                            "ಅರ್ಜಿದಾರರು ಅನ್ವಯವಾಗುವ ಆದಾಯ ಅಥವಾ ಸಾಮಾಜಿಕ ಭದ್ರತಾ ಷರತ್ತುಗಳನ್ನು ಪೂರೈಸಬೇಕು.",
                            "ಅರ್ಜಿದಾರರು ಭಾರತದ ನಿವಾಸಿ ನಾಗರಿಕರಾಗಿರಬೇಕು.",
                            "ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ಒದಗಿಸಬೇಕು."
                        ],
                        "benefits": [
                            "ಅರ್ಹ ಫಲಾನುಭವಿಗಳಿಗೆ ನಿಯಮಿತ ಮಾಸಿಕ ಪಿಂಚಣಿ ನೆರವು.",
                            "ಹಿರಿಯ ನಾಗರಿಕರಿಗೆ ಆರ್ಥಿಕ ಬೆಂಬಲ.",
                            "ಮೂಲ ಜೀವನ ವೆಚ್ಚಗಳಿಗೆ ಆಸರೆ."
                        ],
                        "documents": [
                            "ಗುರುತಿನ ಪುರಾವೆ",
                            "ವಯಸ್ಸಿನ ಪುರಾವೆ",
                            "ನಿವಾಸ ಪುರಾವೆ",
                            "ಆದಾಯ ಪ್ರಮಾಣಪತ್ರ",
                            "ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರಗಳು"
                        ],
                        "application_process": [
                            "ವಯಸ್ಸು ಮತ್ತು ಅರ್ಹತಾ ಮಾನದಂಡಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
                            "ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ಸಿದ್ಧಪಡಿಸಿ.",
                            "ಅರ್ಜಿ ನಮೂನೆಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ.",
                            "ಅರ್ಜಿಯನ್ನು ಸಲ್ಲಿಸಿ.",
                            "ಅರ್ಜಿಯ ಸ್ಥಿತಿಯನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಿ."
                        ],
                        "application_fields": [
                            {"name": "full_name", "label": "ಹಿರಿಯ ನಾಗರಿಕ ಅರ್ಜಿದಾರರ ಪೂರ್ಣ ಹೆಸರು", "placeholder": "ಗುರುತಿನ ಚೀಟಿಯ ಪ್ರಕಾರ ಕಾನೂನುಬದ್ಧ ಪೂರ್ಣ ಹೆಸರು"},
                            {"name": "dob", "label": "ಹುಟ್ಟಿದ ದಿನಾಂಕ (60 ವರ್ಷ ಅಥವಾ ಅದಕ್ಕಿಂತ ಹೆಚ್ಚು)"},
                            {"name": "gender", "label": "ಲಿಂಗ", "options": ["ಪುರುಷ", "ಮಹಿಳೆ", "ಇತರ"]},
                            {"name": "marital_status", "label": "ವೈವಾಹಿಕ ಸ್ಥಿತಿ", "options": ["ವಿವಾಹಿತ", "ವಿಧವೆ/ವಿಧುರ", "ಅವಿವಾಹಿತ", "ವಿಚ್ಛೇದಿತ"]},
                            {"name": "annual_income", "label": "ಎಲ್ಲಾ ಮೂಲಗಳಿಂದ ವಾರ್ಷಿಕ ಆದಾಯ (ರೂ.)", "placeholder": "ಉದಾ. 60000"},
                            {"name": "disbursement_mode", "label": "ಪಿಂಚಣಿ ವಿತರಣಾ ಮಾಧ್ಯಮ", "options": ["ನೇರ ಬ್ಯಾಂಕ್ ವರ್ಗಾವಣೆ (ಡಿಬಿಟಿ)", "ಅಂಚೆ ಕಚೇರಿ ಉಳಿತಾಯ ಬ್ಯಾಂಕ್"]},
                            {"name": "bank_account_number", "label": "ಪಿಂಚಣಿ ಬ್ಯಾಂಕ್ / ಅಂಚೆ ಖಾತೆ ಸಂಖ್ಯೆ", "placeholder": "ಖಾತೆ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ"},
                            {"name": "bank_ifsc", "label": "ಶಾಖೆಯ IFSC / ಅಂಚೆ ಕೋಡ್", "placeholder": "ಉದಾ. IPOS0000001"},
                            {"name": "nominee_name", "label": "ನಾಮಿನಿ / ಪೋಷಕರ ಪೂರ್ಣ ಹೆಸರು", "placeholder": "ನಾಮಿನಿಯ ಹೆಸರು"},
                            {"name": "address", "label": "ಶಾಶ್ವತ ವಸತಿ ವಿಳಾಸ", "placeholder": "ಪಿನ್‌ಕೋಡ್‌ನೊಂದಿಗೆ ಪೂರ್ಣ ವಿಳಾಸ"},
                            {"name": "declaration_consent", "label": "ನಾನು ಯಾವುದೇ ಇತರ ಸರ್ಕಾರಿ ಪಿಂಚಣಿಯನ್ನು ಪಡೆಯುತ್ತಿಲ್ಲ ಎಂದು ನಾನು ದೃಢೀಕರಿಸುತ್ತೇನೆ."}
                        ]
                    },
                    "hi": {
                        "title": "वरिष्ठ नागरिक पेंशन योजना",
                        "category": "पेंशन",
                        "short_description": "पात्र वरिष्ठ नागरिकों के लिए पेंशन सहायता जानकारी।",
                        "description": "यह प्रदर्शन योजना पात्र वरिष्ठ नागरिकों के लिए उपलब्ध पेंशन सहायता के बारे में जानकारी प्रदान करती है।",
                        "eligibility": [
                            "आवेदक को निर्धारित आयु आवश्यकता (60 वर्ष या अधिक) को पूरा करना होगा।",
                            "आवेदक को लागू आय या सामाजिक सुरक्षा शर्तों को पूरा करना होगा।",
                            "आवेदक निवासी नागरिक होना चाहिए।",
                            "आवश्यक दस्तावेज उपलब्ध कराए जाने चाहिए।"
                        ],
                        "benefits": [
                            "पात्र लाभार्थियों के लिए नियमित मासिक पेंशन सहायता।",
                            "वरिष्ठ नागरिकों के लिए वित्तीय सहायता।",
                            "बुनियादी जीवन यापन के खर्चों के लिए सहायता।"
                        ],
                        "documents": [
                            "पहचान प्रमाण",
                            "आयु प्रमाण",
                            "निवास प्रमाण",
                            "आय प्रमाण पत्र",
                            "बैंक खाता विवरण"
                        ],
                        "application_process": [
                            "आयु और पात्रता आवश्यकताओं की जाँच करें।",
                            "आवश्यक दस्तावेज तैयार करें।",
                            "आवेदन पत्र भरें।",
                            "आवेदन जमा करें।",
                            "आवेदन की स्थिति को ट्रैक करें।"
                        ],
                        "application_fields": [
                            {"name": "full_name", "label": "वरिष्ठ नागरिक आवेदक का पूरा नाम", "placeholder": "पहचान पत्र के अनुसार पूरा नाम"},
                            {"name": "dob", "label": "जन्म तिथि (60 वर्ष या अधिक होनी चाहिए)"},
                            {"name": "gender", "label": "लिंग", "options": ["पुरुष", "महिला", "अन्य"]},
                            {"name": "marital_status", "label": "वैवाहिक स्थिति", "options": ["विवाहित", "विधवा / विधुर", "अविवाहित", "तलाकशुदा"]},
                            {"name": "annual_income", "label": "सभी स्रोतों से वर्तमान वार्षिक आय (रु.)", "placeholder": "उदा. 60000"},
                            {"name": "disbursement_mode", "label": "पेंशन भुगतान का पसंदीदा माध्यम", "options": ["प्रत्यक्ष बैंक अंतरण (डीबीटी)", "डाकघर बचत बैंक"]},
                            {"name": "bank_account_number", "label": "पेंशन बैंक / डाकघर खाता संख्या", "placeholder": "खाता संख्या दर्ज करें"},
                            {"name": "bank_ifsc", "label": "शाखा आईएफएससी / पोस्टल कोड", "placeholder": "उदा. IPOS0000001"},
                            {"name": "nominee_name", "label": "नॉमिनी / अभिभावक का पूरा नाम", "placeholder": "नॉमिनी का नाम"},
                            {"name": "address", "label": "स्थायी निवास का पता", "placeholder": "पिन कोड सहित पूरा पता"},
                            {"name": "declaration_consent", "label": "मैं सत्यनिष्ठा से प्रतिज्ञा करता/करती हूँ कि मैं कोई अन्य सरकारी पेंशन प्राप्त नहीं कर रहा/रही हूँ।"}
                        ]
                    }
                }
            },

            {
                "id": "pension-002",
                "category": "Pension",
                "title": "Social Security Pension Assistance",
                "short_description": "Social security pension information for eligible beneficiaries.",
                "description": "A demonstration scheme covering pension-related assistance for eligible citizens under applicable social security conditions.",
                "eligibility": [
                    "Applicant must satisfy the applicable eligibility conditions.",
                    "Applicant must provide identity and residence proof.",
                    "Income or household conditions may apply."
                ],
                "eligibility_rules": {
                    "min_age": 60
                },
                "benefits": [
                    "Periodic financial assistance.",
                    "Social security support.",
                    "Financial assistance for eligible beneficiaries."
                ],
                "documents": [
                    "Identity Proof",
                    "Residence Proof",
                    "Income Certificate",
                    "Bank Account Details",
                    "Age Proof, where applicable"
                ],
                "application_fields": [
                    {
                        "name": "full_name",
                        "label": "Beneficiary Full Name",
                        "type": "text",
                        "required": True,
                        "placeholder": "Name as per Aadhaar / Voter ID"
                    },
                    {
                        "name": "dob",
                        "label": "Date of Birth",
                        "type": "date",
                        "required": True
                    },
                    {
                        "name": "gender",
                        "label": "Gender",
                        "type": "select",
                        "required": True,
                        "options": ["Male", "Female", "Other"]
                    },
                    {
                        "name": "assistance_category",
                        "label": "Social Security Category",
                        "type": "select",
                        "required": True,
                        "options": ["Old Age Assistance", "Disability Welfare Assistance", "Destitute / Widow Assistance", "Special Care Support"]
                    },
                    {
                        "name": "annual_income",
                        "label": "Annual Household Income (INR)",
                        "type": "number",
                        "required": True,
                        "placeholder": "e.g. 45000"
                    },
                    {
                        "name": "disability_details",
                        "label": "Disability / Special Needs Details (if applicable)",
                        "type": "text",
                        "required": False,
                        "placeholder": "Optional: Specify type or percentage if applicable"
                    },
                    {
                        "name": "bank_account_number",
                        "label": "Bank Account Number",
                        "type": "text",
                        "required": True,
                        "placeholder": "Account number for monthly pension credit"
                    },
                    {
                        "name": "bank_ifsc",
                        "label": "Bank IFSC Code",
                        "type": "text",
                        "required": True,
                        "placeholder": "e.g. BARB0KOLKAT"
                    },
                    {
                        "name": "address",
                        "label": "Current Residential Address",
                        "type": "textarea",
                        "required": True,
                        "placeholder": "Complete living address"
                    },
                    {
                        "name": "declaration_consent",
                        "label": "I verify that the above information is correct and I meet the social security criteria.",
                        "type": "checkbox",
                        "required": True
                    }
                ],
                "application_process": [
                    "Check eligibility.",
                    "Prepare the required documents.",
                    "Submit the application.",
                    "Complete verification.",
                    "Receive the decision from the concerned authority."
                ],
                "translations": {
                    "kn": {
                        "title": "ಸಾಮಾಜಿಕ ಭದ್ರತಾ ಪಿಂಚಣಿ ನೆರವು ಯೋಜನೆ",
                        "category": "ಪಿಂಚಣಿ",
                        "short_description": "ಅರ್ಹ ಫಲಾನುಭವಿಗಳಿಗೆ ಸಾಮಾಜಿಕ ಭದ್ರತಾ ಪಿಂಚಣಿ ಮಾಹಿತಿ ಮತ್ತು ಆರ್ಥಿಕ ನೆರವು.",
                        "description": "ಅನ್ವಯವಾಗುವ ಸಾಮಾಜಿಕ ಭದ್ರತಾ ಷರತ್ತುಗಳ ಅಡಿಯಲ್ಲಿ ಅರ್ಹ ನಾಗರಿಕರಿಗೆ ಪಿಂಚಣಿ ನೆರವನ್ನು ಒದಗಿಸುವ ಪ್ರದರ್ಶನ ಯೋಜನೆ.",
                        "eligibility": [
                            "ಅರ್ಜಿದಾರರು ಅನ್ವಯವಾಗುವ ಅರ್ಹತಾ ಷರತ್ತುಗಳನ್ನು ಪೂರೈಸಬೇಕು.",
                            "ಅರ್ಜಿದಾರರು ಗುರುತು ಮತ್ತು ವಾಸಸ್ಥಳದ ಪುರಾವೆಗಳನ್ನು ಒದಗಿಸಬೇಕು.",
                            "ಆದಾಯ ಅಥವಾ ಕುಟುಂಬದ ಷರತ್ತುಗಳು ಅನ್ವಯಿಸಬಹುದು."
                        ],
                        "benefits": [
                            "ನಿಯಮಿತ ಆರ್ಥಿಕ ನೆರವು.",
                            "ಸಾಮಾಜಿಕ ಭದ್ರತಾ ಬೆಂಬಲ.",
                            "ಅರ್ಹ ಫಲಾನುಭವಿಗಳಿಗೆ ಮಾಸಿಕ ಆರ್ಥಿಕ ಆಸರೆ."
                        ],
                        "documents": [
                            "ಗುರುತಿನ ಪುರಾವೆ",
                            "ನಿವಾಸ ಪುರಾವೆ",
                            "ಆದಾಯ ಪ್ರಮಾಣಪತ್ರ",
                            "ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರಗಳು",
                            "ವಯಸ್ಸಿನ ಪುರಾವೆ (ಅನ್ವಯಿಸಿದಲ್ಲಿ)"
                        ],
                        "application_process": [
                            "ಅರ್ಹತೆಯನ್ನು ಪರಿಶೀಲಿಸಿ.",
                            "ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ಸಿದ್ಧಪಡಿಸಿ.",
                            "ಅರ್ಜಿಯನ್ನು ಸಲ್ಲಿಸಿ.",
                            "ಪರಿಶೀಲನೆಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ.",
                            "ಸಂಬಂಧಪಟ್ಟ ಪ್ರಾಧಿಕಾರದಿಂದ ನಿರ್ಧಾರವನ್ನು ಸ್ವೀಕರಿಸಿ."
                        ],
                        "application_fields": [
                            {"name": "full_name", "label": "ಫಲಾನುಭವಿಯ ಪೂರ್ಣ ಹೆಸರು", "placeholder": "ಗುರುತಿನ ಚೀಟಿಯ ಪ್ರಕಾರ ಹೆಸರು"},
                            {"name": "dob", "label": "ಹುಟ್ಟಿದ ದಿನಾಂಕ"},
                            {"name": "gender", "label": "ಲಿಂಗ", "options": ["ಪುರುಷ", "ಮಹಿಳೆ", "ಇತರ"]},
                            {"name": "assistance_category", "label": "ಸಾಮಾಜಿಕ ಭದ್ರತಾ ವರ್ಗ", "options": ["ವೃದ್ಧಾಪ್ಯ ನೆರವು", "ಅಂಗವಿಕಲರ ಕಲ್ಯಾಣ ನೆರವು", "ನಿರಾಶ್ರಿತ / ವಿಧವಾ ನೆರವು", "ವಿಶೇಷ ಆರೈಕೆ"]},
                            {"name": "annual_income", "label": "ವಾರ್ಷಿಕ ಕುಟುಂಬ ಆದಾಯ (ರೂ.)", "placeholder": "ಉದಾ. 45000"},
                            {"name": "disability_details", "label": "ಅಂಗವೈಕಲ್ಯ / ವಿಶೇಷ ಅಗತ್ಯಗಳ ವಿವರಗಳು", "placeholder": "ಅನ್ವಯಿಸಿದಲ್ಲಿ ವಿವರ ತಿಳಿಸಿ"},
                            {"name": "bank_account_number", "label": "ಬ್ಯಾಂಕ್ ಖಾತೆ ಸಂಖ್ಯೆ", "placeholder": "ಮಾಸಿಕ ಪಿಂಚಣಿಗಾಗಿ ಖಾತೆ ಸಂಖ್ಯೆ"},
                            {"name": "bank_ifsc", "label": "ಬ್ಯಾಂಕ್ IFSC ಕೋಡ್", "placeholder": "ಉದಾ. BARB0KOLKAT"},
                            {"name": "address", "label": "ಪ್ರಸ್ತುತ ವಸತಿ ವಿಳಾಸ", "placeholder": "ಸಂಪೂರ್ಣ ವಸತಿ ವಿಳಾಸ"},
                            {"name": "declaration_consent", "label": "ಮೇಲಿನ ಮಾಹಿತಿಯು ಸರಿಯಾಗಿದೆ ಮತ್ತು ನಾನು ಸಾಮಾಜಿಕ ಭದ್ರತಾ ಮಾನದಂಡಗಳನ್ನು ಪೂರೈಸುತ್ತೇನೆ ಎಂದು ದೃಢೀಕರಿಸುತ್ತೇನೆ."}
                        ]
                    },
                    "hi": {
                        "title": "सामाजिक सुरक्षा पेंशन सहायता योजना",
                        "category": "पेंशन",
                        "short_description": "पात्र लाभार्थियों के लिए सामाजिक सुरक्षा पेंशन जानकारी और वित्तीय सहायता।",
                        "description": "लागू सामाजिक सुरक्षा शर्तों के तहत पात्र नागरिकों के लिए पेंशन संबंधी सहायता को कवर करने वाली एक प्रदर्शन योजना।",
                        "eligibility": [
                            "आवेदक को लागू पात्रता शर्तों को पूरा करना होगा।",
                            "आवेदक को पहचान और निवास प्रमाण पत्र प्रदान करना होगा।",
                            "आय या पारिवारिक शर्तें लागू हो सकती हैं।"
                        ],
                        "benefits": [
                            "आवधिक वित्तीय सहायता।",
                            "सामाजिक सुरक्षा समर्थन।",
                            "पात्र लाभार्थियों के लिए वित्तीय सहायता।"
                        ],
                        "documents": [
                            "पहचान प्रमाण",
                            "निवास प्रमाण",
                            "आय प्रमाण पत्र",
                            "बैंक खाता विवरण",
                            "आयु प्रमाण (जहां लागू हो)"
                        ],
                        "application_process": [
                            "पात्रता की जाँच करें।",
                            "आवश्यक दस्तावेज तैयार करें।",
                            "आवेदन जमा करें।",
                            "सत्यापन पूरा करें।",
                            "संबंधित प्राधिकरण से निर्णय प्राप्त करें।"
                        ],
                        "application_fields": [
                            {"name": "full_name", "label": "लाभार्थी का पूरा नाम", "placeholder": "पहचान पत्र के अनुसार नाम"},
                            {"name": "dob", "label": "जन्म तिथि"},
                            {"name": "gender", "label": "लिंग", "options": ["पुरुष", "महिला", "अन्य"]},
                            {"name": "assistance_category", "label": "सामाजिक सुरक्षा श्रेणी", "options": ["वृद्धावस्था सहायता", "दिव्यांग कल्याण सहायता", "निराश्रित / विधवा सहायता", "विशेष देखभाल सहायता"]},
                            {"name": "annual_income", "label": "वार्षिक पारिवारिक आय (रु.)", "placeholder": "उदा. 45000"},
                            {"name": "disability_details", "label": "दिव्यांगता / विशेष आवश्यकता विवरण", "placeholder": "वैकल्पिक: यदि लागू हो तो प्रकार या प्रतिशत बताएं"},
                            {"name": "bank_account_number", "label": "बैंक खाता संख्या", "placeholder": "मासिक पेंशन क्रेडिट के लिए खाता संख्या"},
                            {"name": "bank_ifsc", "label": "बैंक आईएफएससी कोड", "placeholder": "उदा. BARB0KOLKAT"},
                            {"name": "address", "label": "वर्तमान निवास का पता", "placeholder": "पूरा आवासीय पता"},
                            {"name": "declaration_consent", "label": "मैं सत्यापित करता/करती हूँ कि उपरोक्त जानकारी सही है और मैं सामाजिक सुरक्षा मानदंडों को पूरा करता/करती हूँ।"}
                        ]
                    }
                }
            }
        ]

        for data in schemes:
            scheme, created = Scheme.objects.update_or_create(
                id=data["id"],
                defaults=data
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {scheme.title}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Updated: {scheme.title}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "\nScheme database seeding completed with multilingual translations."
            )
        )