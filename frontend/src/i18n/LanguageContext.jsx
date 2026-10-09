import { createContext, useContext, useEffect, useState } from "react";
import en from "./en";
import kn from "./kn";
import hi from "./hi";

const dictionaries = { en, kn, hi };

export const LanguageContext = createContext({
  language: "en",
  setLanguage: () => {},
  t: (key) => key,
  getLocalizedScheme: (scheme) => scheme,
});

export function LanguageProvider({ children }) {
  const [language, setLanguageState] = useState(() => {
    try {
      const saved = localStorage.getItem("portal_language");
      if (saved && ["en", "kn", "hi"].includes(saved)) {
        return saved;
      }
    } catch {
      // ignore
    }
    return "en";
  });

  const setLanguage = (newLang) => {
    if (!["en", "kn", "hi"].includes(newLang)) return;
    setLanguageState(newLang);
    try {
      localStorage.setItem("portal_language", newLang);
    } catch {
      // ignore
    }
    document.documentElement.lang = newLang;
  };

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  const t = (path, fallback = "") => {
    if (!path) return "";
    const keys = path.split(".");

    // Look up in active language
    let cur = dictionaries[language];
    for (const k of keys) {
      if (cur && typeof cur === "object" && k in cur) {
        cur = cur[k];
      } else {
        cur = undefined;
        break;
      }
    }

    if (cur !== undefined && typeof cur === "string") {
      return cur;
    }

    // Fallback to English dictionary
    if (language !== "en") {
      let fallbackCur = dictionaries.en;
      for (const k of keys) {
        if (fallbackCur && typeof fallbackCur === "object" && k in fallbackCur) {
          fallbackCur = fallbackCur[k];
        } else {
          fallbackCur = undefined;
          break;
        }
      }
      if (fallbackCur !== undefined && typeof fallbackCur === "string") {
        return fallbackCur;
      }
    }

    return fallback || path;
  };

  const getLocalizedScheme = (scheme) => {
    if (!scheme) return scheme;
    if (language === "en") return scheme;

    const tr = scheme.translations?.[language];
    if (!tr) return scheme;

    // Overlay translated scheme attributes
    return {
      ...scheme,
      title: tr.title || scheme.title,
      category: tr.category || scheme.category,
      short_description: tr.short_description || scheme.short_description,
      description: tr.description || scheme.description,
      eligibility: tr.eligibility || scheme.eligibility,
      benefits: tr.benefits || scheme.benefits,
      documents: tr.documents || scheme.documents,
      application_process: tr.application_process || scheme.application_process,
      application_fields: tr.application_fields && tr.application_fields.length > 0
        ? tr.application_fields.map((trField) => {
            const orig = scheme.application_fields?.find((f) => f.name === trField.name) || {};
            return {
              ...orig,
              ...trField,
            };
          })
        : scheme.application_fields,
    };
  };

  return (
    <LanguageContext.Provider
      value={{
        language,
        setLanguage,
        t,
        getLocalizedScheme,
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
}

export function useTranslation() {
  return useContext(LanguageContext);
}
