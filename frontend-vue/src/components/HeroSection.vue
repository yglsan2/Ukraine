<template>
  <section
    class="relative min-h-screen flex items-center justify-center overflow-hidden gradient-bg"
  >
    <!-- Livres flottants -->
    <div class="absolute inset-0 pointer-events-none">
      <!-- Livre 1 -->
      <div class="floating-book top-20 left-10 animate-float-slow">
        <div class="w-16 h-20 bg-ukraine-blue rounded-lg shadow-lg transform rotate-12"></div>
      </div>

      <!-- Livre 2 -->
      <div class="floating-book top-40 right-20 animate-float">
        <div class="w-12 h-16 bg-ukraine-yellow rounded-lg shadow-lg transform -rotate-6"></div>
      </div>

      <!-- Livre 3 -->
      <div class="floating-book bottom-40 left-20 animate-float-fast">
        <div class="w-14 h-18 bg-white rounded-lg shadow-lg transform rotate-3"></div>
      </div>

      <!-- Livre 4 -->
      <div class="floating-book bottom-20 right-10 animate-float-slow">
        <div class="w-10 h-14 bg-ukraine-lightBlue rounded-lg shadow-lg transform -rotate-12"></div>
      </div>

      <!-- Livre 5 -->
      <div class="floating-book top-1/3 left-1/4 animate-float">
        <div class="w-8 h-12 bg-ukraine-darkYellow rounded-lg shadow-lg transform rotate-8"></div>
      </div>

      <!-- Livre 6 -->
      <div class="floating-book bottom-1/3 right-1/4 animate-float-fast">
        <div class="w-12 h-16 bg-ukraine-darkBlue rounded-lg shadow-lg transform -rotate-4"></div>
      </div>
    </div>

    <!-- Contenu principal -->
    <div class="relative z-10 text-center px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
      <div class="mb-8">
        <h1
          class="text-4xl sm:text-5xl lg:text-6xl font-display font-bold text-white mb-6 leading-tight"
        >
          <span class="block">Lumières</span>
          <span class="block text-ukraine-yellow">d'Ukraine</span>
        </h1>
        <p class="text-xl sm:text-2xl text-white/90 mb-8 max-w-2xl mx-auto leading-relaxed">
          Partagez la culture ukrainienne à travers les livres. Découvrez, échangez et
          connectez-vous avec des passionnés de lecture.
        </p>
      </div>

      <!-- Boutons d'action -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
        <button class="btn-primary text-lg px-8 py-4">
          <span class="flex items-center space-x-2">
            <span>📚</span>
            <span>Découvrir les livres</span>
          </span>
        </button>
        <button class="btn-secondary text-lg px-8 py-4">
          <span class="flex items-center space-x-2">
            <span>🤝</span>
            <span>Rejoindre l'association</span>
          </span>
        </button>
      </div>

      <!-- Statistiques -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-3xl mx-auto">
        <div class="glass-effect rounded-xl p-6 text-center">
          <div class="text-3xl font-bold text-white mb-2">500+</div>
          <div class="text-white/80">Livres partagés</div>
        </div>
        <div class="glass-effect rounded-xl p-6 text-center">
          <div class="text-3xl font-bold text-white mb-2">200+</div>
          <div class="text-white/80">Membres actifs</div>
        </div>
        <div class="glass-effect rounded-xl p-6 text-center">
          <div class="text-3xl font-bold text-white mb-2">50+</div>
          <div class="text-white/80">Événements organisés</div>
        </div>
      </div>
    </div>

    <!-- Scroll indicator -->
    <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce-slow">
      <div class="w-6 h-10 border-2 border-white/50 rounded-full flex justify-center">
        <div class="w-1 h-3 bg-white/70 rounded-full mt-2 animate-pulse"></div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
// Component logic here if needed
</script>

<style scoped>
.font-display {
  font-family: 'Poppins', system-ui, sans-serif;
}
</style>
