<template>
  <div class="membership-page">
    <div class="container mx-auto px-4 py-8">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-blue-900 mb-4">
          🌻 Adhésion - Les Lumières d'Ukraine
        </h1>
        <p class="text-lg text-gray-600">
          Rejoignez notre association et recevez votre carte d'adhésion personnalisée
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Formulaire d'adhésion -->
        <div class="bg-white rounded-lg shadow-lg p-6">
          <h2 class="text-2xl font-bold text-blue-900 mb-6">📝 Formulaire d'adhésion</h2>
          
          <form @submit.prevent="submitMembership" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Prénom *</label>
                <input 
                  v-model="memberData.firstName" 
                  type="text" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nom *</label>
                <input 
                  v-model="memberData.name" 
                  type="text" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Email *</label>
              <input 
                v-model="memberData.email" 
                type="email" 
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Date de naissance</label>
              <input 
                v-model="memberData.birthDate" 
                type="date" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Adresse</label>
              <input 
                v-model="memberData.address" 
                type="text" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Code Postal</label>
                <input 
                  v-model="memberData.postalCode" 
                  type="text" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Ville</label>
                <input 
                  v-model="memberData.city" 
                  type="text" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Téléphone</label>
              <input 
                v-model="memberData.phone" 
                type="tel" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div class="flex items-center justify-between pt-4">
              <button 
                type="button" 
                @click="generateMemberNumber"
                class="px-4 py-2 bg-yellow-500 text-white rounded-md hover:bg-yellow-600 transition-colors"
              >
                🔢 Générer numéro
              </button>
              <button 
                type="submit" 
                class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
              >
                ✅ Créer l'adhésion
              </button>
            </div>
          </form>
        </div>

        <!-- Aperçu de la carte -->
        <div class="bg-white rounded-lg shadow-lg p-6">
          <h2 class="text-2xl font-bold text-blue-900 mb-6">🪪 Aperçu de votre carte</h2>
          
          <div class="mb-4">
            <MembershipCard :memberData="memberData" @card-generated="onCardGenerated" @card-sent="onCardSent" />
          </div>
          
          <div class="text-center text-sm text-gray-500 mt-4">
            <p>💡 Remplissez le formulaire pour voir votre carte personnalisée</p>
          </div>
        </div>
      </div>

      <!-- Messages de statut -->
      <div v-if="statusMessage" class="mt-8 p-4 rounded-md" :class="statusClass">
        <div class="flex items-center">
          <span class="text-lg mr-2">{{ statusIcon }}</span>
          <p>{{ statusMessage }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MembershipCard from '@/components/MembershipCard.vue'

export default {
  name: 'MembershipView',
  components: {
    MembershipCard
  },
  data() {
    return {
      memberData: {
        name: '',
        firstName: '',
        memberNumber: '',
        joinDate: new Date().toLocaleDateString('fr-FR'),
        birthDate: '',
        address: '',
        postalCode: '',
        city: '',
        phone: '',
        email: ''
      },
      statusMessage: '',
      statusType: 'info'
    }
  },
  computed: {
    statusClass() {
      const classes = {
        success: 'bg-green-100 text-green-800 border border-green-200',
        error: 'bg-red-100 text-red-800 border border-red-200',
        info: 'bg-blue-100 text-blue-800 border border-blue-200'
      }
      return classes[this.statusType] || classes.info
    },
    statusIcon() {
      const icons = {
        success: '✅',
        error: '❌',
        info: 'ℹ️'
      }
      return icons[this.statusType] || icons.info
    }
  },
  methods: {
    async generateMemberNumber() {
      try {
        const response = await fetch('/api/membership/generate-number')
        if (response.ok) {
          const data = await response.json()
          this.memberData.memberNumber = data.memberNumber
          this.showStatus('Numéro d\'adhésion généré avec succès !', 'success')
        } else {
          throw new Error('Erreur lors de la génération du numéro')
        }
      } catch (error) {
        console.error('Erreur:', error)
        this.showStatus('Erreur lors de la génération du numéro d\'adhésion', 'error')
      }
    },

    async submitMembership() {
      try {
        // Valider les données
        if (!this.memberData.firstName || !this.memberData.name || !this.memberData.email) {
          this.showStatus('Veuillez remplir tous les champs obligatoires', 'error')
          return
        }

        // Générer un numéro si pas encore fait
        if (!this.memberData.memberNumber) {
          await this.generateMemberNumber()
        }

        this.showStatus('Adhésion créée avec succès ! Votre carte est prête.', 'success')
        
        // Ici vous pourriez appeler l'API backend pour sauvegarder l'adhésion
        console.log('Données d\'adhésion:', this.memberData)
        
      } catch (error) {
        console.error('Erreur:', error)
        this.showStatus('Erreur lors de la création de l\'adhésion', 'error')
      }
    },

    onCardGenerated(data) {
      this.showStatus(`Carte générée pour le membre ${data.memberNumber}`, 'success')
    },

    onCardSent(data) {
      this.showStatus(`Carte envoyée par email à ${data.to}`, 'success')
    },

    showStatus(message, type = 'info') {
      this.statusMessage = message
      this.statusType = type
      
      // Masquer le message après 5 secondes
      setTimeout(() => {
        this.statusMessage = ''
      }, 5000)
    }
  }
}
</script>

<style scoped>
.membership-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
}

/* Animation d'apparition */
.membership-page > * {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .membership-page .container {
    padding: 1rem;
  }
  
  .membership-page h1 {
    font-size: 2rem;
  }
}
</style> 