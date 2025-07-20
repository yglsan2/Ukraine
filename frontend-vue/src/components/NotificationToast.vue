<template>
  <div class="fixed top-4 right-4 z-50 space-y-2">
    <TransitionGroup name="notification" tag="div">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        :class="[
          'flex items-center p-4 rounded-lg shadow-lg max-w-sm transform transition-all duration-300',
          {
            'bg-green-500 text-white': notification.type === 'success',
            'bg-red-500 text-white': notification.type === 'error',
            'bg-yellow-500 text-white': notification.type === 'warning',
            'bg-blue-500 text-white': notification.type === 'info',
          },
        ]"
      >
        <!-- Icône -->
        <div class="flex-shrink-0 mr-3">
          <span class="text-xl">
            {{ getIcon(notification.type) }}
          </span>
        </div>

        <!-- Contenu -->
        <div class="flex-1">
          <h4 class="font-medium text-sm">
            {{ notification.title }}
          </h4>
          <p v-if="notification.message" class="text-sm opacity-90 mt-1">
            {{ notification.message }}
          </p>
        </div>

        <!-- Bouton fermer -->
        <button
          @click="removeNotification(notification.id)"
          class="flex-shrink-0 ml-3 text-white/80 hover:text-white transition-colors"
        >
          <span class="text-lg">×</span>
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const notifications = ref([])
let nextId = 1

// Fonction pour ajouter une notification
function addNotification({ type = 'info', title, message = '', duration = 5000 }) {
  const id = nextId++
  const notification = { id, type, title, message }

  notifications.value.push(notification)

  // Auto-remove après la durée spécifiée
  if (duration > 0) {
    setTimeout(() => {
      removeNotification(id)
    }, duration)
  }

  return id
}

// Fonction pour supprimer une notification
function removeNotification(id) {
  const index = notifications.value.findIndex((n) => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
}

// Fonction pour obtenir l'icône selon le type
function getIcon(type) {
  const icons = {
    success: '✅',
    error: '❌',
    warning: '⚠️',
    info: 'ℹ️',
  }
  return icons[type] || icons.info
}

// Fonctions utilitaires pour différents types
function success(title, message = '', duration = 5000) {
  return addNotification({ type: 'success', title, message, duration })
}

function error(title, message = '', duration = 7000) {
  return addNotification({ type: 'error', title, message, duration })
}

function warning(title, message = '', duration = 6000) {
  return addNotification({ type: 'warning', title, message, duration })
}

function info(title, message = '', duration = 5000) {
  return addNotification({ type: 'info', title, message, duration })
}

// Exposer les fonctions utilitaires
defineExpose({
  addNotification,
  removeNotification,
  success,
  error,
  warning,
  info,
})
</script>

<style scoped>
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform 0.3s ease;
}
</style>
