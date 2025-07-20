<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navbar -->
    <NavBar />

    <!-- Header -->
    <div class="pt-20 pb-12 gradient-bg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl sm:text-5xl font-display font-bold text-white mb-4">
            Notre <span class="text-ukraine-yellow">Association</span>
          </h1>
          <p class="text-xl text-white/90 max-w-3xl mx-auto">
            Découvrez notre mission et notre engagement pour la culture ukrainienne
          </p>
        </div>
      </div>
    </div>

    <!-- Section Mission -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-6">
              Notre <span class="text-gradient">Mission</span>
            </h2>
            <p class="text-lg text-gray-600 mb-6">
              L'association Lumières d'Ukraine a pour mission de promouvoir et partager la richesse
              de la culture ukrainienne à travers la littérature et les échanges culturels.
            </p>
            <p class="text-lg text-gray-600 mb-8">
              Nous croyons au pouvoir des livres pour rapprocher les peuples et faire découvrir la
              beauté de la culture ukrainienne au monde entier.
            </p>
            <button class="btn-primary text-lg px-8 py-4">Rejoindre l'association</button>
          </div>
          <div class="relative">
            <div
              class="bg-gradient-to-br from-ukraine-blue/20 to-ukraine-yellow/20 rounded-2xl p-8"
            >
              <div class="text-center">
                <span class="text-8xl mb-4 block">💙💛</span>
                <h3 class="text-2xl font-semibold text-gray-900 mb-4">Ensemble pour l'Ukraine</h3>
                <p class="text-gray-600">
                  Soutenons ensemble la culture ukrainienne et partageons sa beauté avec le monde.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section Valeurs -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-4">
            Nos <span class="text-gradient">Valeurs</span>
          </h2>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            Les principes qui guident nos actions et notre engagement
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div class="card p-8 text-center">
            <div
              class="w-16 h-16 bg-ukraine-blue/10 rounded-full flex items-center justify-center mx-auto mb-6"
            >
              <span class="text-3xl">🤝</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">Solidarité</h3>
            <p class="text-gray-600">
              Nous soutenons la communauté ukrainienne et promouvons l'entraide entre nos membres.
            </p>
          </div>

          <div class="card p-8 text-center">
            <div
              class="w-16 h-16 bg-ukraine-yellow/10 rounded-full flex items-center justify-center mx-auto mb-6"
            >
              <span class="text-3xl">🌍</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">Ouverture</h3>
            <p class="text-gray-600">
              Nous accueillons tous ceux qui souhaitent découvrir et partager la culture
              ukrainienne.
            </p>
          </div>

          <div class="card p-8 text-center">
            <div
              class="w-16 h-16 bg-ukraine-lightBlue/10 rounded-full flex items-center justify-center mx-auto mb-6"
            >
              <span class="text-3xl">📚</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">Culture</h3>
            <p class="text-gray-600">
              Nous valorisons la littérature et l'éducation comme vecteurs de compréhension
              mutuelle.
            </p>
          </div>

          <div class="card p-8 text-center">
            <div
              class="w-16 h-16 bg-ukraine-darkBlue/10 rounded-full flex items-center justify-center mx-auto mb-6"
            >
              <span class="text-3xl">🕊️</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">Paix</h3>
            <p class="text-gray-600">
              Nous œuvrons pour la paix et la compréhension entre les peuples.
            </p>
          </div>

          <div class="card p-8 text-center">
            <div
              class="w-16 h-16 bg-ukraine-darkYellow/10 rounded-full flex items-center justify-center mx-auto mb-6"
            >
              <span class="text-3xl">💡</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">Innovation</h3>
            <p class="text-gray-600">
              Nous utilisons les technologies modernes pour faciliter les échanges culturels.
            </p>
          </div>

          <div class="card p-8 text-center">
            <div
              class="w-16 h-16 bg-gradient-to-br from-ukraine-blue/10 to-ukraine-yellow/10 rounded-full flex items-center justify-center mx-auto mb-6"
            >
              <span class="text-3xl">🌟</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">Excellence</h3>
            <p class="text-gray-600">
              Nous visons l'excellence dans tous nos projets et événements culturels.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Section Équipe -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-4">
            Notre <span class="text-gradient">Équipe</span>
          </h2>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            Des passionnés dédiés à la promotion de la culture ukrainienne
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div class="card p-6 text-center">
            <div
              class="w-24 h-24 bg-gradient-to-br from-ukraine-blue to-ukraine-yellow rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <span class="text-3xl text-white">👨‍💼</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Oleksandr Petrov</h3>
            <p class="text-ukraine-blue font-medium mb-3">Président</p>
            <p class="text-gray-600 text-sm">
              Passionné de littérature ukrainienne et engagé pour la promotion de sa culture.
            </p>
          </div>

          <div class="card p-6 text-center">
            <div
              class="w-24 h-24 bg-gradient-to-br from-ukraine-yellow to-ukraine-blue rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <span class="text-3xl text-white">👩‍💼</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Maria Kovalenko</h3>
            <p class="text-ukraine-blue font-medium mb-3">Vice-Présidente</p>
            <p class="text-gray-600 text-sm">
              Spécialiste en événements culturels et coordinatrice de nos activités.
            </p>
          </div>

          <div class="card p-6 text-center">
            <div
              class="w-24 h-24 bg-gradient-to-br from-ukraine-lightBlue to-ukraine-yellow rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <span class="text-3xl text-white">👨‍💻</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Dmytro Ivanov</h3>
            <p class="text-ukraine-blue font-medium mb-3">Directeur Technique</p>
            <p class="text-gray-600 text-sm">
              Expert en développement web et responsable de notre plateforme numérique.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Section Contact -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-6">
          Contactez <span class="text-gradient">l'Association</span>
        </h2>
        <p class="text-xl text-gray-600 mb-8">
          Vous souhaitez nous rejoindre ou en savoir plus sur nos activités ?
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button class="btn-primary text-lg px-8 py-4">Nous contacter</button>
          <button class="btn-secondary text-lg px-8 py-4">Devenir membre</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import NavBar from '@/components/NavBar.vue'

const { t } = useI18n()
</script>

<style scoped>
.font-display {
  font-family: 'Poppins', system-ui, sans-serif;
}
</style>
