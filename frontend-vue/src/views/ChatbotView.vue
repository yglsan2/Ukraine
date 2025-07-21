<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navbar -->
    <NavBar />

    <!-- Header -->
    <div class="pt-20 pb-12 bg-gradient-to-r from-ukraine-lightBlue to-ukraine-blue">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl sm:text-5xl font-display font-bold text-white mb-4">
            🤖 Assistant <span class="text-ukraine-yellow">RagTime</span>
          </h1>
          <p class="text-xl text-white/90 max-w-3xl mx-auto">
            Découvrez la littérature ukrainienne avec notre assistant intelligent
          </p>
        </div>
      </div>
    </div>

    <!-- Interface RagTime -->
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Statut de l'API -->
      <div class="mb-8 text-center">
        <div class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium" 
             :class="apiStatus === 'online' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
          <div class="w-2 h-2 rounded-full mr-2" 
               :class="apiStatus === 'online' ? 'bg-green-500' : 'bg-red-500'"></div>
          {{ apiStatus === 'online' ? 'API RagTime connectée' : 'API RagTime déconnectée' }}
        </div>
      </div>

      <!-- Interface de chat RagTime -->
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <!-- Header du chat -->
        <div class="bg-gradient-to-r from-ukraine-blue to-ukraine-lightBlue p-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                <span class="text-2xl">🤖</span>
              </div>
              <div>
                <h2 class="text-xl font-semibold text-white">RagTime Assistant</h2>
                <p class="text-white/80 text-sm">Spécialiste de la littérature ukrainienne</p>
              </div>
            </div>
            
            <!-- Toggle IA -->
            <div class="flex items-center space-x-3">
              <span class="text-white text-sm">IA enrichie</span>
              <div class="relative">
                <input 
                  type="checkbox" 
                  id="ai-toggle" 
                  v-model="aiEnabled"
                  class="sr-only"
                />
                <label 
                  for="ai-toggle" 
                  class="block w-12 h-6 rounded-full cursor-pointer transition-colors duration-300"
                  :class="aiEnabled ? 'bg-ukraine-yellow' : 'bg-gray-300'"
                >
                  <div 
                    class="block w-4 h-4 bg-white rounded-full shadow transform transition-transform duration-300"
                    :class="aiEnabled ? 'translate-x-7' : 'translate-x-1'"
                  ></div>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Zone de messages -->
        <div class="h-96 overflow-y-auto p-6 space-y-4" ref="chatContainer">
          <!-- Message de bienvenue -->
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 bg-ukraine-blue rounded-full flex items-center justify-center flex-shrink-0">
              <span class="text-white text-sm">🤖</span>
            </div>
            <div class="bg-gray-100 rounded-2xl rounded-tl-md px-4 py-3 max-w-xs lg:max-w-md">
              <p class="text-gray-800">
                👋 Bonjour ! Je suis RagTime, votre assistant spécialisé dans la littérature ukrainienne.
                Posez-moi vos questions sur nos livres !
              </p>
            </div>
          </div>

          <!-- Messages de l'utilisateur -->
          <div
            v-for="message in userMessages"
            :key="message.id"
            class="flex items-start space-x-3 justify-end"
          >
            <div class="bg-ukraine-blue text-white rounded-2xl rounded-tr-md px-4 py-3 max-w-xs lg:max-w-md">
              <p>{{ message.text }}</p>
            </div>
            <div class="w-8 h-8 bg-ukraine-blue rounded-full flex items-center justify-center flex-shrink-0">
              <span class="text-white text-sm">👤</span>
            </div>
          </div>

          <!-- Réponses du bot -->
          <div v-for="message in botMessages" :key="message.id" class="flex items-start space-x-3">
            <div class="w-8 h-8 bg-ukraine-blue rounded-full flex items-center justify-center flex-shrink-0">
              <span class="text-white text-sm">🤖</span>
            </div>
            <div class="bg-gray-100 rounded-2xl rounded-tl-md px-4 py-3 max-w-xs lg:max-w-md">
              <div v-html="message.text" class="text-gray-800"></div>
              <div v-if="message.timing" class="text-xs text-gray-500 mt-2">
                ⏱️ {{ message.timing }}s{{ message.aiUsed ? ' (avec IA)' : '' }}
              </div>
            </div>
          </div>

          <!-- Indicateur de frappe -->
          <div v-if="isTyping" class="flex items-start space-x-3">
            <div class="w-8 h-8 bg-ukraine-blue rounded-full flex items-center justify-center flex-shrink-0">
              <span class="text-white text-sm">🤖</span>
            </div>
            <div class="bg-gray-100 rounded-2xl rounded-tl-md px-4 py-3">
              <div class="flex space-x-1">
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Suggestions rapides -->
        <div class="border-t border-gray-200 p-4">
          <div class="flex flex-wrap gap-2 mb-4">
            <button
              v-for="suggestion in quickSuggestions"
              :key="suggestion"
              @click="sendMessage(suggestion)"
              class="px-3 py-2 bg-gray-100 hover:bg-ukraine-blue hover:text-white rounded-full text-sm transition-colors duration-300"
            >
              {{ suggestion }}
            </button>
          </div>
        </div>

        <!-- Zone de saisie -->
        <div class="border-t border-gray-200 p-4">
          <div class="flex space-x-3">
            <input
              v-model="newMessage"
              @keyup.enter="sendMessage(newMessage)"
              type="text"
              placeholder="Posez votre question sur la littérature ukrainienne..."
              class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
              :disabled="isTyping"
            />
            <button
              @click="sendMessage(newMessage)"
              :disabled="!newMessage.trim() || isTyping"
              class="px-6 py-3 bg-ukraine-blue text-white rounded-lg hover:bg-ukraine-darkBlue transition-colors duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span class="flex items-center space-x-2">
                <span>📤</span>
                <span class="hidden sm:inline">Envoyer</span>
              </span>
            </button>
          </div>
        </div>
      </div>

      <!-- Fonctionnalités RagTime -->
      <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="card p-6 text-center">
          <div class="w-12 h-12 bg-ukraine-blue/10 rounded-full flex items-center justify-center mx-auto mb-4">
            <span class="text-2xl">🔍</span>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Recherche RAG</h3>
          <p class="text-gray-600 text-sm">
            Recherche sémantique ultra-rapide dans notre bibliothèque
          </p>
        </div>

        <div class="card p-6 text-center">
          <div class="w-12 h-12 bg-ukraine-yellow/10 rounded-full flex items-center justify-center mx-auto mb-4">
            <span class="text-2xl">🤖</span>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">IA Enrichie</h3>
          <p class="text-gray-600 text-sm">Réponses contextuelles avec Phi-2 et Mistral 7B</p>
        </div>

        <div class="card p-6 text-center">
          <div class="w-12 h-12 bg-ukraine-lightBlue/10 rounded-full flex items-center justify-center mx-auto mb-4">
            <span class="text-2xl">📚</span>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Résumés Intelligents</h3>
          <p class="text-gray-600 text-sm">
            Résumés automatiques et détection de thèmes
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import NavBar from '@/components/NavBar.vue'

const { t } = useI18n()

const chatContainer = ref()
const newMessage = ref('')
const isTyping = ref(false)
const aiEnabled = ref(true)
const apiStatus = ref('offline')

const userMessages = ref([])
const botMessages = ref([])

const quickSuggestions = [
  'Livres sur la guerre en Ukraine',
  'Romans d\'amour ukrainiens',
  'Auteurs ukrainiens célèbres',
  'Philosophie ukrainienne',
  'Poésie ukrainienne',
  'Livres en français'
]

// Vérifier le statut de l'API RagTime
const checkApiStatus = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/health')
    apiStatus.value = response.ok ? 'online' : 'offline'
  } catch (error) {
    apiStatus.value = 'offline'
    console.error('Erreur connexion API RagTime:', error)
  }
}

// Appeler l'API RagTime
const callRagTimeAPI = async (query) => {
  try {
    const response = await fetch('http://localhost:5000/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        useAI: aiEnabled.value,
        maxResults: 5
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Erreur API RagTime:', error)
    throw error
  }
}

// Formater les livres trouvés
const formatBooksMessage = (books) => {
  let message = '<strong>📚 Livres trouvés :</strong><br><br>'
  
  books.forEach((book, index) => {
    message += `<strong>${index + 1}. ${book.title}</strong><br>`
    if (book.author) message += `   Auteur: ${book.author}<br>`
    if (book.genre) message += `   Genre: ${book.genre}<br>`
    if (book.language) message += `   Langue: ${book.language}<br>`
    if (book.score) message += `   Pertinence: ${(book.score * 100).toFixed(1)}%<br>`
    message += '<br>'
  })

  return message
}

const sendMessage = async (message) => {
  if (!message.trim() || isTyping.value) return

  // Ajouter le message de l'utilisateur
  userMessages.value.push({
    id: Date.now(),
    text: message,
  })

  // Vider le champ de saisie
  newMessage.value = ''

  // Afficher l'indicateur de frappe
  isTyping.value = true

  try {
    // Appeler l'API RagTime
    const response = await callRagTimeAPI(message)
    
    // Masquer l'indicateur de frappe
    isTyping.value = false

    if (response.success) {
      // Ajouter la réponse principale
      if (response.response) {
        botMessages.value.push({
          id: Date.now(),
          text: response.response,
          timing: response.timing?.total_time?.toFixed(2),
          aiUsed: response.ai_used
        })
      }

      // Ajouter les livres trouvés
      if (response.books && response.books.length > 0) {
        const booksMessage = formatBooksMessage(response.books)
        botMessages.value.push({
          id: Date.now() + 1,
          text: booksMessage,
          timing: response.timing?.total_time?.toFixed(2),
          aiUsed: response.ai_used
        })
      }
    } else {
      botMessages.value.push({
        id: Date.now(),
        text: 'Désolé, je n\'ai pas pu traiter votre demande. Veuillez réessayer.',
        timing: '0.00',
        aiUsed: false
      })
    }
  } catch (error) {
    isTyping.value = false
    botMessages.value.push({
      id: Date.now(),
      text: 'Désolé, une erreur s\'est produite. Vérifiez que l\'API RagTime est démarrée.',
      timing: '0.00',
      aiUsed: false
    })
  }

  // Faire défiler vers le bas
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

onMounted(() => {
  // Vérifier le statut de l'API au chargement
  checkApiStatus()
  
  // Vérifier périodiquement le statut
  setInterval(checkApiStatus, 30000)
  
  // Faire défiler vers le bas au chargement
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
})
</script>

<style scoped>
.font-display {
  font-family: 'Poppins', system-ui, sans-serif;
}

.card {
  @apply bg-white rounded-xl shadow-lg border border-gray-100;
}
</style>
