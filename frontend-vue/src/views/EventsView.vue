<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navbar -->
    <NavBar />
    
    <!-- Header -->
    <div class="pt-20 pb-12 bg-gradient-to-r from-ukraine-yellow to-ukraine-darkYellow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl sm:text-5xl font-display font-bold text-ukraine-darkBlue mb-4">
            Événements <span class="text-ukraine-blue">Culturels</span>
          </h1>
          <p class="text-xl text-ukraine-darkBlue/90 max-w-3xl mx-auto">
            Découvrez et participez à nos événements littéraires et culturels ukrainiens
          </p>
        </div>
      </div>
    </div>

    <!-- Filtres -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex flex-col lg:flex-row gap-4 items-center justify-between">
          <div class="flex flex-wrap gap-3">
            <button
              v-for="filter in filters"
              :key="filter.value"
              @click="selectedFilter = filter.value"
              class="px-4 py-2 rounded-lg font-medium transition-all duration-300"
              :class="selectedFilter === filter.value 
                ? 'bg-ukraine-blue text-white' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            >
              {{ filter.label }}
            </button>
          </div>
          
          <button class="btn-primary">
            <span class="flex items-center space-x-2">
              <span>🎉</span>
              <span>Proposer un événement</span>
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Grille des événements -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Événements à venir -->
      <div class="mb-16">
        <h2 class="text-2xl font-display font-bold text-gray-900 mb-8">
          Événements à venir
        </h2>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div
            v-for="event in upcomingEvents"
            :key="event.id"
            class="card overflow-hidden group cursor-pointer"
          >
            <!-- Image de l'événement -->
            <div class="relative h-48 bg-gradient-to-br from-ukraine-blue/20 to-ukraine-yellow/20 flex items-center justify-center">
              <span class="text-6xl">🎭</span>
              <div class="absolute top-4 right-4">
                <span class="px-3 py-1 text-sm font-medium bg-ukraine-blue text-white rounded-full">
                  {{ event.type }}
                </span>
              </div>
            </div>

            <!-- Contenu -->
            <div class="p-6">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-xl font-semibold text-gray-900 group-hover:text-ukraine-blue transition-colors">
                  {{ event.title }}
                </h3>
                <span class="text-ukraine-blue font-medium">{{ event.date }}</span>
              </div>
              
              <p class="text-gray-600 mb-4">{{ event.description }}</p>
              
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center space-x-2 text-gray-500">
                  <span>📍</span>
                  <span>{{ event.location }}</span>
                </div>
                <div class="flex items-center space-x-2 text-gray-500">
                  <span>👥</span>
                  <span>{{ event.participants }} participants</span>
                </div>
              </div>

              <div class="flex items-center justify-between">
                <button class="btn-primary text-sm px-4 py-2">
                  S'inscrire
                </button>
                <button class="text-ukraine-blue hover:text-ukraine-darkBlue transition-colors">
                  <span class="text-lg">📅</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Événements passés -->
      <div>
        <h2 class="text-2xl font-display font-bold text-gray-900 mb-8">
          Événements passés
        </h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="event in pastEvents"
            :key="event.id"
            class="card overflow-hidden group cursor-pointer opacity-75 hover:opacity-100 transition-opacity"
          >
            <!-- Image de l'événement -->
            <div class="relative h-32 bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center">
              <span class="text-4xl">📚</span>
              <div class="absolute top-2 right-2">
                <span class="px-2 py-1 text-xs font-medium bg-gray-500 text-white rounded-full">
                  Terminé
                </span>
              </div>
            </div>

            <!-- Contenu -->
            <div class="p-4">
              <h3 class="text-lg font-semibold text-gray-900 mb-2">
                {{ event.title }}
              </h3>
              <p class="text-sm text-gray-600 mb-3">{{ event.description }}</p>
              
              <div class="flex items-center justify-between text-sm text-gray-500">
                <span>{{ event.date }}</span>
                <span>{{ event.participants }} participants</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import NavBar from '@/components/NavBar.vue'

const selectedFilter = ref('all')

const filters = [
  { label: 'Tous', value: 'all' },
  { label: 'Lectures', value: 'lecture' },
  { label: 'Conférences', value: 'conference' },
  { label: 'Ateliers', value: 'workshop' },
  { label: 'Expositions', value: 'exhibition' }
]

const upcomingEvents = ref([
  {
    id: 1,
    title: 'Soirée Poésie Ukrainienne',
    description: 'Une soirée dédiée à la poésie ukrainienne avec lectures et discussions.',
    date: '15 Déc 2024',
    location: 'Paris, France',
    type: 'Lecture',
    participants: 45
  },
  {
    id: 2,
    title: 'Conférence sur Taras Chevtchenko',
    description: 'Découvrez la vie et l\'œuvre du grand poète ukrainien Taras Chevtchenko.',
    date: '20 Déc 2024',
    location: 'Lyon, France',
    type: 'Conférence',
    participants: 78
  },
  {
    id: 3,
    title: 'Atelier de Calligraphie Ukrainienne',
    description: 'Apprenez l\'art de la calligraphie ukrainienne traditionnelle.',
    date: '25 Déc 2024',
    location: 'Marseille, France',
    type: 'Atelier',
    participants: 23
  },
  {
    id: 4,
    title: 'Exposition Littérature Jeunesse',
    description: 'Exposition de livres pour enfants ukrainiens avec animations.',
    date: '30 Déc 2024',
    location: 'Toulouse, France',
    type: 'Exposition',
    participants: 120
  }
])

const pastEvents = ref([
  {
    id: 5,
    title: 'Festival de la Culture Ukrainienne',
    description: 'Grand festival célébrant la culture ukrainienne.',
    date: '10 Nov 2024',
    participants: 250
  },
  {
    id: 6,
    title: 'Lecture de Contes Traditionnels',
    description: 'Lecture de contes ukrainiens pour enfants.',
    date: '5 Nov 2024',
    participants: 35
  },
  {
    id: 7,
    title: 'Conférence sur l\'Histoire de l\'Ukraine',
    description: 'Conférence sur l\'histoire riche de l\'Ukraine.',
    date: '1 Nov 2024',
    participants: 89
  }
])
</script>

<style scoped>
.font-display {
  font-family: 'Poppins', system-ui, sans-serif;
}
</style> 