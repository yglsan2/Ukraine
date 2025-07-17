<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navbar -->
    <NavBar />
    
    <!-- Header -->
    <div class="pt-20 pb-12 bg-gradient-to-r from-ukraine-blue to-ukraine-lightBlue">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl sm:text-5xl font-display font-bold text-white mb-4">
            Bibliothèque <span class="text-ukraine-yellow">Ukrainienne</span>
          </h1>
          <p class="text-xl text-white/90 max-w-3xl mx-auto">
            Découvrez notre collection de livres ukrainiens partagés par la communauté
          </p>
        </div>
      </div>
    </div>

    <!-- Filtres et recherche -->
    <div class="bg-white border-b border-gray-200 sticky top-16 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex flex-col lg:flex-row gap-4 items-center justify-between">
          <!-- Barre de recherche -->
          <div class="relative flex-1 max-w-md">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Rechercher un livre..."
              class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
            >
            <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">🔍</span>
          </div>

          <!-- Filtres -->
          <div class="flex flex-wrap gap-3">
            <select
              v-model="selectedCategory"
              class="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
            >
              <option value="">Toutes les catégories</option>
              <option value="roman">Roman</option>
              <option value="poesie">Poésie</option>
              <option value="histoire">Histoire</option>
              <option value="culture">Culture</option>
              <option value="jeunesse">Jeunesse</option>
            </select>

            <select
              v-model="selectedLanguage"
              class="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
            >
              <option value="">Toutes les langues</option>
              <option value="ukrainien">Ukrainien</option>
              <option value="francais">Français</option>
              <option value="anglais">Anglais</option>
              <option value="allemand">Allemand</option>
            </select>

            <button class="btn-primary">
              <span class="flex items-center space-x-2">
                <span>📚</span>
                <span>Ajouter un livre</span>
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Grille des livres -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Statistiques -->
      <div class="mb-8 text-center">
        <p class="text-gray-600">
          {{ filteredBooks.length }} livre{{ filteredBooks.length > 1 ? 's' : '' }} trouvé{{ filteredBooks.length > 1 ? 's' : '' }}
        </p>
      </div>

      <!-- Grille -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div
          v-for="book in filteredBooks"
          :key="book.id"
          class="card group cursor-pointer"
        >
          <!-- Image du livre -->
          <div class="relative overflow-hidden rounded-t-xl">
            <div class="aspect-[3/4] bg-gradient-to-br from-ukraine-blue/20 to-ukraine-yellow/20 flex items-center justify-center">
              <span class="text-6xl">📖</span>
            </div>
            <div class="absolute top-3 right-3">
              <span class="px-2 py-1 text-xs font-medium rounded-full"
                :class="{
                  'bg-ukraine-blue/20 text-ukraine-blue': book.language === 'ukrainien',
                  'bg-ukraine-yellow/20 text-ukraine-darkYellow': book.language === 'francais',
                  'bg-green-100 text-green-800': book.language === 'anglais',
                  'bg-purple-100 text-purple-800': book.language === 'allemand'
                }"
              >
                {{ book.language }}
              </span>
            </div>
          </div>

          <!-- Informations du livre -->
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-2 group-hover:text-ukraine-blue transition-colors">
              {{ book.title }}
            </h3>
            <p class="text-gray-600 mb-3">{{ book.author }}</p>
            
            <div class="flex items-center justify-between mb-4">
              <span class="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-700 rounded-full">
                {{ book.category }}
              </span>
              <div class="flex items-center space-x-1 text-yellow-400">
                <span v-for="i in 5" :key="i" class="text-sm">⭐</span>
              </div>
            </div>

            <p class="text-sm text-gray-500 mb-4 line-clamp-2">
              {{ book.description }}
            </p>

            <!-- Actions -->
            <div class="flex items-center justify-between">
              <button class="btn-primary text-sm px-4 py-2">
                Réserver
              </button>
              <button class="text-ukraine-blue hover:text-ukraine-darkBlue transition-colors">
                <span class="text-lg">💬</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div class="mt-12 flex justify-center">
        <nav class="flex items-center space-x-2">
          <button class="px-3 py-2 text-gray-500 hover:text-ukraine-blue transition-colors">
            ← Précédent
          </button>
          <button class="px-3 py-2 bg-ukraine-blue text-white rounded-lg">1</button>
          <button class="px-3 py-2 text-gray-700 hover:text-ukraine-blue transition-colors">2</button>
          <button class="px-3 py-2 text-gray-700 hover:text-ukraine-blue transition-colors">3</button>
          <button class="px-3 py-2 text-gray-500 hover:text-ukraine-blue transition-colors">
            Suivant →
          </button>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import NavBar from '@/components/NavBar.vue'

const searchQuery = ref('')
const selectedCategory = ref('')
const selectedLanguage = ref('')

// Données de test
const books = ref([
  {
    id: 1,
    title: 'Les Champs de la Mort',
    author: 'Vassyl Barka',
    category: 'roman',
    language: 'ukrainien',
    description: 'Un roman poignant sur la famine en Ukraine dans les années 1930.'
  },
  {
    id: 2,
    title: 'Poèmes de la Liberté',
    author: 'Taras Chevtchenko',
    category: 'poesie',
    language: 'ukrainien',
    description: 'Recueil de poèmes célébrant la liberté et l\'indépendance ukrainienne.'
  },
  {
    id: 3,
    title: 'Histoire de l\'Ukraine',
    author: 'Mykhailo Hrushevsky',
    category: 'histoire',
    language: 'francais',
    description: 'Une histoire complète de l\'Ukraine de ses origines à nos jours.'
  },
  {
    id: 4,
    title: 'Contes Ukrainiens',
    author: 'Ivan Franko',
    category: 'jeunesse',
    language: 'ukrainien',
    description: 'Recueil de contes traditionnels ukrainiens pour enfants.'
  },
  {
    id: 5,
    title: 'La Culture Ukrainienne',
    author: 'Dmytro Chyzhevsky',
    category: 'culture',
    language: 'anglais',
    description: 'Exploration approfondie de la culture et des traditions ukrainiennes.'
  },
  {
    id: 6,
    title: 'Les Fleurs du Donbass',
    author: 'Volodymyr Sosiura',
    category: 'poesie',
    language: 'ukrainien',
    description: 'Poèmes inspirés par la région du Donbass et ses habitants.'
  }
])

const filteredBooks = computed(() => {
  return books.value.filter(book => {
    const matchesSearch = !searchQuery.value || 
      book.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      book.author.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesCategory = !selectedCategory.value || book.category === selectedCategory.value
    const matchesLanguage = !selectedLanguage.value || book.language === selectedLanguage.value
    
    return matchesSearch && matchesCategory && matchesLanguage
  })
})
</script>

<style scoped>
.font-display {
  font-family: 'Poppins', system-ui, sans-serif;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 