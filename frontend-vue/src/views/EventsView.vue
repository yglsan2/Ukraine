<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navbar -->
    <NavBar />
    
    <!-- Header -->
    <div class="pt-20 pb-12 bg-gradient-to-r from-ukraine-blue to-ukraine-lightBlue">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl sm:text-5xl font-display font-bold text-white mb-4">
            {{ t('events.title') }}
          </h1>
          <p class="text-xl text-white/90 max-w-3xl mx-auto">
            {{ t('events.subtitle') }}
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
              :placeholder="t('events.search')"
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
              <option value="">{{ t('events.filters.allCategories') }}</option>
              <option value="culture">{{ t('events.filters.categories.culture') }}</option>
              <option value="education">{{ t('events.filters.categories.education') }}</option>
              <option value="solidarite">{{ t('events.filters.categories.solidarite') }}</option>
              <option value="festival">{{ t('events.filters.categories.festival') }}</option>
              <option value="conference">{{ t('events.filters.categories.conference') }}</option>
              <option value="exposition">{{ t('events.filters.categories.exposition') }}</option>
            </select>

            <select
              v-model="selectedLocation"
              class="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
            >
              <option value="">{{ t('events.filters.allLocations') }}</option>
              <option value="Nancy">{{ t('events.filters.locations.nancy') }}</option>
              <option value="Paris">{{ t('events.filters.locations.paris') }}</option>
              <option value="Lyon">{{ t('events.filters.locations.lyon') }}</option>
              <option value="Marseille">{{ t('events.filters.locations.marseille') }}</option>
              <option value="En ligne">{{ t('events.filters.locations.online') }}</option>
            </select>

            <button @click="showAddEventModal = true" class="btn-primary">
              <span class="flex items-center space-x-2">
                <span>📅</span>
                <span>{{ t('events.addEvent') }}</span>
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Vue Calendrier/Liste -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Toggle Vue -->
      <div class="flex justify-center mb-8">
        <div class="bg-white rounded-lg p-1 shadow-sm">
          <button
            @click="viewMode = 'list'"
            :class="[
              'px-4 py-2 rounded-md text-sm font-medium transition-colors',
              viewMode === 'list' 
                ? 'bg-ukraine-blue text-white' 
                : 'text-gray-600 hover:text-gray-900'
            ]"
          >
            {{ t('events.view.list') }}
          </button>
          <button
            @click="viewMode = 'calendar'"
            :class="[
              'px-4 py-2 rounded-md text-sm font-medium transition-colors',
              viewMode === 'calendar' 
                ? 'bg-ukraine-blue text-white' 
                : 'text-gray-600 hover:text-gray-900'
            ]"
          >
            {{ t('events.view.calendar') }}
          </button>
        </div>
      </div>

      <!-- Vue Liste -->
      <div v-if="viewMode === 'list'" class="space-y-6">
        <!-- Statistiques -->
        <div class="text-center mb-8">
          <p class="text-gray-600">
            {{ filteredEvents.length }} {{ t('common.event') }}{{ filteredEvents.length > 1 ? 's' : '' }} {{ t('common.found') }}{{ filteredEvents.length > 1 ? 's' : '' }}
          </p>
        </div>

        <!-- Grille des événements -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div
            v-for="event in filteredEvents"
            :key="event.id"
            class="card group cursor-pointer transform hover:scale-105 transition-all duration-300"
            @click="showEventDetails(event)"
          >
            <!-- Image de l'événement -->
            <div class="relative overflow-hidden rounded-t-xl">
              <div class="aspect-video bg-gradient-to-br from-ukraine-blue/20 to-ukraine-yellow/20 flex items-center justify-center">
                <span class="text-4xl">{{ event.icon }}</span>
              </div>
              <div class="absolute top-3 right-3">
                <span class="px-2 py-1 text-xs font-medium rounded-full"
                  :class="{
                    'bg-ukraine-blue/20 text-ukraine-blue': event.category === 'culture',
                    'bg-ukraine-yellow/20 text-ukraine-darkYellow': event.category === 'education',
                    'bg-green-100 text-green-800': event.category === 'solidarite',
                    'bg-purple-100 text-purple-800': event.category === 'festival',
                    'bg-orange-100 text-orange-800': event.category === 'conference',
                    'bg-pink-100 text-pink-800': event.category === 'exposition'
                  }"
                >
                  {{ event.category }}
                </span>
              </div>
              <div class="absolute bottom-3 left-3">
                <span class="px-2 py-1 text-xs font-medium bg-white/90 text-gray-700 rounded-full">
                  {{ event.location }}
                </span>
              </div>
            </div>

            <!-- Informations de l'événement -->
            <div class="p-6">
              <h3 class="text-xl font-semibold text-gray-900 mb-2 group-hover:text-ukraine-blue transition-colors">
                {{ event.title }}
              </h3>
              
              <div class="flex items-center space-x-4 mb-3 text-sm text-gray-600">
                <span class="flex items-center space-x-1">
                  <span>📅</span>
                  <span>{{ formatDate(event.date) }}</span>
                </span>
                <span class="flex items-center space-x-1">
                  <span>🕒</span>
                  <span>{{ event.time }}</span>
                </span>
              </div>

              <p class="text-gray-600 mb-4 line-clamp-2">
                {{ event.description }}
              </p>

              <!-- Actions -->
              <div class="flex items-center justify-between">
                <button 
                  @click.stop="registerForEvent(event)"
                  class="btn-primary text-sm px-4 py-2"
                  :disabled="event.registered"
                >
                  {{ event.registered ? t('events.event.registered') : t('events.event.register') }}
                </button>
                <button 
                  @click.stop="showEventDetails(event)"
                  class="text-ukraine-blue hover:text-ukraine-darkBlue transition-colors"
                >
                  <span class="text-lg">👁️</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Vue Calendrier -->
      <div v-else class="bg-white rounded-xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-gray-900">
            {{ currentMonthName }} {{ currentYear }}
          </h3>
          <div class="flex space-x-2">
            <button @click="previousMonth" class="p-2 hover:bg-gray-100 rounded-lg">
              ←
            </button>
            <button @click="nextMonth" class="p-2 hover:bg-gray-100 rounded-lg">
              →
            </button>
          </div>
        </div>

        <!-- En-têtes des jours -->
        <div class="grid grid-cols-7 gap-1 mb-2">
          <div v-for="day in ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']" :key="day" class="text-center text-sm font-medium text-gray-500 py-2">
            {{ day }}
          </div>
        </div>

        <!-- Grille du calendrier -->
        <div class="grid grid-cols-7 gap-1">
          <div
            v-for="day in calendarDays"
            :key="day.date"
            :class="[
              'min-h-[80px] p-2 border border-gray-200 relative cursor-pointer hover:bg-gray-50 transition-colors',
              day.isCurrentMonth ? 'bg-white' : 'bg-gray-50 text-gray-400',
              day.isToday ? 'bg-ukraine-blue/10 border-ukraine-blue' : ''
            ]"
            @click="selectDate(day)"
          >
            <span class="text-sm font-medium">{{ day.dayNumber }}</span>
            
            <!-- Événements du jour -->
            <div class="mt-1 space-y-1">
              <div
                v-for="event in getEventsForDate(day.date)"
                :key="event.id"
                class="text-xs p-1 rounded bg-ukraine-blue/20 text-ukraine-blue truncate"
                @click.stop="showEventDetails(event)"
              >
                {{ event.title }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Ajouter un événement -->
    <div v-if="showAddEventModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-gray-900">Ajouter un événement</h3>
            <button @click="showAddEventModal = false" class="text-gray-400 hover:text-gray-600">
              <span class="text-2xl">×</span>
            </button>
          </div>
        </div>
        
        <form @submit.prevent="addEvent" class="p-6 space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Titre *</label>
              <input
                v-model="newEvent.title"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Catégorie *</label>
              <select
                v-model="newEvent.category"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              >
                <option value="">Sélectionner une catégorie</option>
                <option value="culture">Culture</option>
                <option value="education">Éducation</option>
                <option value="solidarite">Solidarité</option>
                <option value="festival">Festival</option>
                <option value="conference">Conférence</option>
                <option value="exposition">Exposition</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Date *</label>
              <input
                v-model="newEvent.date"
                type="date"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Heure *</label>
              <input
                v-model="newEvent.time"
                type="time"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Lieu *</label>
              <input
                v-model="newEvent.location"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Organisateur *</label>
              <input
                v-model="newEvent.organizer"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              >
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <textarea
              v-model="newEvent.description"
              rows="4"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              placeholder="Description de l'événement..."
            ></textarea>
          </div>
          
          <div class="flex justify-end space-x-4 pt-4">
            <button
              type="button"
              @click="showAddEventModal = false"
              class="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Annuler
            </button>
            <button
              type="submit"
              class="btn-primary px-6 py-3"
            >
              Ajouter l'événement
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Détails de l'événement -->
    <div v-if="selectedEvent" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-gray-900">Détails de l'événement</h3>
            <button @click="selectedEvent = null" class="text-gray-400 hover:text-gray-600">
              <span class="text-2xl">×</span>
            </button>
          </div>
        </div>
        
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <!-- Image -->
            <div class="md:col-span-1">
              <div class="aspect-video bg-gradient-to-br from-ukraine-blue/20 to-ukraine-yellow/20 rounded-xl flex items-center justify-center">
                <span class="text-6xl">{{ selectedEvent.icon }}</span>
              </div>
            </div>
            
            <!-- Informations -->
            <div class="md:col-span-2 space-y-6">
              <div>
                <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ selectedEvent.title }}</h2>
                <p class="text-lg text-gray-600 mb-4">Organisé par {{ selectedEvent.organizer }}</p>
                
                <div class="flex flex-wrap gap-2 mb-4">
                  <span class="px-3 py-1 text-sm font-medium bg-ukraine-blue/20 text-ukraine-blue rounded-full">
                    {{ selectedEvent.category }}
                  </span>
                  <span class="px-3 py-1 text-sm font-medium bg-ukraine-yellow/20 text-ukraine-darkYellow rounded-full">
                    {{ selectedEvent.location }}
                  </span>
                </div>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="flex items-center space-x-3">
                  <span class="text-2xl">📅</span>
                  <div>
                    <p class="font-medium text-gray-900">{{ formatDate(selectedEvent.date) }}</p>
                    <p class="text-sm text-gray-600">{{ selectedEvent.time }}</p>
                  </div>
                </div>
                
                <div class="flex items-center space-x-3">
                  <span class="text-2xl">📍</span>
                  <div>
                    <p class="font-medium text-gray-900">{{ selectedEvent.location }}</p>
                    <p class="text-sm text-gray-600">Lieu de l'événement</p>
                  </div>
                </div>
              </div>
              
              <div>
                <h4 class="text-lg font-semibold text-gray-900 mb-2">Description</h4>
                <p class="text-gray-600">{{ selectedEvent.description }}</p>
              </div>
              
              <div class="flex items-center justify-between pt-4">
                <button 
                  @click="registerForEvent(selectedEvent)"
                  class="btn-primary px-6 py-3"
                  :disabled="selectedEvent.registered"
                >
                  {{ selectedEvent.registered ? 'Déjà inscrit' : 'S\'inscrire à cet événement' }}
                </button>
                
                <div class="flex items-center space-x-4">
                  <span class="text-sm text-gray-500">
                    {{ selectedEvent.attendees }} participant{{ selectedEvent.attendees > 1 ? 's' : '' }}
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
import NavBar from '@/components/NavBar.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const searchQuery = ref('')
const selectedCategory = ref('')
const selectedLocation = ref('')
const showAddEventModal = ref(false)
const selectedEvent = ref(null)
const viewMode = ref('list')
const currentDate = ref(new Date())

// Nouvel événement
const newEvent = ref({
  title: '',
  category: '',
  date: '',
  time: '',
  location: '',
  organizer: '',
  description: ''
})

// Données de test enrichies
const events = ref([
  {
    id: 1,
    title: 'Soirée Culturelle Ukrainienne',
    category: 'culture',
    date: '2024-02-15',
    time: '19:00',
    location: 'Nancy',
    organizer: 'Association Les Lumières d\'Ukraine',
    description: 'Une soirée exceptionnelle pour découvrir la culture ukrainienne à travers la musique, la danse et la gastronomie traditionnelle.',
    icon: '🎭',
    registered: false,
    attendees: 45
  },
  {
    id: 2,
    title: 'Cours de Langue Ukrainienne',
    category: 'education',
    date: '2024-02-20',
    time: '18:30',
    location: 'Nancy',
    organizer: 'Institut de Langues Ukrainiennes',
    description: 'Cours d\'initiation à la langue ukrainienne pour débutants. Découvrez les bases de cette belle langue slave.',
    icon: '📚',
    registered: true,
    attendees: 12
  },
  {
    id: 3,
    title: 'Collecte de Dons pour l\'Ukraine',
    category: 'solidarite',
    date: '2024-02-25',
    time: '10:00',
    location: 'Nancy',
    organizer: 'Comité de Solidarité',
    description: 'Collecte de dons en faveur des populations ukrainiennes touchées par le conflit. Vêtements, médicaments et denrées alimentaires.',
    icon: '🤝',
    registered: false,
    attendees: 78
  },
  {
    id: 4,
    title: 'Festival du Cinéma Ukrainien',
    category: 'festival',
    date: '2024-03-01',
    time: '20:00',
    location: 'Paris',
    organizer: 'Cinémathèque Ukrainienne',
    description: 'Projection de films ukrainiens contemporains suivie d\'une discussion avec les réalisateurs.',
    icon: '🎬',
    registered: false,
    attendees: 120
  },
  {
    id: 5,
    title: 'Conférence sur l\'Histoire de l\'Ukraine',
    category: 'conference',
    date: '2024-03-05',
    time: '14:00',
    location: 'En ligne',
    organizer: 'Université de Nancy',
    description: 'Conférence en ligne sur l\'histoire de l\'Ukraine, de la Rus\' de Kiev à nos jours.',
    icon: '🎓',
    registered: false,
    attendees: 89
  },
  {
    id: 6,
    title: 'Exposition d\'Art Ukrainien',
    category: 'exposition',
    date: '2024-03-10',
    time: '11:00',
    location: 'Lyon',
    organizer: 'Galerie d\'Art Contemporain',
    description: 'Exposition d\'œuvres d\'artistes ukrainiens contemporains, peintures, sculptures et installations.',
    icon: '🎨',
    registered: false,
    attendees: 34
  }
])

const filteredEvents = computed(() => {
  return events.value.filter(event => {
    const matchesSearch = !searchQuery.value || 
      event.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      event.organizer.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesCategory = !selectedCategory.value || event.category === selectedCategory.value
    const matchesLocation = !selectedLocation.value || event.location === selectedLocation.value
    
    return matchesSearch && matchesCategory && matchesLocation
  })
})

const currentMonthName = computed(() => {
  return currentDate.value.toLocaleDateString('fr-FR', { month: 'long' })
})

const currentYear = computed(() => {
  return currentDate.value.getFullYear()
})

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  
  const startDate = new Date(firstDay)
  startDate.setDate(startDate.getDate() - (firstDay.getDay() || 7) + 1)
  
  const endDate = new Date(lastDay)
  endDate.setDate(endDate.getDate() + (7 - lastDay.getDay()) % 7)
  
  const days = []
  const today = new Date()
  
  for (let date = new Date(startDate); date <= endDate; date.setDate(date.getDate() + 1)) {
    days.push({
      date: new Date(date),
      dayNumber: date.getDate(),
      isCurrentMonth: date.getMonth() === month,
      isToday: date.toDateString() === today.toDateString()
    })
  }
  
  return days
})

function showEventDetails(event) {
  selectedEvent.value = event
}

function registerForEvent(event) {
  if (!event.registered) {
    event.registered = true
    event.attendees++
    window.$notify?.success('Inscription réussie !', `Vous êtes inscrit à "${event.title}".`)
  }
}

function addEvent() {
  const event = {
    id: events.value.length + 1,
    ...newEvent.value,
    icon: getEventIcon(newEvent.value.category),
    registered: false,
    attendees: 0
  }
  
  events.value.push(event)
  showAddEventModal.value = false
  
  window.$notify?.success('Événement créé !', `${event.title} a été ajouté au calendrier.`)
  
  // Reset form
  newEvent.value = {
    title: '',
    category: '',
    date: '',
    time: '',
    location: '',
    organizer: '',
    description: ''
  }
}

function getEventIcon(category) {
  const icons = {
    culture: '🎭',
    education: '📚',
    solidarite: '🤝',
    festival: '🎬',
    conference: '🎓',
    exposition: '🎨'
  }
  return icons[category] || '📅'
}

function getEventsForDate(date) {
  return events.value.filter(event => {
    const eventDate = new Date(event.date)
    return eventDate.toDateString() === date.toDateString()
  })
}

function selectDate(day) {
  if (day.isCurrentMonth) {
    // Ici on pourrait naviguer vers la vue liste avec le filtre de date
    console.log('Date sélectionnée:', day.date)
  }
}

function previousMonth() {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1)
}

function nextMonth() {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1)
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    weekday: 'long',
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