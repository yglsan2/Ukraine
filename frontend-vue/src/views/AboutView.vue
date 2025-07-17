<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navbar -->
    <NavBar />
    
    <!-- Header -->
    <div class="pt-20 pb-12 bg-gradient-to-r from-ukraine-darkBlue to-ukraine-blue">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl sm:text-5xl font-display font-bold text-white mb-4">
            À propos de <span class="text-ukraine-yellow">Lumières d'Ukraine</span>
          </h1>
          <p class="text-xl text-white/90 max-w-3xl mx-auto">
            Découvrez l'histoire de notre projet et notre vision pour la culture ukrainienne
          </p>
        </div>
      </div>
    </div>

    <!-- Section Histoire -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-6">
              Notre <span class="text-gradient">Histoire</span>
            </h2>
            <p class="text-lg text-gray-600 mb-6">
              Lumières d'Ukraine est né d'une passion partagée pour la littérature ukrainienne 
              et d'un désir de créer des ponts culturels entre l'Ukraine et le reste du monde.
            </p>
            <p class="text-lg text-gray-600 mb-6">
              Fondé en 2023, notre projet a rapidement évolué pour devenir une plateforme 
              collaborative où les passionnés de culture ukrainienne peuvent partager, 
              découvrir et échanger autour de la littérature.
            </p>
            <p class="text-lg text-gray-600">
              Aujourd'hui, nous sommes fiers de compter plus de 200 membres actifs 
              et d'avoir facilité le partage de plus de 500 livres ukrainiens.
            </p>
          </div>
          <div class="relative">
            <div class="bg-gradient-to-br from-ukraine-blue/20 to-ukraine-yellow/20 rounded-2xl p-8">
              <div class="text-center">
                <span class="text-6xl mb-4 block">📖</span>
                <h3 class="text-2xl font-semibold text-gray-900 mb-4">Une Aventure Littéraire</h3>
                <p class="text-gray-600">
                  Chaque livre partagé est une fenêtre ouverte sur la culture ukrainienne.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section Vision -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-4">
            Notre <span class="text-gradient">Vision</span>
          </h2>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            Nous imaginons un monde où la culture ukrainienne est accessible à tous
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="card p-8 text-center">
            <div class="w-16 h-16 bg-ukraine-blue/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <span class="text-3xl">🌍</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">Accessibilité Mondiale</h3>
            <p class="text-gray-600">
              Rendre la littérature ukrainienne accessible à tous, partout dans le monde.
            </p>
          </div>
          
          <div class="card p-8 text-center">
            <div class="w-16 h-16 bg-ukraine-yellow/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <span class="text-3xl">🤝</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">Communauté Unie</h3>
            <p class="text-gray-600">
              Créer une communauté internationale passionnée de culture ukrainienne.
            </p>
          </div>
          
          <div class="card p-8 text-center">
            <div class="w-16 h-16 bg-ukraine-lightBlue/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <span class="text-3xl">💡</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">Innovation Continue</h3>
            <p class="text-gray-600">
              Utiliser la technologie pour faciliter les échanges culturels.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Section Technologies -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-4">
            Nos <span class="text-gradient">Technologies</span>
          </h2>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            Une plateforme moderne construite avec les meilleures technologies
          </p>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div class="text-center">
            <div class="w-20 h-20 bg-ukraine-blue/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-3xl">⚡</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Vue.js 3</h3>
            <p class="text-gray-600 text-sm">Interface moderne et réactive</p>
          </div>
          
          <div class="text-center">
            <div class="w-20 h-20 bg-ukraine-yellow/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-3xl">🎨</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Tailwind CSS</h3>
            <p class="text-gray-600 text-sm">Design moderne et responsive</p>
          </div>
          
          <div class="text-center">
            <div class="w-20 h-20 bg-ukraine-lightBlue/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-3xl">☕</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Spring Boot</h3>
            <p class="text-gray-600 text-sm">Backend robuste et sécurisé</p>
          </div>
          
          <div class="text-center">
            <div class="w-20 h-20 bg-ukraine-darkBlue/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-3xl">🗄️</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">MySQL</h3>
            <p class="text-gray-600 text-sm">Base de données performante</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Section Statistiques -->
    <section class="py-20 gradient-bg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-display font-bold text-white mb-4">
            Nos <span class="text-ukraine-yellow">Réalisations</span>
          </h2>
          <p class="text-xl text-white/90 max-w-3xl mx-auto">
            Des chiffres qui témoignent de notre impact sur la communauté
          </p>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div class="text-center">
            <div class="text-4xl md:text-5xl font-bold text-white mb-2">500+</div>
            <div class="text-white/80">Livres partagés</div>
          </div>
          <div class="text-center">
            <div class="text-4xl md:text-5xl font-bold text-white mb-2">200+</div>
            <div class="text-white/80">Membres actifs</div>
          </div>
          <div class="text-center">
            <div class="text-4xl md:text-5xl font-bold text-white mb-2">50+</div>
            <div class="text-white/80">Événements organisés</div>
          </div>
          <div class="text-center">
            <div class="text-4xl md:text-5xl font-bold text-white mb-2">5</div>
            <div class="text-white/80">Langues supportées</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section Contact -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-6">
          Rejoignez <span class="text-gradient">l'Aventure</span>
        </h2>
        <p class="text-xl text-gray-600 mb-8">
          Faites partie de notre communauté et contribuez à la promotion de la culture ukrainienne
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button class="btn-primary text-lg px-8 py-4">
            Commencer maintenant
          </button>
          <button class="btn-secondary text-lg px-8 py-4">
            En savoir plus
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import NavBar from '@/components/NavBar.vue'
</script>

<style scoped>
.font-display {
  font-family: 'Poppins', system-ui, sans-serif;
}
</style>
