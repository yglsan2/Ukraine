<script setup lang="js">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app.mjs'

const router = useRouter()
const appStore = useAppStore()

// État réactif
const isDarkMode = ref(false)
const isLoading = ref(false)
const toasts = ref([])

// Méthodes
const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  document.body.classList.toggle('dark-mode')
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
}

const openProfile = () => {
  router.push('/profile')
}

const openMessages = () => {
  router.push('/messages')
}

const openFavorites = () => {
  router.push('/favorites')
}

const logout = () => {
  appStore.logout()
  showToast('Déconnexion', 'Vous avez été déconnecté avec succès', 'fas fa-sign-out-alt', 'info')
  router.push('/')
}

const showToast = (title, message, icon, type = 'info') => {
  const id = Date.now()
  // Convertir les icônes FontAwesome en emojis
  const iconMap = {
    'fas fa-sign-out-alt': '🚪',
    'fas fa-check': '✅',
    'fas fa-exclamation-triangle': '⚠️',
    'fas fa-info-circle': 'ℹ️',
    'fas fa-times': '❌',
    'fas fa-heart': '❤️',
    'fas fa-book': '📖',
    'fas fa-user': '👤',
    'fas fa-envelope': '💬',
    'fas fa-home': '🏠',
    'fas fa-search': '🔍',
    'fas fa-plus': '➕',
    'fas fa-sun': '☀️',
    'fas fa-moon': '🌙'
  }
  
  const emojiIcon = iconMap[icon] || 'ℹ️'
  
  toasts.value.push({ id, title, message, icon: emojiIcon, type })
  
  setTimeout(() => {
    removeToast(id)
  }, 5000)
}

const removeToast = (id) => {
  const index = toasts.value.findIndex(toast => toast.id === id)
  if (index > -1) {
    toasts.value.splice(index, 1)
  }
}

// Initialisation
onMounted(() => {
  // Restaurer le thème
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDarkMode.value = true
    document.body.classList.add('dark-mode')
  }
  
  // Initialiser le store
  appStore.initialize()
  
  // Vérifier la connexion PWA
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.ready.then(registration => {
      console.log('PWA ready:', registration)
    })
  }
  
  // Écouter les événements de mise à jour
  window.addEventListener('beforeinstallprompt', () => {
    console.log('PWA install prompt available')
  })
})
</script>

<template>
  <div id="app">
    <!-- Navigation principale -->
    <nav class="navbar navbar-expand-lg navbar-dark sticky-top">
      <div class="container-fluid">
        <!-- Titre à gauche -->
        <router-link class="navbar-brand d-flex align-items-center" to="/">
          <span class="brand-icon">📚</span>
          <span class="fw-bold">Lumières d'Ukraine</span>
        </router-link>
        
        <!-- Bouton toggle pour mobile -->
        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
          aria-controls="navbarNav" 
          aria-expanded="false" 
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <!-- Navigation à droite -->
        <div class="collapse navbar-collapse flex-grow-0" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">
                <span class="nav-icon">🏠</span>Accueil
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/explorer">
                <span class="nav-icon">🔍</span>Explorer
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/proposer">
                <span class="nav-icon">➕</span>Proposer un livre
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/mes-livres">
                <span class="nav-icon">📖</span>Mes livres
              </router-link>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                <span class="nav-icon">👤</span>Mon profil
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="#" @click="openProfile">
                  <span class="dropdown-icon">👤</span>Profil
                </a></li>
                <li><a class="dropdown-item" href="#" @click="openMessages">
                  <span class="dropdown-icon">💬</span>Messages
                </a></li>
                <li><a class="dropdown-item" href="#" @click="openFavorites">
                  <span class="dropdown-icon">❤️</span>Favoris
                </a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#" @click="logout">
                  <span class="dropdown-icon">🚪</span>Déconnexion
                </a></li>
              </ul>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click="toggleTheme">
                <span class="nav-icon">{{ isDarkMode ? '☀️' : '🌙' }}</span>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Contenu principal -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Navigation mobile (bottom) -->
    <nav class="navbar navbar-dark fixed-bottom d-lg-none">
      <div class="container-fluid">
        <div class="row w-100">
          <div class="col text-center">
            <router-link class="nav-link text-white" to="/">
              <span class="mobile-icon">🏠</span>
              <small class="d-block">Accueil</small>
            </router-link>
          </div>
          <div class="col text-center">
            <router-link class="nav-link text-white" to="/explorer">
              <span class="mobile-icon">🔍</span>
              <small class="d-block">Explorer</small>
            </router-link>
          </div>
          <div class="col text-center">
            <router-link class="nav-link text-white" to="/proposer">
              <span class="mobile-icon">➕</span>
              <small class="d-block">Ajouter</small>
            </router-link>
          </div>
          <div class="col text-center">
            <router-link class="nav-link text-white" to="/messages">
              <span class="mobile-icon">💬</span>
              <small class="d-block">Messages</small>
            </router-link>
          </div>
          <div class="col text-center">
            <router-link class="nav-link text-white" to="/profile">
              <span class="mobile-icon">👤</span>
              <small class="d-block">Profil</small>
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Toast notifications -->
    <div class="toast-container position-fixed bottom-0 end-0 p-3">
      <div 
        v-for="toast in toasts" 
        :key="toast.id"
        class="toast show" 
        role="alert"
      >
        <div class="toast-header">
          <span class="toast-icon">{{ toast.icon }}</span>
          <strong class="me-auto">{{ toast.title }}</strong>
          <button 
            type="button" 
            class="btn-close" 
            @click="removeToast(toast.id)"
          ></button>
        </div>
        <div class="toast-body">
          {{ toast.message }}
        </div>
      </div>
    </div>

    <!-- Loading overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Chargement...</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Reset complet pour éliminer toutes les marges et paddings */
* {
  box-sizing: border-box;
}

html, body {
  margin: 0 !important;
  padding: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  overflow-x: hidden;
}

#app {
  width: 100vw !important;
  height: 100vh !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow-x: hidden;
}

/* Bandeau principal moderne et professionnel aux couleurs ukrainiennes */
.navbar {
  background: linear-gradient(135deg, #0057b8 0%, #ffffff 25%, #ffdd00 50%, #ffffff 75%, #0057b8 100%) !important;
  box-shadow: 0 2px 15px rgba(0, 87, 184, 0.2);
  backdrop-filter: blur(10px);
  width: 100vw !important;
  margin: 0 !important;
  padding: 0.75rem 0 !important;
  position: relative;
  z-index: 1000;
  border-bottom: 2px solid rgba(255, 221, 0, 0.3);
}

/* Container avec espacement forcé */
.container-fluid {
  max-width: 100vw !important;
  width: 100vw !important;
  margin: 0 !important;
  padding: 0 2rem !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
}

.navbar-brand {
  color: #0057b8 !important;
  font-weight: 700;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  margin-right: 0 !important;
  flex-shrink: 0 !important;
}

.navbar-brand:hover {
  transform: scale(1.02);
  color: #0057b8 !important;
}

.brand-icon {
  font-size: 1.5rem;
  margin-right: 0.5rem;
}

/* Navigation forcée à droite */
.navbar-collapse {
  flex-grow: 0 !important;
  margin-left: auto !important;
}

.navbar-nav {
  display: flex !important;
  align-items: center !important;
  margin: 0 !important;
  padding: 0 !important;
  gap: 0.5rem;
}

.nav-link {
  color: #0057b8 !important;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  padding: 0.75rem 1.25rem !important;
  border-radius: 8px;
  white-space: nowrap;
}

.nav-link:hover {
  color: #ffdd00 !important;
  background: rgba(0, 87, 184, 0.1);
  transform: translateY(-1px);
}

.nav-icon {
  font-size: 1.1rem;
  margin-right: 0.5rem;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: #ffdd00;
  transition: all 0.3s ease;
  transform: translateX(-50%);
  border-radius: 1px;
}

.nav-link:hover::after {
  width: 70%;
}

/* Contenu principal sans marges - optimisé pour tous les écrans */
.main-content {
  min-height: calc(100vh - 120px);
  padding: 20px 0 80px 0;
  width: 100vw !important;
  margin: 0 !important;
  overflow-x: hidden;
}

/* Navigation mobile moderne */
.navbar.fixed-bottom {
  background: linear-gradient(135deg, #0057b8 0%, #ffffff 25%, #ffdd00 50%, #ffffff 75%, #0057b8 100%) !important;
  box-shadow: 0 -2px 15px rgba(0, 87, 184, 0.2);
  padding: 10px 0 !important;
  margin: 0 !important;
  width: 100vw !important;
  border-top: 2px solid rgba(255, 221, 0, 0.3);
}

.navbar.fixed-bottom .nav-link {
  color: #0057b8 !important;
  padding: 8px 4px !important;
  font-size: 0.8rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.navbar.fixed-bottom .nav-link:hover {
  color: #ffdd00 !important;
  transform: translateY(-2px);
}

.mobile-icon {
  font-size: 1.3rem;
  margin-bottom: 2px;
  display: block;
}

.navbar.fixed-bottom .nav-link small {
  font-size: 0.7rem;
  line-height: 1;
  font-weight: 500;
  color: #0057b8;
}

/* Dropdown moderne et professionnel */
.dropdown-menu {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 50%, #ffffff 100%);
  border: 1px solid rgba(0, 87, 184, 0.2);
  box-shadow: 0 8px 25px rgba(0, 87, 184, 0.15);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  margin-top: 0.5rem;
}

.dropdown-item {
  color: #0057b8 !important;
  padding: 0.75rem 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.dropdown-item:hover {
  background: rgba(0, 87, 184, 0.1) !important;
  color: #ffdd00 !important;
  transform: translateX(3px);
}

.dropdown-icon {
  font-size: 1rem;
  margin-right: 0.5rem;
}

.dropdown-divider {
  border-color: rgba(0, 87, 184, 0.2);
  margin: 0.5rem 0;
}

/* Toggle button moderne */
.navbar-toggler {
  border: 2px solid rgba(0, 87, 184, 0.3) !important;
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.navbar-toggler:hover {
  border-color: #ffdd00 !important;
  background: rgba(0, 87, 184, 0.1);
}

.navbar-toggler:focus {
  box-shadow: 0 0 0 0.2rem rgba(255, 221, 0, 0.25) !important;
}

/* Collapse mobile amélioré */
.navbar-collapse {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 249, 250, 0.95) 100%);
  border-radius: 12px;
  margin-top: 10px;
  padding: 15px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 25px rgba(0, 87, 184, 0.15);
  border: 1px solid rgba(0, 87, 184, 0.1);
}

/* Dark mode amélioré */
.dark-mode {
  background-color: #1a1a1a;
  color: #ffffff;
}

.dark-mode .navbar {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%) !important;
}

.dark-mode .card {
  background-color: #2d2d2d;
  border-color: #404040;
}

/* Loading overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(5px);
}

.loading-overlay .spinner-border {
  width: 3rem;
  height: 3rem;
  color: #ffdd00;
}

/* Toast amélioré */
.toast-container {
  z-index: 9998;
}

.toast {
  max-width: 350px;
  box-shadow: 0 8px 25px rgba(0, 87, 184, 0.15);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 87, 184, 0.1);
}

.toast-icon {
  font-size: 1.1rem;
  margin-right: 0.5rem;
}

/* Animations améliorées */
@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.toast {
  animation: slideInRight 0.3s ease;
}

/* Responsive optimisé pour TOUS les écrans */

/* Très grands écrans (4K et plus) */
@media (min-width: 2560px) {
  .container-fluid {
    padding: 0 4rem !important;
  }
  
  .navbar-brand {
    font-size: 1.5rem;
  }
  
  .nav-link {
    font-size: 1.1rem;
    padding: 0.75rem 1.5rem !important;
  }
  
  .main-content {
    padding: 40px 0 100px 0;
  }
}

/* Grands écrans (Full HD et plus) */
@media (min-width: 1920px) {
  .container-fluid {
    padding: 0 3rem !important;
  }
  
  .navbar-brand {
    font-size: 1.3rem;
  }
  
  .nav-link {
    font-size: 1rem;
    padding: 0.6rem 1.2rem !important;
  }
  
  .main-content {
    padding: 30px 0 90px 0;
  }
}

/* Écrans moyens (HD et plus) */
@media (min-width: 1366px) {
  .container-fluid {
    padding: 0 2.5rem !important;
  }
  
  .navbar-brand {
    font-size: 1.2rem;
  }
  
  .nav-link {
    font-size: 0.95rem;
    padding: 0.5rem 1rem !important;
  }
  
  .main-content {
    padding: 25px 0 85px 0;
  }
}

/* Écrans standards (1024px et plus) */
@media (min-width: 1024px) {
  .container-fluid {
    padding: 0 2rem !important;
  }
  
  .navbar-brand {
    font-size: 1.1rem;
  }
  
  .nav-link {
    font-size: 0.9rem;
    padding: 0.5rem 1rem !important;
  }
  
  .main-content {
    padding: 20px 0 80px 0;
  }
}

/* Tablettes */
@media (max-width: 1199.98px) {
  .navbar-nav .nav-link {
    padding: 0.5rem 0.75rem;
    font-size: 0.9rem;
  }
  
  .navbar-brand {
    font-size: 1.1rem;
  }
  
  .container-fluid {
    padding: 0 1.5rem !important;
  }
}

/* Tablettes et petits écrans */
@media (max-width: 991.98px) {
  .main-content {
    padding-bottom: 100px;
    padding-top: 15px;
  }
  
  .navbar-nav .nav-link {
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin: 2px 0;
  }
  
  .navbar-nav .nav-link:hover {
    background: rgba(0, 87, 184, 0.1);
    transform: translateY(-2px);
  }
  
  .container-fluid {
    padding: 0 1rem !important;
  }
}

/* Mobiles */
@media (max-width: 767.98px) {
  .navbar-brand {
    font-size: 1rem;
  }
  
  .navbar-brand span:last-child {
    display: none;
  }
  
  .brand-icon {
    font-size: 1.3rem;
  }
  
  .main-content {
    padding-bottom: 120px;
  }
  
  .container-fluid {
    padding: 0 0.75rem !important;
  }
}

/* Petits mobiles */
@media (max-width: 575.98px) {
  .navbar-brand {
    font-size: 0.9rem;
  }
  
  .navbar-nav .nav-link {
    font-size: 0.85rem;
    padding: 0.5rem 0.75rem;
  }
  
  .main-content {
    padding: 10px 0 130px 0;
  }
  
  .container-fluid {
    padding: 0 0.5rem !important;
  }
}

/* Très petits écrans */
@media (max-width: 375px) {
  .navbar-brand {
    font-size: 0.8rem;
  }
  
  .navbar-nav .nav-link {
    font-size: 0.8rem;
    padding: 0.4rem 0.6rem;
  }
  
  .container-fluid {
    padding: 0 0.25rem !important;
  }
}
</style>
