<template>
  <nav class="navbar" :class="{ 'navbar-scrolled': isScrolled }">
    <!-- Effet de fond avec particules -->
    <div class="navbar-background">
      <div class="bg-particles">
        <div v-for="i in 20" :key="i" class="particle" :style="getParticleStyle(i)"></div>
      </div>
      <div class="bg-gradient"></div>
    </div>

    <!-- Livres flottants dans la navbar -->
    <div class="floating-books-nav">
      <div v-for="i in 5" :key="i" class="nav-book" :style="getNavBookStyle(i)">
        <div class="book-cover-nav"></div>
        <div class="book-pages-nav"></div>
      </div>
    </div>

    <div class="navbar-container">
      <!-- Logo officiel de l'association -->
      <div class="logo-container">
        <div class="logo-image">
          <img src="/images/logo-main.png" alt="Les Lumières d'Ukraine" class="logo-svg" />
        </div>
        <div class="logo-glow"></div>
      </div>

      <!-- Navigation principale -->
      <div class="nav-links" :class="{ 'nav-open': isMenuOpen }">
        <router-link 
          v-for="link in navLinks" 
          :key="link.path"
          :to="link.path"
          class="nav-link"
          :class="{ 'active': $route.path === link.path }"
        >
          <span class="link-icon">{{ link.icon }}</span>
          <span class="link-text">{{ link.name }}</span>
          <div class="link-hover-effect"></div>
        </router-link>
      </div>

      <!-- Sélecteur de langue premium -->
      <div class="language-selector">
        <div class="selector-container" @click="toggleLanguageMenu">
          <div class="current-language">
            <span class="flag">{{ currentLanguage.flag }}</span>
            <span class="code">{{ currentLanguage.code.toUpperCase() }}</span>
            <span class="arrow" :class="{ 'rotated': isLanguageMenuOpen }">▼</span>
          </div>
          <div class="language-dropdown" :class="{ 'open': isLanguageMenuOpen }">
            <div 
              v-for="lang in languages" 
              :key="lang.code"
              class="language-option"
              @click="selectLanguage(lang)"
            >
              <span class="flag">{{ lang.flag }}</span>
              <div class="name">{{ lang.name }}</div>
              <div class="native-name">{{ lang.nativeName }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Bouton menu mobile -->
      <button class="mobile-menu-btn" @click="toggleMenu">
        <div class="hamburger" :class="{ 'active': isMenuOpen }">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </button>
    </div>

    <!-- Menu mobile overlay -->
    <div class="mobile-overlay" :class="{ 'open': isMenuOpen }" @click="closeMenu">
      <div class="mobile-menu" @click.stop>
        <div class="mobile-header">
          <div class="mobile-logo">
            <span class="logo-icon">🇺🇦</span>
            <span class="logo-text">Lumières d'Ukraine</span>
          </div>
          <button class="close-btn" @click="closeMenu">×</button>
        </div>
        <div class="mobile-links">
          <router-link 
            v-for="link in navLinks" 
            :key="link.path"
            :to="link.path"
            class="mobile-link"
            @click="closeMenu"
          >
            <span class="link-icon">{{ link.icon }}</span>
            <span class="link-text">{{ link.name }}</span>
          </router-link>
        </div>
        <div class="mobile-language">
          <div class="mobile-lang-title">{{ t('nav.selectLanguage') }}</div>
          <div class="mobile-lang-options">
            <div 
              v-for="lang in languages" 
              :key="lang.code"
              class="mobile-lang-option"
              @click="selectLanguage(lang); closeMenu()"
            >
              <span class="flag">{{ lang.flag }}</span>
              <span class="name">{{ lang.nativeName }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { getAvailableLocales, setLocale, getCurrentLocale } from '@/i18n'

const { t, locale } = useI18n()

const isScrolled = ref(false)
const isMenuOpen = ref(false)
const isLanguageMenuOpen = ref(false)
const forceUpdate = ref(0) // Variable pour forcer la mise à jour

const languages = computed(() => getAvailableLocales())

const currentLanguage = computed(() => {
  const current = getCurrentLocale()
  return languages.value.find(lang => lang.code === current) || languages.value[0]
})

const navLinks = ref([
  { name: t('nav.home'), path: '/', icon: '🏠' },
  { name: t('nav.books'), path: '/books', icon: '📚' },
  { name: t('nav.events'), path: '/events', icon: '🎭' },
  { name: t('nav.association'), path: '/association', icon: '🤝' },
  { name: t('nav.membership'), path: '/membership', icon: '🪪' },
  { name: t('nav.chatbot'), path: '/chatbot', icon: '🤖' }
])

// Fonction pour mettre à jour les liens de navigation
const updateNavLinks = () => {
  navLinks.value = [
    { name: t('nav.home'), path: '/', icon: '🏠' },
    { name: t('nav.books'), path: '/books', icon: '📚' },
    { name: t('nav.events'), path: '/events', icon: '🎭' },
    { name: t('nav.association'), path: '/association', icon: '🤝' },
    { name: t('nav.membership'), path: '/membership', icon: '🪪' },
    { name: t('nav.chatbot'), path: '/chatbot', icon: '🤖' }
  ]
}

// Écouter les changements de langue
watch(locale, (newLocale) => {
  console.log('Langue changée vers:', newLocale)
  forceUpdate.value++ // Forcer la mise à jour
  updateNavLinks() // Mettre à jour les liens de navigation
})

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
  
  // Fermer le dropdown de langue lors du défilement
  if (isLanguageMenuOpen.value) {
    isLanguageMenuOpen.value = false
  }
}

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
  isLanguageMenuOpen.value = false
}

const closeMenu = () => {
  isMenuOpen.value = false
}

const toggleLanguageMenu = () => {
  console.log('toggleLanguageMenu appelée')
  console.log('État actuel:', isLanguageMenuOpen.value)
  isLanguageMenuOpen.value = !isLanguageMenuOpen.value
  console.log('Nouvel état:', isLanguageMenuOpen.value)
  
  // Positionner le dropdown dynamiquement
  if (isLanguageMenuOpen.value) {
    nextTick(() => {
      const selector = document.querySelector('.language-selector')
      const dropdown = document.querySelector('.language-dropdown')
      if (selector && dropdown) {
        const rect = selector.getBoundingClientRect()
        const navbarHeight = 80 // Hauteur de la navbar
        const scrollY = window.scrollY
        
        // Calculer la position optimale
        const topPosition = rect.bottom + 10
        const rightPosition = window.innerWidth - rect.right
        
        // Vérifier si le dropdown dépasse le bas de l'écran
        const dropdownHeight = 300 // Hauteur maximale du dropdown
        const viewportHeight = window.innerHeight
        const spaceBelow = viewportHeight - topPosition
        
        if (spaceBelow < dropdownHeight) {
          // Positionner au-dessus du sélecteur si pas assez d'espace en dessous
          dropdown.style.top = `${rect.top - dropdownHeight - 10}px`
        } else {
          // Positionner en dessous du sélecteur
          dropdown.style.top = `${topPosition}px`
        }
        
        dropdown.style.right = `${rightPosition}px`
      }
    })
  }
}

const selectLanguage = (lang) => {
  console.log('Changement de langue vers:', lang.code)
  setLocale(lang.code)
  isLanguageMenuOpen.value = false
  
  // Forcer la mise à jour de l'interface
  nextTick(() => {
    updateNavLinks()
    forceUpdate.value++
  })
}

const getParticleStyle = (index) => {
  const size = Math.random() * 3 + 1
  const x = Math.random() * 100
  const y = Math.random() * 100
  const delay = Math.random() * 5
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${x}%`,
    top: `${y}%`,
    animationDelay: `${delay}s`
  }
}

const getNavBookStyle = (index) => {
  const x = Math.random() * 100
  const y = Math.random() * 100
  const rotation = Math.random() * 360
  const delay = Math.random() * 8
  return {
    left: `${x}%`,
    top: `${y}%`,
    transform: `rotate(${rotation}deg)`,
    animationDelay: `${delay}s`
  }
}

const startParticleAnimation = () => {
  setInterval(() => {
    document.querySelectorAll('.bg-particles .particle').forEach(particle => {
      const x = Math.random() * 100
      const y = Math.random() * 100
      particle.style.transform = `translate(${x}px, ${y}px)`
    })
  }, 3000)
}

const startBookAnimation = () => {
  setInterval(() => {
    document.querySelectorAll('.floating-books-nav .nav-book').forEach(book => {
      const rotation = Math.random() * 360
      const scale = 0.8 + Math.random() * 0.4
      book.style.transform = `rotate(${rotation}deg) scale(${scale})`
    })
  }, 5000)
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  startParticleAnimation()
  startBookAnimation()
  
  // Gestionnaire de clic global pour fermer le dropdown de langue
  document.addEventListener('click', (event) => {
    const languageSelector = document.querySelector('.language-selector')
    if (languageSelector && !languageSelector.contains(event.target)) {
      isLanguageMenuOpen.value = false
    }
  })
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
  // Nettoyer le gestionnaire de clic global
  document.removeEventListener('click', (event) => {
    const languageSelector = document.querySelector('.language-selector')
    if (languageSelector && !languageSelector.contains(event.target)) {
      isLanguageMenuOpen.value = false
    }
  })
})
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  transition: all 0.4s ease;
  height: 80px;
  overflow: hidden;
}

.navbar-scrolled {
  background: rgba(30, 60, 114, 0.95);
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  height: 70px;
}

/* Fond avec particules */
.navbar-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.bg-particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  animation: particleFloat 8s ease-in-out infinite;
  pointer-events: none;
}

@keyframes particleFloat {
  0%, 100% { transform: translateY(0px) scale(1); opacity: 0.3; }
  50% { transform: translateY(-15px) scale(1.2); opacity: 0.8; }
}

.bg-gradient {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, 
    rgba(30, 60, 114, 0.9) 0%, 
    rgba(42, 82, 152, 0.8) 50%, 
    rgba(0, 86, 179, 0.9) 100%);
}

/* Livres flottants dans la navbar */
.floating-books-nav {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

.nav-book {
  position: absolute;
  width: 30px;
  height: 40px;
  animation: navBookFloat 10s ease-in-out infinite;
  opacity: 0.6;
}

.book-cover-nav {
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  border-radius: 2px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  position: relative;
}

.book-pages-nav {
  position: absolute;
  top: 1px;
  left: 1px;
  right: 1px;
  bottom: 1px;
  background: white;
  border-radius: 1px;
}

@keyframes navBookFloat {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(3deg); }
}

.navbar-container {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 1rem;
  height: 100%;
  gap: 1rem;
}

/* Logo officiel de l'association */
.logo-container {
  display: flex;
  align-items: center;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 25px;
  padding: 0.75rem 1.5rem;
}

.logo-container:hover {
  transform: scale(1.05);
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.logo-image {
  height: 50px;
  width: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 15px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logo-svg {
  height: 100%;
  width: auto;
  max-width: 130px;
  object-fit: contain;
  filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.15));
  transition: all 0.3s ease;
}

.logo-container:hover .logo-svg {
  filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.4));
}

.logo-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.3) 0%, transparent 70%);
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.logo-container:hover .logo-glow {
  opacity: 1;
}

/* Navigation principale */
.nav-links {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
  justify-content: center;
  flex-wrap: wrap;
}

.nav-link {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: white;
  text-decoration: none;
  font-weight: 600;
  padding: 0.75rem 1rem;
  border-radius: 25px;
  transition: all 0.3s ease;
  overflow: hidden;
  white-space: nowrap;
  min-width: fit-content;
}

.nav-link:hover,
.nav-link.active {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  transform: translateY(-2px);
}

.link-icon {
  font-size: 1.1rem;
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.nav-link:hover .link-icon {
  transform: scale(1.2);
}

.link-text {
  font-size: 0.9rem;
  transition: color 0.3s ease;
  white-space: nowrap;
}

.nav-link.active .link-text {
  color: #ffd700;
}

.link-hover-effect {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.nav-link:hover .link-hover-effect {
  left: 100%;
}

/* Sélecteur de langue premium */
.language-selector {
  position: relative;
  z-index: 1001;
}

.selector-container {
  position: relative;
  cursor: pointer;
}

.current-language {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 25px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
}

.current-language:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.flag {
  font-size: 1.2rem;
}

.code {
  font-size: 0.9rem;
}

.arrow {
  font-size: 0.8rem;
  transition: transform 0.3s ease;
}

.arrow.rotated {
  transform: rotate(180deg);
}

.language-dropdown {
  position: fixed;
  background: rgba(30, 60, 114, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden;
  transform: translateY(-20px) scale(0.95);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  min-width: 200px;
  z-index: 10000;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  max-height: 300px;
  overflow-y: auto;
}

.language-dropdown.open {
  transform: translateY(0) scale(1);
  opacity: 1;
  visibility: visible;
}

.language-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  color: white;
  text-decoration: none;
  transition: all 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.language-option:last-child {
  border-bottom: none;
}

.language-option:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(5px);
}

.language-option .flag {
  font-size: 1.2rem;
}

.language-option .name {
  font-weight: 600;
  flex: 1;
}

.language-option .native-name {
  font-size: 0.8rem;
  opacity: 0.8;
}

/* Bouton menu mobile */
.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.hamburger {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 24px;
  height: 20px;
  position: relative;
}

.hamburger span {
  width: 100%;
  height: 2px;
  background: white;
  border-radius: 2px;
  transition: all 0.3s ease;
  transform-origin: center;
}

.hamburger.active span:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.hamburger.active span:nth-child(2) {
  opacity: 0;
}

.hamburger.active span:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

/* Menu mobile overlay */
.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  z-index: 999;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.mobile-overlay.open {
  opacity: 1;
  visibility: visible;
}

.mobile-menu {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  max-width: 400px;
  height: 100vh;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  padding: 2rem;
  transform: translateX(100%);
  transition: transform 0.3s ease;
  overflow-y: auto;
}

.mobile-overlay.open .mobile-menu {
  transform: translateX(0);
}

.mobile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 3rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.mobile-logo {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: white;
}

.mobile-logo .logo-icon {
  font-size: 2rem;
}

.mobile-logo .logo-text {
  font-size: 1.2rem;
  font-weight: 700;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.mobile-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 3rem;
}

.mobile-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  color: white;
  text-decoration: none;
  font-weight: 600;
  border-radius: 15px;
  transition: all 0.3s ease;
}

.mobile-link:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(10px);
}

.mobile-link .link-icon {
  font-size: 1.5rem;
}

.mobile-language {
  color: white;
}

.mobile-lang-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  opacity: 0.8;
}

.mobile-lang-options {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-lang-option {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mobile-lang-option:hover {
  background: rgba(255, 255, 255, 0.1);
}

.mobile-lang-option .flag {
  font-size: 1.5rem;
}

.mobile-lang-option .name {
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .navbar-container {
    max-width: 100%;
    padding: 0 0.5rem;
  }
  
  .nav-links {
    gap: 0.5rem;
  }
  
  .nav-link {
    padding: 0.5rem 0.75rem;
  }
  
  .link-text {
    font-size: 0.85rem;
  }
}

@media (max-width: 1024px) {
  .nav-links {
    gap: 0.5rem;
  }
  
  .nav-link {
    padding: 0.5rem 0.75rem;
  }
  
  .link-text {
    font-size: 0.8rem;
  }
}

@media (max-width: 900px) {
  .nav-links {
    gap: 0.25rem;
  }
  
  .nav-link {
    padding: 0.5rem 0.5rem;
  }
  
  .link-text {
    font-size: 0.75rem;
  }
}

@media (max-width: 768px) {
  .navbar-container {
    padding: 0 1rem;
  }
  
  .nav-links {
    display: none;
  }
  
  .language-selector {
    display: none;
  }
  
  .mobile-menu-btn {
    display: block;
  }
  
  .logo-title {
    font-size: 1.2rem;
  }
  
  .logo-subtitle {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .navbar {
    height: 70px;
  }
  
  .logo-icon {
    font-size: 2rem;
  }
  
  .logo-title {
    font-size: 1rem;
  }
  
  .logo-subtitle {
    font-size: 0.7rem;
  }
  
  .mobile-menu {
    max-width: 100%;
  }
}
</style> 