<template>
  <div class="interactive-map-container">
    <div class="map-header">
      <h3 class="map-title">Carte Interactive</h3>
      <p class="map-subtitle">Découvrez nos activités par région</p>
    </div>

    <div class="map-wrapper">
      <!-- Carte de la France stylisée -->
      <div class="france-map">
        <!-- Régions avec points d'activité -->
        <div
          v-for="region in regions"
          :key="region.id"
          class="region-point"
          :class="{ active: selectedRegion?.id === region.id }"
          :style="{ left: region.x + '%', top: region.y + '%' }"
          @click="selectRegion(region)"
          @mouseenter="hoverRegion(region)"
          @mouseleave="hoverRegion(null)"
        >
          <div class="region-marker">
            <span class="marker-icon">{{ region.icon }}</span>
            <span class="marker-count">{{ region.activityCount }}</span>
          </div>

          <!-- Tooltip -->
          <div v-if="hoveredRegion?.id === region.id" class="region-tooltip">
            <h4>{{ region.name }}</h4>
            <p>{{ region.activityCount }} activité{{ region.activityCount > 1 ? 's' : '' }}</p>
            <div class="tooltip-activities">
              <div
                v-for="activity in region.activities.slice(0, 3)"
                :key="activity.id"
                class="tooltip-activity"
              >
                <span class="activity-icon">{{ activity.icon }}</span>
                <span class="activity-name">{{ activity.name }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Lignes de connexion entre régions -->
        <svg class="connection-lines" viewBox="0 0 100 100" preserveAspectRatio="none">
          <line
            v-for="connection in connections"
            :key="connection.id"
            :x1="connection.from.x"
            :y1="connection.from.y"
            :x2="connection.to.x"
            :y2="connection.to.y"
            class="connection-line"
          />
        </svg>
      </div>

      <!-- Panneau d'informations -->
      <div class="map-info-panel">
        <div v-if="selectedRegion" class="region-info">
          <div class="region-header">
            <h4 class="region-name">{{ selectedRegion.name }}</h4>
            <button @click="selectedRegion = null" class="close-btn">×</button>
          </div>

          <div class="region-stats">
            <div class="stat-item">
              <span class="stat-icon">📚</span>
              <div class="stat-content">
                <span class="stat-value">{{ selectedRegion.booksCount }}</span>
                <span class="stat-label">Livres</span>
              </div>
            </div>
            <div class="stat-item">
              <span class="stat-icon">📅</span>
              <div class="stat-content">
                <span class="stat-value">{{ selectedRegion.eventsCount }}</span>
                <span class="stat-label">Événements</span>
              </div>
            </div>
            <div class="stat-item">
              <span class="stat-icon">👥</span>
              <div class="stat-content">
                <span class="stat-value">{{ selectedRegion.membersCount }}</span>
                <span class="stat-label">Membres</span>
              </div>
            </div>
          </div>

          <div class="region-activities">
            <h5>Activités récentes</h5>
            <div class="activity-list">
              <div
                v-for="activity in selectedRegion.activities"
                :key="activity.id"
                class="activity-item"
              >
                <span class="activity-icon">{{ activity.icon }}</span>
                <div class="activity-details">
                  <span class="activity-name">{{ activity.name }}</span>
                  <span class="activity-date">{{ activity.date }}</span>
                </div>
              </div>
            </div>
          </div>

          <button class="btn-primary w-full mt-4">Voir toutes les activités</button>
        </div>

        <div v-else class="map-instructions">
          <div class="instruction-icon">🗺️</div>
          <h4>Explorez la carte</h4>
          <p>Cliquez sur un point pour découvrir les activités de cette région</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const selectedRegion = ref(null)
const hoveredRegion = ref(null)

// Données des régions
const regions = ref([
  {
    id: 'grand-est',
    name: 'Grand Est',
    x: 85,
    y: 45,
    icon: '🏛️',
    activityCount: 12,
    booksCount: 45,
    eventsCount: 8,
    membersCount: 156,
    activities: [
      { id: 1, name: 'Soirée Culturelle Nancy', icon: '🎭', date: '15 fév 2024' },
      { id: 2, name: 'Cours de Langue Strasbourg', icon: '📚', date: '20 fév 2024' },
      { id: 3, name: 'Exposition Metz', icon: '🎨', date: '25 fév 2024' },
      { id: 4, name: 'Collecte de Dons', icon: '🤝', date: '1 mars 2024' },
    ],
  },
  {
    id: 'ile-de-france',
    name: 'Île-de-France',
    x: 45,
    y: 35,
    icon: '🗼',
    activityCount: 18,
    booksCount: 78,
    eventsCount: 15,
    membersCount: 342,
    activities: [
      { id: 5, name: 'Festival Cinéma Paris', icon: '🎬', date: '1 mars 2024' },
      { id: 6, name: 'Conférence Sorbonne', icon: '🎓', date: '5 mars 2024' },
      { id: 7, name: 'Exposition Louvre', icon: '🎨', date: '10 mars 2024' },
    ],
  },
  {
    id: 'auvergne-rhone-alpes',
    name: 'Auvergne-Rhône-Alpes',
    x: 70,
    y: 65,
    icon: '🏔️',
    activityCount: 9,
    booksCount: 32,
    eventsCount: 6,
    membersCount: 98,
    activities: [
      { id: 8, name: 'Exposition Lyon', icon: '🎨', date: '10 mars 2024' },
      { id: 9, name: 'Concert Grenoble', icon: '🎵', date: '15 mars 2024' },
    ],
  },
  {
    id: 'provence-alpes-cote-azur',
    name: "Provence-Alpes-Côte d'Azur",
    x: 75,
    y: 80,
    icon: '🌊',
    activityCount: 7,
    booksCount: 28,
    eventsCount: 4,
    membersCount: 67,
    activities: [
      { id: 10, name: 'Festival Marseille', icon: '🎭', date: '20 mars 2024' },
      { id: 11, name: 'Exposition Nice', icon: '🎨', date: '25 mars 2024' },
    ],
  },
  {
    id: 'occitanie',
    name: 'Occitanie',
    x: 55,
    y: 75,
    icon: '🌻',
    activityCount: 6,
    booksCount: 23,
    eventsCount: 3,
    membersCount: 45,
    activities: [{ id: 12, name: 'Conférence Toulouse', icon: '🎓', date: '30 mars 2024' }],
  },
])

// Connexions entre régions
const connections = ref([
  { id: 1, from: { x: 85, y: 45 }, to: { x: 45, y: 35 } },
  { id: 2, from: { x: 85, y: 45 }, to: { x: 70, y: 65 } },
  { id: 3, from: { x: 45, y: 35 }, to: { x: 70, y: 65 } },
  { id: 4, from: { x: 70, y: 65 }, to: { x: 75, y: 80 } },
  { id: 5, from: { x: 55, y: 75 }, to: { x: 75, y: 80 } },
])

function selectRegion(region) {
  selectedRegion.value = region
}

function hoverRegion(region) {
  hoveredRegion.value = region
}
</script>

<style scoped>
.interactive-map-container {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.map-header {
  text-align: center;
  margin-bottom: 24px;
}

.map-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e3c72;
  margin-bottom: 8px;
}

.map-subtitle {
  color: #6b7280;
  font-size: 16px;
}

.map-wrapper {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 24px;
  align-items: start;
}

.france-map {
  position: relative;
  width: 100%;
  height: 400px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  overflow: hidden;
}

.region-point {
  position: absolute;
  transform: translate(-50%, -50%);
  cursor: pointer;
  z-index: 10;
  transition: all 0.3s ease;
}

.region-point:hover,
.region-point.active {
  transform: translate(-50%, -50%) scale(1.2);
  z-index: 20;
}

.region-marker {
  position: relative;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #0056b3 0%, #1e3c72 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 86, 179, 0.3);
  transition: all 0.3s ease;
}

.region-point:hover .region-marker,
.region-point.active .region-marker {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
}

.marker-icon {
  font-size: 16px;
  color: white;
}

.region-point:hover .marker-icon,
.region-point.active .marker-icon {
  color: #1e3c72;
}

.marker-count {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #ff6b6b;
  color: white;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 16px;
  text-align: center;
}

.region-tooltip {
  position: absolute;
  bottom: 50px;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  z-index: 30;
}

.region-tooltip h4 {
  font-size: 14px;
  font-weight: 600;
  color: #1e3c72;
  margin-bottom: 4px;
}

.region-tooltip p {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 8px;
}

.tooltip-activities {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tooltip-activity {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
}

.activity-icon {
  font-size: 12px;
}

.connection-lines {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.connection-line {
  stroke: #cbd5e1;
  stroke-width: 1;
  opacity: 0.6;
  animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.8;
  }
}

.map-info-panel {
  background: #f8fafc;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e2e8f0;
}

.region-info {
  animation: fadeIn 0.3s ease;
}

.region-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.region-name {
  font-size: 18px;
  font-weight: 600;
  color: #1e3c72;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #6b7280;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #e2e8f0;
  color: #374151;
}

.region-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.stat-icon {
  font-size: 20px;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
  color: #1e3c72;
}

.stat-label {
  font-size: 11px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.region-activities h5 {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 12px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.activity-item:hover {
  border-color: #0056b3;
  box-shadow: 0 2px 4px rgba(0, 86, 179, 0.1);
}

.activity-icon {
  font-size: 16px;
}

.activity-details {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.activity-name {
  font-size: 13px;
  font-weight: 500;
  color: #374151;
}

.activity-date {
  font-size: 11px;
  color: #6b7280;
}

.map-instructions {
  text-align: center;
  padding: 40px 20px;
  color: #6b7280;
}

.instruction-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.map-instructions h4 {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.map-instructions p {
  font-size: 14px;
  line-height: 1.5;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .map-wrapper {
    grid-template-columns: 1fr;
  }

  .map-info-panel {
    order: -1;
  }

  .france-map {
    height: 300px;
  }
}
</style>
