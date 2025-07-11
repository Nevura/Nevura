import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import en from '../i18n/en.json';
import fr from '../i18n/fr.json';
import es from '../i18n/es.json';
import de from '../i18n/de.json';
import ko from '../i18n/ko.json';
import it from '../i18n/it.json';
import jpn from '../i18n/jpn.json';
import ru from '../i18n/ru.json';
import po from '../i18n/po.json';

const resources = {
  en: { translation: English },
  fr: { translation: Français },
  es: { translation: Español },
  de: { translation: Deutsch },
  ko: { translation: 한국인 },
  it: { translation: Italiano },
  jpn: { translation: 日本語 },
  ru: { translation: Русский },
  po: { translation: Português }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'fr',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
