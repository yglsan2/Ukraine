<script setup>
import NavBar from '@/components/NavBar.vue'
import { ref, onMounted } from 'vue'

const animatedStats = ref({
  books: 0,
  members: 0,
  events: 0,
  languages: 0
})

const targetStats = {
  books: 500,
  members: 200,
  events: 50,
  languages: 5
}

onMounted(() => {
  // Animation des statistiques
  const animateStats = () => {
    const duration = 2000
    const steps = 60
    const stepDuration = duration / steps
    
    let step = 0
    const timer = setInterval(() => {
      step++
      const progress = step / steps
      const easeOut = 1 - Math.pow(1 - progress, 3)
      
      animatedStats.value.books = Math.floor(targetStats.books * easeOut)
      animatedStats.value.members = Math.floor(targetStats.members * easeOut)
      animatedStats.value.events = Math.floor(targetStats.events * easeOut)
      animatedStats.value.languages = Math.floor(targetStats.languages * easeOut)
      
      if (step >= steps) {
        clearInterval(timer)
      }
    }, stepDuration)
  }
  
  // Démarrer l'animation après 1 seconde
  setTimeout(animateStats, 1000)
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-yellow-50 overflow-hidden">
    <!-- Navbar -->
    <NavBar />
    
    <!-- Hero Section Ultra-Moderne -->
    <section class="relative min-h-screen flex items-center justify-center overflow-hidden px-4 sm:px-6 lg:px-8">
      <!-- Arrière-plan animé -->
      <div class="absolute inset-0">
        <!-- Particules flottantes -->
        <div class="absolute top-20 left-10 w-4 h-4 bg-yellow-300 rounded-full animate-ping opacity-60"></div>
        <div class="absolute top-40 right-20 w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
        <div class="absolute top-60 left-1/4 w-3 h-3 bg-yellow-200 rounded-full animate-pulse"></div>
        <div class="absolute top-80 right-1/3 w-1 h-1 bg-blue-300 rounded-full animate-ping"></div>
        <div class="absolute top-32 left-2/3 w-2 h-2 bg-yellow-400 rounded-full animate-bounce"></div>
        
                 <!-- Livres flottants géants avec mouvements naturels -->
         <div class="absolute top-10 left-1/6 animate-float-hero-1">
           <div class="w-16 h-20 bg-gradient-to-br from-yellow-300 to-yellow-500 rounded-lg shadow-2xl transform rotate-12 border-2 border-yellow-200"></div>
         </div>
         <div class="absolute top-20 right-1/4 animate-float-hero-2">
           <div class="w-12 h-16 bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg shadow-2xl transform -rotate-6 border-2 border-blue-300"></div>
         </div>
         <div class="absolute top-40 left-3/4 animate-float-hero-3">
           <div class="w-14 h-18 bg-gradient-to-br from-white to-gray-100 rounded-lg shadow-2xl transform rotate-3 border-2 border-gray-200"></div>
         </div>
        
        <!-- Ondes de lumière -->
        <div class="absolute inset-0 bg-gradient-radial from-yellow-200/20 via-transparent to-transparent"></div>
      </div>
      
             <!-- Contenu principal -->
       <div class="relative z-10 text-center max-w-6xl mx-auto w-full">
                 <!-- Titre principal avec effet de glitch -->
         <div class="mb-8">
           <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-black mb-6 relative">
             <span class="bg-gradient-to-r from-blue-600 via-yellow-400 to-blue-800 bg-clip-text text-transparent">
               Lumières d'Ukraine
             </span>
             <div class="absolute -inset-2 bg-gradient-to-r from-yellow-400 to-blue-500 rounded-3xl blur-2xl opacity-30"></div>
           </h1>
          
                              <!-- Sous-titre avec effets subtils -->
           <div class="text-lg sm:text-xl md:text-2xl lg:text-3xl font-bold text-gray-700 mb-8">
             <span class="inline-block opacity-80">🌟</span>
             <span class="bg-gradient-to-r from-blue-700 to-yellow-600 bg-clip-text text-transparent">
               Partagez la culture ukrainienne à travers les livres
             </span>
             <span class="inline-block opacity-80">🌟</span>
           </div>
          
                     <!-- Description -->
           <p class="text-base sm:text-lg md:text-xl lg:text-2xl text-gray-600 max-w-4xl mx-auto leading-relaxed mb-12 px-4">
             Découvrez une collection unique de livres ukrainiens, participez à des événements culturels 
             et rejoignez une communauté passionnée de littérature et de partage.
           </p>
        </div>
        
                 <!-- Boutons d'action avec effets -->
         <div class="flex flex-col sm:flex-row gap-4 sm:gap-6 justify-center items-center mb-16 px-4">
           <button class="group relative px-8 sm:px-10 md:px-12 py-4 sm:py-5 md:py-6 bg-gradient-to-r from-yellow-400 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 text-blue-900 font-black text-lg sm:text-xl rounded-3xl shadow-2xl border-4 border-yellow-200/60 transition-all duration-500 transform hover:scale-110 hover:shadow-3xl">
             <span class="relative z-10 flex items-center gap-2 sm:gap-3">
               <span class="text-xl sm:text-2xl group-hover:rotate-12 transition-transform duration-300">🚀</span>
               Commencer l'aventure
             </span>
             <div class="absolute inset-0 bg-gradient-to-r from-yellow-300 to-yellow-400 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 blur-sm"></div>
           </button>
           
           <button class="group relative px-8 sm:px-10 md:px-12 py-4 sm:py-5 md:py-6 bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 hover:from-blue-700 hover:to-blue-600 text-yellow-200 font-black text-lg sm:text-xl rounded-3xl shadow-2xl border-4 border-blue-300/60 transition-all duration-500 transform hover:scale-110 hover:shadow-3xl">
             <span class="relative z-10 flex items-center gap-2 sm:gap-3">
               <span class="text-xl sm:text-2xl group-hover:rotate-12 transition-transform duration-300">📚</span>
               Découvrir les livres
             </span>
             <div class="absolute inset-0 bg-gradient-to-r from-blue-500 to-blue-600 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 blur-sm"></div>
           </button>
         </div>
        
                 <!-- Indicateur de scroll -->
         <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2">
           <div class="w-6 h-10 border-2 border-blue-600 rounded-full flex justify-center">
             <div class="w-1 h-3 bg-blue-600 rounded-full mt-2"></div>
           </div>
         </div>
      </div>
    </section>
    
    <!-- Section Fonctionnalités avec effets glassmorphism -->
    <section class="py-12 sm:py-16 md:py-20 relative">
      <div class="absolute inset-0 bg-gradient-to-br from-blue-100/50 via-white to-yellow-100/50"></div>
      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12 sm:mb-16 md:mb-20">
          <h2 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black mb-4 sm:mb-6">
            <span class="bg-gradient-to-r from-blue-700 via-yellow-600 to-blue-800 bg-clip-text text-transparent">
              Fonctionnalités Magiques
            </span>
          </h2>
          <p class="text-lg sm:text-xl md:text-2xl text-gray-600 max-w-4xl mx-auto px-4">
            Une expérience unique pour découvrir et partager la culture ukrainienne
          </p>
        </div>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
          <!-- Carte 1 -->
          <div class="group relative p-6 sm:p-6 sm:p-8 bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 hover:shadow-3xl transition-all duration-500 transform hover:scale-105">
            <div class="absolute inset-0 bg-gradient-to-br from-yellow-400/20 to-blue-400/20 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="relative z-10 text-center">
              <div class="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-yellow-300 to-yellow-500 rounded-2xl flex items-center justify-center mx-auto mb-4 sm:mb-4 sm:mb-6 shadow-xl group-hover:scale-110 transition-transform duration-300">
                <span class="text-3xl sm:text-3xl sm:text-4xl group-hover:rotate-12 transition-transform duration-300">📚</span>
              </div>
              <h3 class="text-xl sm:text-2xl font-bold text-gray-900 mb-3 sm:mb-4">Bibliothèque Virtuelle</h3>
              <p class="text-sm sm:text-base text-sm sm:text-base text-gray-600 leading-relaxed">
                Explorez notre collection unique de livres ukrainiens, classiques et contemporains, 
                disponibles en plusieurs langues.
              </p>
            </div>
          </div>
          
          <!-- Carte 2 -->
          <div class="group relative p-6 sm:p-6 sm:p-8 bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 hover:shadow-3xl transition-all duration-500 transform hover:scale-105">
            <div class="absolute inset-0 bg-gradient-to-br from-blue-400/20 to-yellow-400/20 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="relative z-10 text-center">
              <div class="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-blue-400 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4 sm:mb-4 sm:mb-6 shadow-xl group-hover:scale-110 transition-transform duration-300">
                <span class="text-3xl sm:text-3xl sm:text-4xl group-hover:rotate-12 transition-transform duration-300">🎉</span>
              </div>
              <h3 class="text-xl sm:text-2xl font-bold text-gray-900 mb-3 sm:mb-4">Événements Culturels</h3>
              <p class="text-sm sm:text-base text-sm sm:text-base text-gray-600 leading-relaxed">
                Participez à des rencontres littéraires, des lectures publiques et des événements 
                culturels ukrainiens.
              </p>
            </div>
          </div>
          
          <!-- Carte 3 -->
          <div class="group relative p-6 sm:p-8 bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 hover:shadow-3xl transition-all duration-500 transform hover:scale-105">
            <div class="absolute inset-0 bg-gradient-to-br from-yellow-400/20 to-blue-400/20 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="relative z-10 text-center">
              <div class="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-green-400 to-green-600 rounded-2xl flex items-center justify-center mx-auto mb-4 sm:mb-6 shadow-xl group-hover:scale-110 transition-transform duration-300">
                <span class="text-3xl sm:text-4xl group-hover:rotate-12 transition-transform duration-300">🤖</span>
              </div>
              <h3 class="text-xl sm:text-2xl font-bold text-gray-900 mb-3 sm:mb-4">Assistant IA</h3>
              <p class="text-sm sm:text-base text-gray-600 leading-relaxed">
                Notre chatbot intelligent vous aide à trouver des livres, répond à vos questions 
                et vous guide dans votre découverte.
              </p>
            </div>
          </div>
          
          <!-- Carte 4 -->
          <div class="group relative p-6 sm:p-8 bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 hover:shadow-3xl transition-all duration-500 transform hover:scale-105">
            <div class="absolute inset-0 bg-gradient-to-br from-blue-400/20 to-yellow-400/20 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="relative z-10 text-center">
              <div class="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-purple-400 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4 sm:mb-6 shadow-xl group-hover:scale-110 transition-transform duration-300">
                <span class="text-3xl sm:text-4xl group-hover:rotate-12 transition-transform duration-300">🌍</span>
              </div>
              <h3 class="text-xl sm:text-2xl font-bold text-gray-900 mb-3 sm:mb-4">Multilingue</h3>
              <p class="text-sm sm:text-base text-gray-600 leading-relaxed">
                Interface disponible en français, anglais, ukrainien, allemand et polonais 
                pour une accessibilité maximale.
              </p>
            </div>
          </div>
          
          <!-- Carte 5 -->
          <div class="group relative p-6 sm:p-8 bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 hover:shadow-3xl transition-all duration-500 transform hover:scale-105">
            <div class="absolute inset-0 bg-gradient-to-br from-yellow-400/20 to-blue-400/20 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="relative z-10 text-center">
              <div class="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-red-400 to-red-600 rounded-2xl flex items-center justify-center mx-auto mb-4 sm:mb-6 shadow-xl group-hover:scale-110 transition-transform duration-300">
                <span class="text-3xl sm:text-4xl group-hover:rotate-12 transition-transform duration-300">🔒</span>
              </div>
              <h3 class="text-xl sm:text-2xl font-bold text-gray-900 mb-3 sm:mb-4">Sécurisé</h3>
              <p class="text-sm sm:text-base text-gray-600 leading-relaxed">
                Authentification JWT et protection des données pour une expérience 
                utilisateur sécurisée et confidentielle.
              </p>
            </div>
          </div>
          
          <!-- Carte 6 -->
          <div class="group relative p-6 sm:p-8 bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 hover:shadow-3xl transition-all duration-500 transform hover:scale-105">
            <div class="absolute inset-0 bg-gradient-to-br from-blue-400/20 to-yellow-400/20 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="relative z-10 text-center">
              <div class="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-yellow-300 via-blue-400 to-yellow-500 rounded-2xl flex items-center justify-center mx-auto mb-4 sm:mb-6 shadow-xl group-hover:scale-110 transition-transform duration-300">
                <span class="text-3xl sm:text-4xl group-hover:rotate-12 transition-transform duration-300">💙💛</span>
              </div>
              <h3 class="text-xl sm:text-2xl font-bold text-gray-900 mb-3 sm:mb-4">Communauté</h3>
              <p class="text-sm sm:text-base text-gray-600 leading-relaxed">
                Rejoignez une communauté passionnée de culture ukrainienne, 
                partagez vos découvertes et créez des liens durables.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Section Statistiques avec animation -->
    <section class="py-12 sm:py-16 md:py-20 bg-gradient-to-br from-blue-600 via-blue-700 to-blue-800 relative overflow-hidden">
      <!-- Particules de fond -->
      <div class="absolute inset-0">
        <div class="absolute top-10 left-10 w-2 h-2 bg-yellow-300 rounded-full animate-ping"></div>
        <div class="absolute top-20 right-20 w-1 h-1 bg-yellow-200 rounded-full animate-bounce"></div>
        <div class="absolute top-40 left-1/3 w-3 h-3 bg-yellow-400 rounded-full animate-pulse"></div>
      </div>
      
      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12 sm:mb-16 md:mb-20">
          <h2 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black text-white mb-4 sm:mb-6">
            Notre <span class="text-yellow-300">Impact</span>
          </h2>
          <p class="text-lg sm:text-xl md:text-2xl text-white/90 max-w-4xl mx-auto px-4">
            Découvrez les chiffres qui témoignent de notre engagement pour la culture ukrainienne
          </p>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 sm:gap-8">
          <div class="text-center group">
            <div class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black text-yellow-300 mb-3 sm:mb-4 group-hover:scale-110 transition-transform duration-300">
              {{ animatedStats.books }}+
            </div>
            <div class="text-base sm:text-lg md:text-xl text-white/90 font-semibold">Livres partagés</div>
          </div>
          <div class="text-center group">
            <div class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black text-yellow-300 mb-3 sm:mb-4 group-hover:scale-110 transition-transform duration-300">
              {{ animatedStats.members }}+
            </div>
            <div class="text-base sm:text-lg md:text-xl text-white/90 font-semibold">Membres actifs</div>
          </div>
          <div class="text-center group">
            <div class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black text-yellow-300 mb-3 sm:mb-4 group-hover:scale-110 transition-transform duration-300">
              {{ animatedStats.events }}+
            </div>
            <div class="text-base sm:text-lg md:text-xl text-white/90 font-semibold">Événements</div>
          </div>
          <div class="text-center group">
            <div class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black text-yellow-300 mb-3 sm:mb-4 group-hover:scale-110 transition-transform duration-300">
              {{ animatedStats.languages }}
            </div>
            <div class="text-base sm:text-lg md:text-xl text-white/90 font-semibold">Langues</div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Section Call to Action finale -->
    <section class="py-12 sm:py-16 md:py-20 bg-gradient-to-br from-yellow-50 via-white to-blue-50 relative">
      <div class="absolute inset-0">
                 <!-- Livres flottants de fond -->
         <div class="absolute bottom-10 left-10 animate-float-final-1">
           <div class="w-8 h-10 bg-gradient-to-br from-yellow-300 to-yellow-500 rounded-sm shadow-lg transform rotate-12"></div>
         </div>
         <div class="absolute bottom-20 right-20 animate-float-final-2">
           <div class="w-6 h-8 bg-gradient-to-br from-blue-400 to-blue-600 rounded-sm shadow-lg transform -rotate-6"></div>
         </div>
      </div>
      
      <div class="relative z-10 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black mb-6 sm:mb-8">
          <span class="bg-gradient-to-r from-blue-700 via-yellow-600 to-blue-800 bg-clip-text text-transparent">
            Prêt à rejoindre l'aventure ?
          </span>
        </h2>
        <p class="text-lg sm:text-xl md:text-2xl text-gray-600 mb-8 sm:mb-12 max-w-4xl mx-auto leading-relaxed px-4">
          Commencez dès aujourd'hui à partager et découvrir la richesse de la littérature ukrainienne. 
          Rejoignez notre communauté et faites partie de cette belle aventure culturelle.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 sm:gap-6 justify-center items-center">
          <button class="group relative px-8 sm:px-10 md:px-12 py-4 sm:py-5 md:py-6 bg-gradient-to-r from-yellow-400 via-yellow-500 to-yellow-600 hover:from-yellow-500 hover:to-yellow-400 text-blue-900 font-black text-lg sm:text-xl rounded-3xl shadow-2xl border-4 border-yellow-200/60 transition-all duration-500 transform hover:scale-110 hover:shadow-3xl">
            <span class="relative z-10 flex items-center gap-2 sm:gap-3">
              <span class="text-xl sm:text-2xl group-hover:rotate-12 transition-transform duration-300">🎯</span>
              Commencer maintenant
            </span>
          </button>
          <button class="group relative px-8 sm:px-10 md:px-12 py-4 sm:py-5 md:py-6 bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 hover:from-blue-700 hover:to-blue-600 text-yellow-200 font-black text-lg sm:text-xl rounded-3xl shadow-2xl border-4 border-blue-300/60 transition-all duration-500 transform hover:scale-110 hover:shadow-3xl">
            <span class="relative z-10 flex items-center gap-2 sm:gap-3">
              <span class="text-xl sm:text-2xl group-hover:rotate-12 transition-transform duration-300">ℹ️</span>
              En savoir plus
            </span>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Animations naturelles et variées */
@keyframes float-hero-1 {
  0%, 100% { transform: translateY(0px) translateX(0px) rotate(12deg); }
  25% { transform: translateY(-15px) translateX(5px) rotate(18deg); }
  50% { transform: translateY(-25px) translateX(-3px) rotate(8deg); }
  75% { transform: translateY(-12px) translateX(2px) rotate(15deg); }
}
@keyframes float-hero-2 {
  0%, 100% { transform: translateY(0px) translateX(0px) rotate(-6deg); }
  30% { transform: translateY(-18px) translateX(-6px) rotate(-2deg); }
  60% { transform: translateY(-28px) translateX(4px) rotate(-12deg); }
  90% { transform: translateY(-8px) translateX(-2px) rotate(-8deg); }
}
@keyframes float-hero-3 {
  0%, 100% { transform: translateY(0px) translateX(0px) rotate(3deg); }
  20% { transform: translateY(-20px) translateX(3px) rotate(8deg); }
  40% { transform: translateY(-12px) translateX(-4px) rotate(-2deg); }
  80% { transform: translateY(-22px) translateX(2px) rotate(6deg); }
}

.animate-float-hero-1 {
  animation: float-hero-1 9s ease-in-out infinite;
}
.animate-float-hero-2 {
  animation: float-hero-2 7.5s ease-in-out infinite;
}
.animate-float-hero-3 {
  animation: float-hero-3 10s ease-in-out infinite;
}

@keyframes float-final-1 {
  0%, 100% { transform: translateY(0px) translateX(0px) rotate(12deg); }
  40% { transform: translateY(-8px) translateX(2px) rotate(15deg); }
  80% { transform: translateY(-4px) translateX(-1px) rotate(10deg); }
}
@keyframes float-final-2 {
  0%, 100% { transform: translateY(0px) translateX(0px) rotate(-6deg); }
  50% { transform: translateY(-6px) translateX(-2px) rotate(-3deg); }
  90% { transform: translateY(-2px) translateX(1px) rotate(-8deg); }
}

.animate-float-final-1 {
  animation: float-final-1 6s ease-in-out infinite;
}
.animate-float-final-2 {
  animation: float-final-2 8s ease-in-out infinite;
}



/* Effets de glassmorphism */
.backdrop-blur-xl {
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}

/* Ombres personnalisées */
.shadow-3xl {
  box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.25);
}

/* Gradient radial */
.bg-gradient-radial {
  background: radial-gradient(circle, var(--tw-gradient-stops));
}
</style>
