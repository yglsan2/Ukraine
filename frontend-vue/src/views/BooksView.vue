<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navbar -->
    <NavBar />
    
    <!-- Header -->
    <div class="pt-20 pb-12 bg-gradient-to-r from-ukraine-blue to-ukraine-lightBlue">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl sm:text-5xl font-display font-bold text-white mb-4">
            {{ t('books.title') }}
          </h1>
          <p class="text-xl text-white/90 max-w-3xl mx-auto">
            {{ t('books.subtitle') }}
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
              :placeholder="t('books.search')"
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
              <option value="">{{ t('books.filters.allCategories') }}</option>
              <option value="roman">{{ t('books.filters.categories.novel') }}</option>
              <option value="poesie">{{ t('books.filters.categories.poetry') }}</option>
              <option value="histoire">{{ t('books.filters.categories.history') }}</option>
              <option value="culture">{{ t('books.filters.categories.culture') }}</option>
              <option value="jeunesse">{{ t('books.filters.categories.youth') }}</option>
              <option value="politique">{{ t('books.filters.categories.politics') }}</option>
              <option value="art">{{ t('books.filters.categories.art') }}</option>
            </select>

            <select
              v-model="selectedLanguage"
              class="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
            >
              <option value="">{{ t('books.filters.allLanguages') }}</option>
              <option value="ukrainien">{{ t('books.filters.languages.ukrainian') }}</option>
              <option value="francais">{{ t('books.filters.languages.french') }}</option>
              <option value="anglais">{{ t('books.filters.languages.english') }}</option>
              <option value="allemand">{{ t('books.filters.languages.german') }}</option>
            </select>

            <button @click="showAddBookModal = true" class="btn-primary">
              <span class="flex items-center space-x-2">
                <span>📚</span>
                <span>{{ t('books.addBook') }}</span>
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
          {{ filteredBooks.length }} {{ t('book') }}{{ filteredBooks.length > 1 ? 's' : '' }} {{ t('found') }}{{ filteredBooks.length > 1 ? 's' : '' }}
        </p>
      </div>

      <!-- Grille -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div
          v-for="book in filteredBooks"
          :key="book.id"
          class="card group cursor-pointer transform hover:scale-105 transition-all duration-300"
          @click="showBookDetails(book)"
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
            <div class="absolute bottom-3 left-3">
              <span class="px-2 py-1 text-xs font-medium bg-white/90 text-gray-700 rounded-full">
                {{ book.condition }}
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
              <button 
                @click.stop="reserveBook(book)"
                class="btn-primary text-sm px-4 py-2"
                :disabled="book.reserved"
              >
                {{ book.reserved ? t('books.book.reserved') : t('books.book.reserve') }}
              </button>
              <button 
                @click.stop="showBookDetails(book)"
                class="text-ukraine-blue hover:text-ukraine-darkBlue transition-colors"
              >
                <span class="text-lg">👁️</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div class="mt-12 flex justify-center">
        <nav class="flex items-center space-x-2">
          <button 
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="px-3 py-2 text-gray-500 hover:text-ukraine-blue transition-colors disabled:opacity-50"
          >
            {{ t('actions.previous') }}
          </button>
          <button 
            v-for="page in totalPages" 
            :key="page"
            @click="currentPage = page"
            :class="[
              'px-3 py-2 rounded-lg transition-colors',
              currentPage === page 
                ? 'bg-ukraine-blue text-white' 
                : 'text-gray-700 hover:text-ukraine-blue'
            ]"
          >
            {{ page }}
          </button>
          <button 
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="px-3 py-2 text-gray-500 hover:text-ukraine-blue transition-colors disabled:opacity-50"
          >
            {{ t('actions.next') }} →
          </button>
        </nav>
      </div>
    </div>

    <!-- Modal Ajouter un livre -->
    <div v-if="showAddBookModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-gray-900">{{ t('books.modal.addBook') }}</h3>
            <button @click="showAddBookModal = false" class="text-gray-400 hover:text-gray-600">
              <span class="text-2xl">×</span>
            </button>
          </div>
        </div>
        
        <form @submit.prevent="addBook" class="p-6 space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('books.modal.form.title') }} *</label>
              <input
                v-model="newBook.title"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('books.modal.form.author') }} *</label>
              <input
                v-model="newBook.author"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('books.modal.form.category') }} *</label>
              <select
                v-model="newBook.category"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              >
                <option value="">{{ t('books.modal.form.selectCategory') }}</option>
                <option value="roman">{{ t('roman') }}</option>
                <option value="poesie">{{ t('poesie') }}</option>
                <option value="histoire">{{ t('histoire') }}</option>
                <option value="culture">{{ t('culture') }}</option>
                <option value="jeunesse">{{ t('jeunesse') }}</option>
                <option value="politique">{{ t('politique') }}</option>
                <option value="art">{{ t('art') }}</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('language') }} *</label>
              <select
                v-model="newBook.language"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              >
                <option value="">{{ t('selectLanguage') }}</option>
                <option value="ukrainien">{{ t('ukrainien') }}</option>
                <option value="francais">{{ t('francais') }}</option>
                <option value="anglais">{{ t('anglais') }}</option>
                <option value="allemand">{{ t('allemand') }}</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('condition') }} *</label>
              <select
                v-model="newBook.condition"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              >
                <option value="">{{ t('selectCondition') }}</option>
                <option value="Excellent">{{ t('excellent') }}</option>
                <option value="Très bon">{{ t('veryGood') }}</option>
                <option value="Bon">{{ t('good') }}</option>
                <option value="Moyen">{{ t('average') }}</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('publicationYear') }}</label>
              <input
                v-model="newBook.year"
                type="number"
                min="1800"
                max="2024"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              >
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('description') }}</label>
            <textarea
              v-model="newBook.description"
              rows="4"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              placeholder="Description du livre..."
            ></textarea>
          </div>
          
          <div class="flex justify-end space-x-4 pt-4">
            <button
              type="button"
              @click="showAddBookModal = false"
              class="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              {{ t('cancel') }}
            </button>
            <button
              type="submit"
              class="btn-primary px-6 py-3"
            >
              {{ t('addBook') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Détails du livre -->
    <div v-if="selectedBook" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-gray-900">{{ t('bookDetails') }}</h3>
            <button @click="selectedBook = null" class="text-gray-400 hover:text-gray-600">
              <span class="text-2xl">×</span>
            </button>
          </div>
        </div>
        
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <!-- Image -->
            <div class="md:col-span-1">
              <div class="aspect-[3/4] bg-gradient-to-br from-ukraine-blue/20 to-ukraine-yellow/20 rounded-xl flex items-center justify-center">
                <span class="text-8xl">📖</span>
              </div>
            </div>
            
            <!-- Informations -->
            <div class="md:col-span-2 space-y-6">
              <div>
                <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ selectedBook.title }}</h2>
                <p class="text-lg text-gray-600 mb-4">{{ t('by') }} {{ selectedBook.author }}</p>
                
                <div class="flex flex-wrap gap-2 mb-4">
                  <span class="px-3 py-1 text-sm font-medium bg-ukraine-blue/20 text-ukraine-blue rounded-full">
                    {{ selectedBook.category }}
                  </span>
                  <span class="px-3 py-1 text-sm font-medium bg-ukraine-yellow/20 text-ukraine-darkYellow rounded-full">
                    {{ selectedBook.language }}
                  </span>
                  <span class="px-3 py-1 text-sm font-medium bg-green-100 text-green-800 rounded-full">
                    {{ selectedBook.condition }}
                  </span>
                  <span v-if="selectedBook.year" class="px-3 py-1 text-sm font-medium bg-purple-100 text-purple-800 rounded-full">
                    {{ selectedBook.year }}
                  </span>
                </div>
              </div>
              
              <div>
                <h4 class="text-lg font-semibold text-gray-900 mb-2">{{ t('description') }}</h4>
                <p class="text-gray-600">{{ selectedBook.description }}</p>
              </div>
              
              <div class="flex items-center justify-between pt-4">
                <button 
                  @click="reserveBook(selectedBook)"
                  class="btn-primary px-6 py-3"
                  :disabled="selectedBook.reserved"
                >
                  {{ selectedBook.reserved ? t('alreadyReserved') : t('reserveThisBook') }}
                </button>
                
                <div class="flex items-center space-x-4">
                  <span class="text-sm text-gray-500">
                    {{ t('addedOn') }} {{ formatDate(selectedBook.addedDate) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import NavBar from '@/components/NavBar.vue'

const { t } = useI18n()

const searchQuery = ref('')
const selectedCategory = ref('')
const selectedLanguage = ref('')
const showAddBookModal = ref(false)
const selectedBook = ref(null)
const currentPage = ref(1)
const itemsPerPage = 12

// Nouveau livre
const newBook = ref({
  title: '',
  author: '',
  category: '',
  language: '',
  condition: '',
  year: '',
  description: ''
})

// Données de test enrichies
const books = ref([
  {
    id: 1,
    title: 'Les Champs de la Mort',
    author: 'Vassyl Barka',
    category: 'roman',
    language: 'ukrainien',
    condition: 'Très bon',
    year: 1963,
    description: 'Un roman poignant sur la famine en Ukraine dans les années 1930, connu sous le nom d\'Holodomor. L\'auteur décrit avec une précision historique et une sensibilité littéraire les souffrances du peuple ukrainien.',
    reserved: false,
    addedDate: '2024-01-15'
  },
  {
    id: 2,
    title: 'Poèmes de la Liberté',
    author: 'Taras Chevtchenko',
    category: 'poesie',
    language: 'ukrainien',
    condition: 'Excellent',
    year: 1840,
    description: 'Recueil de poèmes célébrant la liberté et l\'indépendance ukrainienne. Chevtchenko, considéré comme le père de la littérature ukrainienne moderne, exprime l\'âme et les aspirations du peuple ukrainien.',
    reserved: false,
    addedDate: '2024-01-10'
  },
  {
    id: 3,
    title: 'Histoire de l\'Ukraine',
    author: 'Mykhailo Hrushevsky',
    category: 'histoire',
    language: 'francais',
    condition: 'Bon',
    year: 1913,
    description: 'Une histoire complète de l\'Ukraine de ses origines à nos jours. Cette œuvre monumentale reste une référence incontournable pour comprendre l\'histoire ukrainienne.',
    reserved: true,
    addedDate: '2024-01-05'
  },
  {
    id: 4,
    title: 'Contes Ukrainiens',
    author: 'Ivan Franko',
    category: 'jeunesse',
    language: 'ukrainien',
    condition: 'Moyen',
    year: 1890,
    description: 'Recueil de contes traditionnels ukrainiens pour enfants. Ces histoires transmettent les valeurs et la culture ukrainienne aux plus jeunes.',
    reserved: false,
    addedDate: '2024-01-20'
  },
  {
    id: 5,
    title: 'La Culture Ukrainienne',
    author: 'Dmytro Chyzhevsky',
    category: 'culture',
    language: 'anglais',
    condition: 'Excellent',
    year: 1955,
    description: 'Exploration approfondie de la culture et des traditions ukrainiennes. L\'auteur analyse les influences byzantines, slaves et européennes sur la culture ukrainienne.',
    reserved: false,
    addedDate: '2024-01-12'
  },
  {
    id: 6,
    title: 'Les Fleurs du Donbass',
    author: 'Volodymyr Sosiura',
    category: 'poesie',
    language: 'ukrainien',
    condition: 'Très bon',
    year: 1928,
    description: 'Poèmes inspirés par la région du Donbass et ses habitants. L\'auteur célèbre la beauté de cette terre et la résilience de son peuple.',
    reserved: false,
    addedDate: '2024-01-18'
  },
  {
    id: 7,
    title: 'L\'Ukraine et l\'Europe',
    author: 'Mykola Kostomarov',
    category: 'politique',
    language: 'francais',
    condition: 'Bon',
    year: 1860,
    description: 'Analyse des relations entre l\'Ukraine et l\'Europe à travers l\'histoire. L\'auteur examine les influences mutuelles et les perspectives d\'avenir.',
    reserved: false,
    addedDate: '2024-01-08'
  },
  {
    id: 8,
    title: 'L\'Art Ukrainien Moderne',
    author: 'Oleksandr Murashko',
    category: 'art',
    language: 'ukrainien',
    condition: 'Excellent',
    year: 1910,
    description: 'Présentation de l\'art ukrainien moderne et de ses représentants. L\'ouvrage inclut de nombreuses reproductions d\'œuvres d\'art.',
    reserved: false,
    addedDate: '2024-01-22'
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

const paginatedBooks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredBooks.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredBooks.value.length / itemsPerPage)
})

function showBookDetails(book) {
  selectedBook.value = book
}

function reserveBook(book) {
  if (!book.reserved) {
    book.reserved = true
    window.$notify?.success(t('bookReserved'), `${book.title} ${t('addedToReservations')}`)
  }
}

function addBook() {
  const book = {
    id: books.value.length + 1,
    ...newBook.value,
    reserved: false,
    addedDate: new Date().toISOString().split('T')[0]
  }
  
  books.value.push(book)
  showAddBookModal.value = false
  
  window.$notify?.success(t('bookAdded'), `${book.title} ${t('addedToLibrary')}`)
  
  // Reset form
  newBook.value = {
    title: '',
    author: '',
    category: '',
    language: '',
    condition: '',
    year: '',
    description: ''
  }
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
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