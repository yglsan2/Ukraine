<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navbar -->
    <NavBar />

    <!-- Header -->
    <div class="pt-20 pb-12 bg-gradient-to-r from-ukraine-darkBlue to-ukraine-blue">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl sm:text-5xl font-display font-bold text-white mb-4">
            {{ t('about.title') }}
          </h1>
          <p class="text-xl text-white/90 max-w-3xl mx-auto">
            {{ t('about.description') }}
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
              {{ t('about.history.title') }}
            </h2>
            <p class="text-lg text-gray-600 mb-6">
              {{ t('about.history.description1') }}
            </p>
            <p class="text-lg text-gray-600 mb-6">
              {{ t('about.history.description2') }}
            </p>
            <p class="text-lg text-gray-600">
              {{ t('about.history.description3') }}
            </p>
          </div>
          <div class="relative">
            <div
              class="bg-gradient-to-br from-ukraine-blue/20 to-ukraine-yellow/20 rounded-2xl p-8"
            >
              <div class="text-center">
                <span class="text-6xl mb-4 block">📖</span>
                <h3 class="text-2xl font-semibold text-gray-900 mb-4">
                  {{ t('about.vision.book.title') }}
                </h3>
                <p class="text-gray-600">
                  {{ t('about.vision.book.description') }}
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
            {{ t('about.vision.title') }}
          </h2>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            {{ t('about.vision.description') }}
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="card p-8 text-center">
            <div
              class="w-16 h-16 bg-ukraine-blue/10 rounded-full flex items-center justify-center mx-auto mb-6"
            >
              <span class="text-3xl">🌍</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">
              {{ t('about.vision.accessibility.title') }}
            </h3>
            <p class="text-gray-600">
              {{ t('about.vision.accessibility.description') }}
            </p>
          </div>

          <div class="card p-8 text-center">
            <div
              class="w-16 h-16 bg-ukraine-yellow/10 rounded-full flex items-center justify-center mx-auto mb-6"
            >
              <span class="text-3xl">🤝</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">
              {{ t('about.vision.community.title') }}
            </h3>
            <p class="text-gray-600">
              {{ t('about.vision.community.description') }}
            </p>
          </div>

          <div class="card p-8 text-center">
            <div
              class="w-16 h-16 bg-ukraine-lightBlue/10 rounded-full flex items-center justify-center mx-auto mb-6"
            >
              <span class="text-3xl">💡</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-4">
              {{ t('about.vision.innovation.title') }}
            </h3>
            <p class="text-gray-600">
              {{ t('about.vision.innovation.description') }}
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
            {{ t('about.technologies.title') }}
          </h2>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            {{ t('about.technologies.description') }}
          </p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div class="text-center">
            <div
              class="w-20 h-20 bg-ukraine-blue/10 rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <span class="text-3xl">⚡</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              {{ t('about.technologies.vue.title') }}
            </h3>
            <p class="text-gray-600 text-sm">
              {{ t('about.technologies.vue.description') }}
            </p>
          </div>

          <div class="text-center">
            <div
              class="w-20 h-20 bg-ukraine-yellow/10 rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <span class="text-3xl">🎨</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              {{ t('about.technologies.tailwind.title') }}
            </h3>
            <p class="text-gray-600 text-sm">
              {{ t('about.technologies.tailwind.description') }}
            </p>
          </div>

          <div class="text-center">
            <div
              class="w-20 h-20 bg-ukraine-lightBlue/10 rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <span class="text-3xl">☕</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              {{ t('about.technologies.spring.title') }}
            </h3>
            <p class="text-gray-600 text-sm">
              {{ t('about.technologies.spring.description') }}
            </p>
          </div>

          <div class="text-center">
            <div
              class="w-20 h-20 bg-ukraine-darkBlue/10 rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <span class="text-3xl">🗄️</span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">
              {{ t('about.technologies.mysql.title') }}
            </h3>
            <p class="text-gray-600 text-sm">
              {{ t('about.technologies.mysql.description') }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Section Statistiques -->
    <section class="py-20 gradient-bg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl sm:text-4xl font-display font-bold text-white mb-4">
            {{ t('about.achievements.title') }}
          </h2>
          <p class="text-xl text-white/90 max-w-3xl mx-auto">
            {{ t('about.achievements.description') }}
          </p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div class="text-center">
            <div class="text-4xl md:text-5xl font-bold text-white mb-2">500+</div>
            <div class="text-white/80">
              {{ t('about.achievements.books') }}
            </div>
          </div>
          <div class="text-center">
            <div class="text-4xl md:text-5xl font-bold text-white mb-2">200+</div>
            <div class="text-white/80">
              {{ t('about.achievements.members') }}
            </div>
          </div>
          <div class="text-center">
            <div class="text-4xl md:text-5xl font-bold text-white mb-2">50+</div>
            <div class="text-white/80">
              {{ t('about.achievements.events') }}
            </div>
          </div>
          <div class="text-center">
            <div class="text-4xl md:text-5xl font-bold text-white mb-2">5</div>
            <div class="text-white/80">
              {{ t('about.achievements.languages') }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section Contact -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-6">
          {{ t('about.join.title') }}
        </h2>
        <p class="text-xl text-gray-600 mb-8">
          {{ t('about.join.description') }}
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button class="btn-primary text-lg px-8 py-4">
            {{ t('about.join.cta1') }}
          </button>
          <button class="btn-secondary text-lg px-8 py-4">
            {{ t('about.join.cta2') }}
          </button>
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
