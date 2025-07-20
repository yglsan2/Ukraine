<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navbar -->
    <NavBar />

    <!-- Header -->
    <div class="pt-20 pb-12 bg-gradient-to-r from-ukraine-lightBlue to-ukraine-blue">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl sm:text-5xl font-display font-bold text-white mb-4">
            Assistant <span class="text-ukraine-yellow">Intelligent</span>
          </h1>
          <p class="text-xl text-white/90 max-w-3xl mx-auto">
            Posez vos questions sur la littérature ukrainienne et obtenez des réponses instantanées
          </p>
        </div>
      </div>
    </div>

    <!-- Interface de chat -->
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <!-- Header du chat -->
        <div class="bg-gradient-to-r from-ukraine-blue to-ukraine-lightBlue p-6">
          <div class="flex items-center space-x-4">
            <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
              <span class="text-2xl">🤖</span>
            </div>
            <div>
              <h2 class="text-xl font-semibold text-white">Assistant Ukraine</h2>
              <p class="text-white/80 text-sm">En ligne • Prêt à vous aider</p>
            </div>
          </div>
        </div>

        <!-- Zone de messages -->
        <div class="h-96 overflow-y-auto p-6 space-y-4" ref="chatContainer">
          <!-- Message de bienvenue -->
          <div class="flex items-start space-x-3">
            <div
              class="w-8 h-8 bg-ukraine-blue rounded-full flex items-center justify-center flex-shrink-0"
            >
              <span class="text-white text-sm">🤖</span>
            </div>
            <div class="bg-gray-100 rounded-2xl rounded-tl-md px-4 py-3 max-w-xs lg:max-w-md">
              <p class="text-gray-800">
                Bonjour ! Je suis votre assistant spécialisé dans la littérature ukrainienne.
                Comment puis-je vous aider aujourd'hui ?
              </p>
            </div>
          </div>

          <!-- Messages de l'utilisateur -->
          <div
            v-for="message in userMessages"
            :key="message.id"
            class="flex items-start space-x-3 justify-end"
          >
            <div
              class="bg-ukraine-blue text-white rounded-2xl rounded-tr-md px-4 py-3 max-w-xs lg:max-w-md"
            >
              <p>{{ message.text }}</p>
            </div>
            <div
              class="w-8 h-8 bg-ukraine-blue rounded-full flex items-center justify-center flex-shrink-0"
            >
              <span class="text-white text-sm">👤</span>
            </div>
          </div>

          <!-- Réponses du bot -->
          <div v-for="message in botMessages" :key="message.id" class="flex items-start space-x-3">
            <div
              class="w-8 h-8 bg-ukraine-blue rounded-full flex items-center justify-center flex-shrink-0"
            >
              <span class="text-white text-sm">🤖</span>
            </div>
            <div class="bg-gray-100 rounded-2xl rounded-tl-md px-4 py-3 max-w-xs lg:max-w-md">
              <p class="text-gray-800">{{ message.text }}</p>
            </div>
          </div>

          <!-- Indicateur de frappe -->
          <div v-if="isTyping" class="flex items-start space-x-3">
            <div
              class="w-8 h-8 bg-ukraine-blue rounded-full flex items-center justify-center flex-shrink-0"
            >
              <span class="text-white text-sm">🤖</span>
            </div>
            <div class="bg-gray-100 rounded-2xl rounded-tl-md px-4 py-3">
              <div class="flex space-x-1">
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div
                  class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                  style="animation-delay: 0.1s"
                ></div>
                <div
                  class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                  style="animation-delay: 0.2s"
                ></div>
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
              placeholder="Tapez votre message..."
              class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-ukraine-blue focus:border-transparent"
            />
            <button
              @click="sendMessage(newMessage)"
              :disabled="!newMessage.trim()"
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

      <!-- Fonctionnalités -->
      <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="card p-6 text-center">
          <div
            class="w-12 h-12 bg-ukraine-blue/10 rounded-full flex items-center justify-center mx-auto mb-4"
          >
            <span class="text-2xl">📚</span>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Recherche de Livres</h3>
          <p class="text-gray-600 text-sm">
            Trouvez des livres ukrainiens par genre, auteur ou thème
          </p>
        </div>

        <div class="card p-6 text-center">
          <div
            class="w-12 h-12 bg-ukraine-yellow/10 rounded-full flex items-center justify-center mx-auto mb-4"
          >
            <span class="text-2xl">🌍</span>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Culture Ukrainienne</h3>
          <p class="text-gray-600 text-sm">Découvrez l'histoire et la culture ukrainienne</p>
        </div>

        <div class="card p-6 text-center">
          <div
            class="w-12 h-12 bg-ukraine-lightBlue/10 rounded-full flex items-center justify-center mx-auto mb-4"
          >
            <span class="text-2xl">🎯</span>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Recommandations</h3>
          <p class="text-gray-600 text-sm">
            Obtenez des suggestions personnalisées selon vos goûts
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import NavBar from '@/components/NavBar.vue'

const { t } = useI18n()

const chatContainer = ref<HTMLElement>()
const newMessage = ref('')
const isTyping = ref(false)

const userMessages = ref([{ id: 1, text: 'Pouvez-vous me recommander des livres ukrainiens ?' }])

const botMessages = ref([
  {
    id: 1,
    text: "Bien sûr ! Je peux vous recommander plusieurs livres ukrainiens selon vos préférences. Que recherchez-vous ? De la poésie, des romans, de l'histoire ?",
  },
])

const quickSuggestions = [
  'Livres de poésie',
  'Romans ukrainiens',
  "Histoire de l'Ukraine",
  'Auteurs célèbres',
]

const sendMessage = async (message: string) => {
  if (!message.trim()) return

  // Ajouter le message de l'utilisateur
  userMessages.value.push({
    id: Date.now(),
    text: message,
  })

  // Vider le champ de saisie
  newMessage.value = ''

  // Simuler la frappe du bot
  isTyping.value = true
  await new Promise((resolve) => setTimeout(resolve, 1000))
  isTyping.value = false

  // Ajouter la réponse du bot
  const responses = [
    'Excellente question ! Laissez-moi vous aider avec cela.',
    'Je peux vous recommander plusieurs ouvrages sur ce sujet.',
    "C'est un thème très intéressant de la littérature ukrainienne.",
    'Voici ce que je peux vous dire à ce sujet...',
  ]

  botMessages.value.push({
    id: Date.now(),
    text: responses[Math.floor(Math.random() * responses.length)],
  })

  // Faire défiler vers le bas
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

onMounted(() => {
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
</style>
