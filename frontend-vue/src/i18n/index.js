import { createI18n } from 'vue-i18n'
import fr from './locales/fr.js'
import en from './locales/en.js'
import uk from './locales/uk.js'
import de from './locales/de.js'
import pl from './locales/pl.js'

const messages = {
  fr,
  en,
  uk,
  de,
  pl
}

// Détection automatique de la langue
function getDefaultLocale() {
  const savedLocale = localStorage.getItem('locale')
  if (savedLocale && messages[savedLocale]) {
    return savedLocale
  }
  
  const browserLocale = navigator.language.split('-')[0]
  if (messages[browserLocale]) {
    return browserLocale
  }
  
  return 'fr' // Langue par défaut
}

const i18n = createI18n({
  legacy: false, // Utiliser l'API Composition
  locale: getDefaultLocale(),
  fallbackLocale: 'fr',
  messages,
  globalInjection: true,
  silentTranslationWarn: true,
  allowComposition: true
})

// Fonction pour changer de langue
export function setLocale(locale) {
  if (messages[locale]) {
    i18n.global.locale.value = locale
    localStorage.setItem('locale', locale)
    document.documentElement.lang = locale
    // Forcer la mise à jour de l'interface
    window.dispatchEvent(new CustomEvent('localeChanged', { detail: { locale } }))
    // Forcer le re-render de l'application
    if (window.location) {
      window.location.reload()
    }
  }
}

// Fonction pour obtenir la langue actuelle
export function getCurrentLocale() {
  return i18n.global.locale.value
}

// Fonction pour obtenir toutes les langues disponibles
export function getAvailableLocales() {
  return Object.keys(messages).map(code => ({
    code,
    name: messages[code].meta.languageName,
    nativeName: messages[code].meta.nativeName,
    flag: messages[code].meta.flag
  }))
}

export default i18n 