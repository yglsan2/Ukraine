<template>
  <nav class="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-blue-900/95 via-blue-800/95 to-yellow-400/95 backdrop-blur-3xl shadow-2xl border-b border-yellow-300/30 overflow-hidden">
    <!-- Particules flottantes -->
    <div class="absolute inset-0 pointer-events-none">
      <div class="floating-particle top-4 left-10 w-2 h-2 bg-yellow-300 rounded-full animate-pulse"></div>
      <div class="floating-particle top-8 right-20 w-1 h-1 bg-blue-300 rounded-full animate-ping"></div>
      <div class="floating-particle top-12 left-1/4 w-1.5 h-1.5 bg-white rounded-full animate-bounce"></div>
      <div class="floating-particle top-6 right-1/3 w-1 h-1 bg-yellow-200 rounded-full animate-pulse"></div>
    </div>

    <!-- Livres flottants dans la navbar avec mouvements naturels -->
    <div class="absolute inset-0 pointer-events-none">
      <div class="floating-book top-2 left-1/4 animate-float-natural-1">
        <div class="w-5 h-7 bg-gradient-to-br from-yellow-300 to-yellow-500 rounded-sm shadow-lg transform rotate-8 border border-yellow-200"></div>
      </div>
      <div class="floating-book top-1 right-1/3 animate-float-natural-2">
        <div class="w-4 h-6 bg-gradient-to-br from-blue-400 to-blue-600 rounded-sm shadow-lg transform -rotate-12 border border-blue-300"></div>
      </div>
      <div class="floating-book top-3 left-2/3 animate-float-natural-3">
        <div class="w-6 h-8 bg-gradient-to-br from-white to-gray-100 rounded-sm shadow-lg transform rotate-5 border border-gray-200"></div>
      </div>
      <div class="floating-book top-2 right-1/5 animate-float-natural-4">
        <div class="w-3 h-5 bg-gradient-to-br from-yellow-200 to-yellow-400 rounded-sm shadow-lg transform -rotate-8 border border-yellow-100"></div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-6 flex items-center justify-between h-20 relative z-10">
      <!-- Logo animé avec effet de lumière -->
      <div class="flex items-center space-x-4 group cursor-pointer">
        <div class="relative">
          <div class="w-16 h-16 bg-gradient-to-br from-yellow-300 via-yellow-400 to-yellow-500 rounded-2xl flex items-center justify-center shadow-2xl animate-pulse group-hover:scale-110 transition-all duration-500 border-2 border-yellow-200/50">
            <span class="text-4xl drop-shadow-lg animate-bounce">🇺🇦</span>
          </div>
          <div class="absolute -inset-1 bg-gradient-to-r from-yellow-400 to-blue-500 rounded-2xl blur opacity-30 group-hover:opacity-50 transition-opacity duration-500 -z-10"></div>
          <div class="absolute -bottom-1 left-1/2 -translate-x-1/2 text-xs text-yellow-200 font-bold animate-pulse">Lumière</div>
        </div>
        <div class="relative">
          <h1 class="text-3xl font-black bg-gradient-to-r from-yellow-300 via-white to-blue-400 bg-clip-text text-transparent tracking-tight drop-shadow-lg animate-pulse">
            Lumières d'Ukraine
          </h1>
          <p class="text-sm text-blue-100/90 font-medium tracking-wider animate-pulse">Partage de culture</p>
          <div class="absolute -bottom-1 left-0 w-full h-0.5 bg-gradient-to-r from-yellow-400 to-blue-500 rounded-full animate-pulse"></div>
        </div>
      </div>

      <!-- Navigation principale avec effets -->
      <div class="hidden lg:flex items-center space-x-1">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="group relative px-6 py-3 rounded-2xl font-bold text-white/90 hover:text-yellow-300 focus:text-yellow-400 focus:outline-none focus:ring-2 focus:ring-yellow-400/60 transition-all duration-300 flex items-center gap-3 bg-white/5 hover:bg-yellow-400/20 backdrop-blur-md shadow-lg hover:shadow-2xl border border-transparent hover:border-yellow-300/50 transform hover:scale-105"
          :class="{ 'bg-yellow-400/30 text-yellow-200 shadow-2xl border-yellow-300/70 scale-105': route.path === item.path }"
        >
          <span class="text-2xl group-hover:scale-125 group-hover:rotate-12 transition-all duration-300">{{ item.icon }}</span>
          <span class="relative">
            {{ item.name }}
            <span v-if="route.path === item.path" class="absolute -bottom-2 left-1/2 -translate-x-1/2 w-3 h-3 bg-yellow-300 rounded-full shadow-lg"></span>
          </span>
          <div class="absolute inset-0 bg-gradient-to-r from-yellow-400/20 to-blue-400/20 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </router-link>
      </div>

      <!-- Actions à droite avec effets premium -->
      <div class="flex items-center space-x-4">
        <!-- Sélecteur de langue avec animation -->
        <div class="relative">
          <button
            @click="toggleLanguageMenu"
            class="flex items-center gap-3 px-5 py-3 rounded-2xl bg-gradient-to-r from-white/10 to-yellow-400/10 hover:from-yellow-400/20 hover:to-blue-400/20 text-white font-bold shadow-xl border border-yellow-200/30 focus:outline-none focus:ring-2 focus:ring-yellow-300/60 transition-all duration-300 transform hover:scale-105"
            aria-haspopup="true"
            :aria-expanded="languageMenuOpen"
          >
            <span class="text-2xl">{{ currentLanguage.flag }}</span>
            <span class="uppercase tracking-widest text-yellow-200">{{ currentLanguage.code }}</span>
            <svg class="w-5 h-5 ml-1 transition-transform text-yellow-200" :class="{ 'rotate-180': languageMenuOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </button>
          
          <!-- Menu déroulant des langues avec effet glassmorphism -->
          <transition name="fade-scale">
            <div
              v-show="languageMenuOpen"
              class="absolute right-0 mt-4 w-64 bg-white/95 rounded-3xl shadow-2xl border border-yellow-200/40 overflow-hidden animate-pop-in backdrop-blur-2xl z-50"
              @click.away="languageMenuOpen = false"
            >
              <div class="p-4">
                <div class="text-sm font-bold text-blue-800 px-3 py-2 uppercase tracking-wider border-b border-yellow-200/30">Choisir une langue</div>
                <div class="space-y-2 mt-3">
                  <button
                    v-for="lang in languages"
                    :key="lang.code"
                    @click="selectLanguage(lang)"
                    class="w-full flex items-center gap-4 px-4 py-3 rounded-2xl hover:bg-gradient-to-r hover:from-yellow-100/80 hover:to-blue-100/80 transition-all duration-300 group transform hover:scale-105"
                    :class="{ 'bg-gradient-to-r from-yellow-200/80 to-blue-200/80 text-blue-900 font-bold shadow-lg': currentLanguage.code === lang.code }"
                  >
                    <span class="text-3xl group-hover:scale-125 group-hover:rotate-12 transition-all duration-300">{{ lang.flag }}</span>
                    <div class="flex-1 text-left">
                      <div class="font-semibold text-gray-800">{{ lang.name }}</div>
                      <div class="text-xs text-gray-600">{{ lang.nativeName }}</div>
                    </div>
                    <span v-if="currentLanguage.code === lang.code" class="w-3 h-3 bg-blue-600 rounded-full shadow-lg"></span>
                  </button>
                </div>
              </div>
            </div>
          </transition>
        </div>

        <!-- Boutons d'authentification avec effets -->
        <button class="hidden md:inline-block px-6 py-3 bg-gradient-to-r from-yellow-300 via-yellow-400 to-yellow-500 hover:from-yellow-400 hover:to-yellow-300 text-blue-900 font-black rounded-2xl shadow-xl border-2 border-yellow-200/60 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl">
          Se connecter
        </button>
        <button class="hidden md:inline-block px-6 py-3 bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 hover:from-blue-700 hover:to-blue-600 text-yellow-200 font-black rounded-2xl shadow-xl border-2 border-blue-300/60 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl">
          S'inscrire
        </button>

        <!-- Menu mobile avec animation -->
        <button
          @click="toggleMobileMenu"
          class="lg:hidden p-4 rounded-2xl bg-gradient-to-r from-white/10 to-yellow-400/10 hover:from-yellow-400/20 hover:to-blue-400/20 text-white shadow-xl border border-yellow-200/30 focus:outline-none focus:ring-2 focus:ring-yellow-300/60 transition-all duration-300 transform hover:scale-105"
          aria-label="Ouvrir le menu mobile"
        >
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
    </div>

    <!-- Menu mobile déroulant avec effets -->
    <transition name="slide-fade">
      <div
        v-show="mobileMenuOpen"
        class="lg:hidden border-t border-yellow-300/30 bg-gradient-to-br from-blue-900/95 via-blue-800/95 to-yellow-400/95 backdrop-blur-3xl shadow-2xl px-6 py-8 space-y-6 animate-pop-in"
      >
        <div class="space-y-3">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            @click="mobileMenuOpen = false"
            class="flex items-center gap-4 px-6 py-4 rounded-2xl font-bold text-white/90 hover:text-yellow-300 bg-white/5 hover:bg-yellow-400/20 backdrop-blur-md shadow-lg border border-transparent hover:border-yellow-300/50 transition-all duration-300 transform hover:scale-105"
            :class="{ 'bg-yellow-400/30 text-yellow-200 shadow-2xl border-yellow-300/70 scale-105': route.path === item.path }"
          >
            <span class="text-3xl">{{ item.icon }}</span>
            <span>{{ item.name }}</span>
          </router-link>
        </div>
        
        <div class="pt-6 border-t border-yellow-300/30">
          <div class="text-lg font-bold text-yellow-200 mb-4 uppercase tracking-wider">Langues disponibles</div>
          <div class="space-y-3">
            <button
              v-for="lang in languages"
              :key="lang.code"
              @click="selectLanguage(lang)"
              class="w-full flex items-center gap-4 px-6 py-4 rounded-2xl hover:bg-gradient-to-r hover:from-yellow-100/80 hover:to-blue-100/80 transition-all duration-300 group transform hover:scale-105"
              :class="{ 'bg-gradient-to-r from-yellow-200/80 to-blue-200/80 text-blue-900 font-bold shadow-lg': currentLanguage.code === lang.code }"
            >
              <span class="text-3xl group-hover:scale-125 group-hover:rotate-12 transition-all duration-300">{{ lang.flag }}</span>
              <div class="flex-1 text-left">
                <div class="font-semibold">{{ lang.name }}</div>
                <div class="text-sm text-gray-600">{{ lang.nativeName }}</div>
              </div>
              <span v-if="currentLanguage.code === lang.code" class="w-3 h-3 bg-blue-600 rounded-full shadow-lg"></span>
            </button>
          </div>
        </div>
        
        <div class="pt-6 border-t border-yellow-300/30 space-y-4">
          <button class="w-full px-6 py-4 bg-gradient-to-r from-yellow-300 via-yellow-400 to-yellow-500 hover:from-yellow-400 hover:to-yellow-300 text-blue-900 font-black rounded-2xl shadow-xl border-2 border-yellow-200/60 transition-all duration-300 transform hover:scale-105">
            Se connecter
          </button>
          <button class="w-full px-6 py-4 bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 hover:from-blue-700 hover:to-blue-600 text-yellow-200 font-black rounded-2xl shadow-xl border-2 border-blue-300/60 transition-all duration-300 transform hover:scale-105">
            S'inscrire
          </button>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const mobileMenuOpen = ref(false)
const languageMenuOpen = ref(false)

const currentLanguage = ref({
  code: 'FR',
  name: 'Français',
  nativeName: 'Français',
  flag: '🇫🇷'
})

const languages = [
  { code: 'FR', name: 'Français', nativeName: 'Français', flag: '🇫🇷' },
  { code: 'EN', name: 'Anglais', nativeName: 'English', flag: '🇬🇧' },
  { code: 'UK', name: 'Ukrainien', nativeName: 'Українська', flag: '🇺🇦' },
  { code: 'DE', name: 'Allemand', nativeName: 'Deutsch', flag: '🇩🇪' },
  { code: 'PL', name: 'Polonais', nativeName: 'Polski', flag: '🇵🇱' }
]

const navItems = [
  { name: 'Accueil', path: '/', icon: '🏠' },
  { name: 'Livres', path: '/books', icon: '📚' },
  { name: 'Événements', path: '/events', icon: '🎉' },
  { name: 'Association', path: '/association', icon: '🏛️' },
  { name: 'Chatbot', path: '/chatbot', icon: '🤖' },
  { name: 'À propos', path: '/about', icon: 'ℹ️' }
]

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
  if (mobileMenuOpen.value) {
    languageMenuOpen.value = false
  }
}

const toggleLanguageMenu = () => {
  languageMenuOpen.value = !languageMenuOpen.value
}

const selectLanguage = (lang) => {
  currentLanguage.value = lang
  languageMenuOpen.value = false
}
</script>

<style scoped>
.backdrop-blur-3xl {
  backdrop-filter: blur(48px);
  -webkit-backdrop-filter: blur(48px);
}

/* Animations naturelles et variées */
@keyframes float-natural-1 {
  0%, 100% { transform: translateY(0px) translateX(0px) rotate(8deg); }
  25% { transform: translateY(-8px) translateX(3px) rotate(12deg); }
  50% { transform: translateY(-12px) translateX(-2px) rotate(5deg); }
  75% { transform: translateY(-6px) translateX(1px) rotate(10deg); }
}
@keyframes float-natural-2 {
  0%, 100% { transform: translateY(0px) translateX(0px) rotate(-12deg); }
  30% { transform: translateY(-10px) translateX(-4px) rotate(-8deg); }
  60% { transform: translateY(-15px) translateX(2px) rotate(-15deg); }
  90% { transform: translateY(-5px) translateX(-1px) rotate(-10deg); }
}
@keyframes float-natural-3 {
  0%, 100% { transform: translateY(0px) translateX(0px) rotate(5deg); }
  20% { transform: translateY(-12px) translateX(2px) rotate(8deg); }
  40% { transform: translateY(-8px) translateX(-3px) rotate(2deg); }
  80% { transform: translateY(-14px) translateX(1px) rotate(6deg); }
}
@keyframes float-natural-4 {
  0%, 100% { transform: translateY(0px) translateX(0px) rotate(-8deg); }
  35% { transform: translateY(-6px) translateX(-2px) rotate(-5deg); }
  70% { transform: translateY(-10px) translateX(3px) rotate(-12deg); }
  85% { transform: translateY(-4px) translateX(-1px) rotate(-9deg); }
}

.animate-float-natural-1 {
  animation: float-natural-1 7s ease-in-out infinite;
}
.animate-float-natural-2 {
  animation: float-natural-2 5.5s ease-in-out infinite;
}
.animate-float-natural-3 {
  animation: float-natural-3 8s ease-in-out infinite;
}
.animate-float-natural-4 {
  animation: float-natural-4 6.5s ease-in-out infinite;
}

@keyframes bounce-x {
  0%, 100% { transform: translateX(0); }
  50% { transform: translateX(8px); }
}
.animate-bounce-x {
  animation: bounce-x 1.5s infinite;
}

@keyframes pop-in {
  0% { opacity: 0; transform: scale(0.9) translateY(-10px); }
  100% { opacity: 1; transform: scale(1) translateY(0); }
}
.animate-pop-in {
  animation: pop-in 0.4s cubic-bezier(.4,2,.6,1) both;
}

/* Transitions */
.fade-scale-enter-active, .fade-scale-leave-active {
  transition: all 0.3s cubic-bezier(.4,2,.6,1);
}
.fade-scale-enter-from, .fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}

.slide-fade-enter-active {
  transition: all 0.4s cubic-bezier(.4,2,.6,1);
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(-30px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

/* Particules flottantes */
.floating-particle {
  position: absolute;
  animation-duration: 3s;
  animation-iteration-count: infinite;
}
</style> 