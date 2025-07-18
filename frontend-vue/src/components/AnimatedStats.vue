<template>
  <div class="animated-stats-container">
    <div class="stats-grid">
      <div 
        v-for="stat in stats" 
        :key="stat.id"
        class="stat-card"
        :class="{ 'animate': stat.animate }"
      >
        <div class="stat-icon">
          <span class="icon">{{ stat.icon }}</span>
        </div>
        
        <div class="stat-content">
          <div class="stat-number">
            <span class="counter" :data-target="stat.value">0</span>
            <span v-if="stat.suffix" class="suffix">{{ stat.suffix }}</span>
          </div>
          <h3 class="stat-label">{{ stat.label }}</h3>
          <p class="stat-description">{{ stat.description }}</p>
        </div>
        
        <!-- Barre de progression -->
        <div class="stat-progress">
          <div 
            class="progress-bar"
            :style="{ width: stat.percentage + '%' }"
          ></div>
        </div>
      </div>
    </div>
    
    <!-- Graphique circulaire -->
    <div class="stats-chart">
      <div class="chart-container">
        <canvas ref="chartCanvas" width="200" height="200"></canvas>
        <div class="chart-center">
          <span class="chart-total">{{ totalValue }}</span>
          <span class="chart-label">Total</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  stats: {
    type: Array,
    default: () => []
  }
})

const chartCanvas = ref(null)

const totalValue = ref(0)

// Animation des compteurs
function animateCounter(element, target, duration = 2000) {
  const start = 0
  const increment = target / (duration / 16)
  let current = start
  
  const timer = setInterval(() => {
    current += increment
    if (current >= target) {
      current = target
      clearInterval(timer)
    }
    element.textContent = Math.floor(current)
  }, 16)
}

// Animation des barres de progression
function animateProgress(element, target, duration = 2000) {
  const start = 0
  const increment = target / (duration / 16)
  let current = start
  
  const timer = setInterval(() => {
    current += increment
    if (current >= target) {
      current = target
      clearInterval(timer)
    }
    element.style.width = current + '%'
  }, 16)
}

// Dessiner le graphique circulaire
function drawChart() {
  const canvas = chartCanvas.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  const centerX = canvas.width / 2
  const centerY = canvas.height / 2
  const radius = 80
  
  // Calculer le total
  const total = props.stats.reduce((sum, stat) => sum + stat.value, 0)
  totalValue.value = total
  
  // Couleurs pour chaque section
  const colors = ['#0056b3', '#ffd700', '#ff6b6b', '#4ecdc4', '#45b7d1']
  
  let currentAngle = -Math.PI / 2 // Commencer en haut
  
  props.stats.forEach((stat, index) => {
    const sliceAngle = (stat.value / total) * 2 * Math.PI
    
    // Dessiner la section
    ctx.beginPath()
    ctx.moveTo(centerX, centerY)
    ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle)
    ctx.closePath()
    ctx.fillStyle = colors[index % colors.length]
    ctx.fill()
    
    // Bordure
    ctx.strokeStyle = '#ffffff'
    ctx.lineWidth = 2
    ctx.stroke()
    
    currentAngle += sliceAngle
  })
}

// Observer l'intersection pour déclencher les animations
function observeElements() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const statCard = entry.target
        const counter = statCard.querySelector('.counter')
        const progressBar = statCard.querySelector('.progress-bar')
        const stat = props.stats.find(s => s.id === statCard.dataset.statId)
        
        if (counter && stat) {
          animateCounter(counter, stat.value)
        }
        
        if (progressBar && stat) {
          animateProgress(progressBar, stat.percentage)
        }
        
        statCard.classList.add('animate')
        observer.unobserve(statCard)
      }
    })
  }, { threshold: 0.5 })
  
  document.querySelectorAll('.stat-card').forEach(card => {
    observer.observe(card)
  })
}

onMounted(() => {
  // Dessiner le graphique
  drawChart()
  
  // Observer les éléments pour les animations
  setTimeout(observeElements, 500)
})

// Redessiner le graphique si les données changent
watch(() => props.stats, () => {
  drawChart()
}, { deep: true })
</script>

<style scoped>
.animated-stats-container {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 40px;
  align-items: start;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateY(20px);
}

.stat-card.animate {
  opacity: 1;
  transform: translateY(0);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #0056b3 0%, #1e3c72 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.stat-card:nth-child(2) .stat-icon {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
}

.stat-card:nth-child(3) .stat-icon {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
}

.stat-card:nth-child(4) .stat-icon {
  background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
}

.icon {
  font-size: 24px;
  color: white;
}

.stat-content {
  margin-bottom: 16px;
}

.stat-number {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin-bottom: 8px;
}

.counter {
  font-size: 32px;
  font-weight: 700;
  color: #1e3c72;
  line-height: 1;
}

.suffix {
  font-size: 16px;
  color: #6b7280;
  font-weight: 500;
}

.stat-label {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 4px;
}

.stat-description {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
}

.stat-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: #e2e8f0;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #0056b3 0%, #1e3c72 100%);
  transition: width 2s ease;
  width: 0;
}

.stat-card:nth-child(2) .progress-bar {
  background: linear-gradient(90deg, #ffd700 0%, #ffed4e 100%);
}

.stat-card:nth-child(3) .progress-bar {
  background: linear-gradient(90deg, #ff6b6b 0%, #ee5a52 100%);
}

.stat-card:nth-child(4) .progress-bar {
  background: linear-gradient(90deg, #4ecdc4 0%, #44a08d 100%);
}

.stats-chart {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  text-align: center;
}

.chart-container {
  position: relative;
  display: inline-block;
}

.chart-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.chart-total {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: #1e3c72;
  line-height: 1;
}

.chart-label {
  display: block;
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 4px;
}

@media (max-width: 1024px) {
  .animated-stats-container {
    grid-template-columns: 1fr;
  }
  
  .stats-chart {
    order: -1;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    padding: 20px;
  }
  
  .counter {
    font-size: 28px;
  }
}
</style> 
  <div class="animated-stats-container">
    <div class="stats-grid">
      <div 
        v-for="stat in stats" 
        :key="stat.id"
        class="stat-card"
        :class="{ 'animate': stat.animate }"
      >
        <div class="stat-icon">
          <span class="icon">{{ stat.icon }}</span>
        </div>
        
        <div class="stat-content">
          <div class="stat-number">
            <span class="counter" :data-target="stat.value">0</span>
            <span v-if="stat.suffix" class="suffix">{{ stat.suffix }}</span>
          </div>
          <h3 class="stat-label">{{ stat.label }}</h3>
          <p class="stat-description">{{ stat.description }}</p>
        </div>
        
        <!-- Barre de progression -->
        <div class="stat-progress">
          <div 
            class="progress-bar"
            :style="{ width: stat.percentage + '%' }"
          ></div>
        </div>
      </div>
    </div>
    
    <!-- Graphique circulaire -->
    <div class="stats-chart">
      <div class="chart-container">
        <canvas ref="chartCanvas" width="200" height="200"></canvas>
        <div class="chart-center">
          <span class="chart-total">{{ totalValue }}</span>
          <span class="chart-label">Total</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  stats: {
    type: Array,
    default: () => []
  }
})

const chartCanvas = ref(null)

const totalValue = ref(0)

// Animation des compteurs
function animateCounter(element, target, duration = 2000) {
  const start = 0
  const increment = target / (duration / 16)
  let current = start
  
  const timer = setInterval(() => {
    current += increment
    if (current >= target) {
      current = target
      clearInterval(timer)
    }
    element.textContent = Math.floor(current)
  }, 16)
}

// Animation des barres de progression
function animateProgress(element, target, duration = 2000) {
  const start = 0
  const increment = target / (duration / 16)
  let current = start
  
  const timer = setInterval(() => {
    current += increment
    if (current >= target) {
      current = target
      clearInterval(timer)
    }
    element.style.width = current + '%'
  }, 16)
}

// Dessiner le graphique circulaire
function drawChart() {
  const canvas = chartCanvas.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  const centerX = canvas.width / 2
  const centerY = canvas.height / 2
  const radius = 80
  
  // Calculer le total
  const total = props.stats.reduce((sum, stat) => sum + stat.value, 0)
  totalValue.value = total
  
  // Couleurs pour chaque section
  const colors = ['#0056b3', '#ffd700', '#ff6b6b', '#4ecdc4', '#45b7d1']
  
  let currentAngle = -Math.PI / 2 // Commencer en haut
  
  props.stats.forEach((stat, index) => {
    const sliceAngle = (stat.value / total) * 2 * Math.PI
    
    // Dessiner la section
    ctx.beginPath()
    ctx.moveTo(centerX, centerY)
    ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle)
    ctx.closePath()
    ctx.fillStyle = colors[index % colors.length]
    ctx.fill()
    
    // Bordure
    ctx.strokeStyle = '#ffffff'
    ctx.lineWidth = 2
    ctx.stroke()
    
    currentAngle += sliceAngle
  })
}

// Observer l'intersection pour déclencher les animations
function observeElements() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const statCard = entry.target
        const counter = statCard.querySelector('.counter')
        const progressBar = statCard.querySelector('.progress-bar')
        const stat = props.stats.find(s => s.id === statCard.dataset.statId)
        
        if (counter && stat) {
          animateCounter(counter, stat.value)
        }
        
        if (progressBar && stat) {
          animateProgress(progressBar, stat.percentage)
        }
        
        statCard.classList.add('animate')
        observer.unobserve(statCard)
      }
    })
  }, { threshold: 0.5 })
  
  document.querySelectorAll('.stat-card').forEach(card => {
    observer.observe(card)
  })
}

onMounted(() => {
  // Dessiner le graphique
  drawChart()
  
  // Observer les éléments pour les animations
  setTimeout(observeElements, 500)
})

// Redessiner le graphique si les données changent
watch(() => props.stats, () => {
  drawChart()
}, { deep: true })
</script>

<style scoped>
.animated-stats-container {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 40px;
  align-items: start;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateY(20px);
}

.stat-card.animate {
  opacity: 1;
  transform: translateY(0);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #0056b3 0%, #1e3c72 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.stat-card:nth-child(2) .stat-icon {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
}

.stat-card:nth-child(3) .stat-icon {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
}

.stat-card:nth-child(4) .stat-icon {
  background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
}

.icon {
  font-size: 24px;
  color: white;
}

.stat-content {
  margin-bottom: 16px;
}

.stat-number {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin-bottom: 8px;
}

.counter {
  font-size: 32px;
  font-weight: 700;
  color: #1e3c72;
  line-height: 1;
}

.suffix {
  font-size: 16px;
  color: #6b7280;
  font-weight: 500;
}

.stat-label {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 4px;
}

.stat-description {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
}

.stat-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: #e2e8f0;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #0056b3 0%, #1e3c72 100%);
  transition: width 2s ease;
  width: 0;
}

.stat-card:nth-child(2) .progress-bar {
  background: linear-gradient(90deg, #ffd700 0%, #ffed4e 100%);
}

.stat-card:nth-child(3) .progress-bar {
  background: linear-gradient(90deg, #ff6b6b 0%, #ee5a52 100%);
}

.stat-card:nth-child(4) .progress-bar {
  background: linear-gradient(90deg, #4ecdc4 0%, #44a08d 100%);
}

.stats-chart {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  text-align: center;
}

.chart-container {
  position: relative;
  display: inline-block;
}

.chart-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.chart-total {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: #1e3c72;
  line-height: 1;
}

.chart-label {
  display: block;
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 4px;
}

@media (max-width: 1024px) {
  .animated-stats-container {
    grid-template-columns: 1fr;
  }
  
  .stats-chart {
    order: -1;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    padding: 20px;
  }
  
  .counter {
    font-size: 28px;
  }
}
</style> 