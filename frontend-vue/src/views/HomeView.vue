<script setup>
import NavBar from '@/components/NavBar.vue'
import { ref, onMounted } from 'vue'

const animatedStats = ref({
  books: 0,
  members: 0,
  events: 0,
  languages: 0
})

const targetStats = {
  books: 500,
  members: 200,
  events: 50,
  languages: 5
}

const features = ref([
  {
    icon: '📚',
    title: 'Bibliothèque Virtuelle',
    description: 'Accédez à notre collection exclusive de livres ukrainiens'
  },
  {
    icon: '🎭',
    title: 'Événements Culturels',
    description: 'Participez à nos rencontres et spectacles'
  },
  {
    icon: '🎨',
    title: 'Expositions d\'Art',
    description: 'Découvrez les artistes ukrainiens contemporains'
  },
  {
    icon: '🎵',
    title: 'Musique Traditionnelle',
    description: 'Écoutez et apprenez la musique ukrainienne'
  },
  {
    icon: '🌍',
    title: 'Échanges Culturels',
    description: 'Connectez-vous avec la communauté ukrainienne'
  },
  {
    icon: '💡',
    title: 'Apprentissage',
    description: 'Cours de langue et d\'histoire ukrainienne'
  }
])

const stats = ref([
  { value: 1500, label: 'Membres' },
  { value: 500, label: 'Livres' },
  { value: 50, label: 'Événements' },
  { value: 100, label: 'Artistes' }
])

const getParticleStyle = (index) => {
  const size = Math.random() * 4 + 2;
  const x = Math.random() * 100;
  const y = Math.random() * 100;
  const delay = Math.random() * 20;
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${x}%`,
    top: `${y}%`,
    animationDelay: `${delay}s`
  };
}

const getBookStyle = (index) => {
  const x = Math.random() * 100;
  const y = Math.random() * 100;
  const rotation = Math.random() * 360;
  const delay = Math.random() * 10;
  return {
    left: `${x}%`,
    top: `${y}%`,
    transform: `rotate(${rotation}deg)`,
    animationDelay: `${delay}s`
  };
}

const startAnimations = () => {
  // Animation des particules
  setInterval(() => {
    document.querySelectorAll('.particle').forEach(particle => {
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      particle.style.transform = `translate(${x}px, ${y}px)`;
    });
  }, 3000);
  
  // Animation des livres
  setInterval(() => {
    document.querySelectorAll('.book').forEach(book => {
      const rotation = Math.random() * 360;
      const scale = 0.8 + Math.random() * 0.4;
      book.style.transform = `rotate(${rotation}deg) scale(${scale})`;
    });
  }, 5000);
}

onMounted(() => {
  // Animation des statistiques
  const animateStats = () => {
    const duration = 2000
    const steps = 60
    const stepDuration = duration / steps
    
    let step = 0
    const timer = setInterval(() => {
      step++
      const progress = step / steps
      const easeOut = 1 - Math.pow(1 - progress, 3)
      
      animatedStats.value.books = Math.floor(targetStats.books * easeOut)
      animatedStats.value.members = Math.floor(targetStats.members * easeOut)
      animatedStats.value.events = Math.floor(targetStats.events * easeOut)
      animatedStats.value.languages = Math.floor(targetStats.languages * easeOut)
      
      if (step >= steps) {
        clearInterval(timer)
      }
    }, stepDuration)
  }
  
  // Démarrer l'animation après 1 seconde
  setTimeout(animateStats, 1000)
  
  // Démarrer les autres animations
  startAnimations()
})
</script>

<template>
  <div class="home-container">
    <!-- Particules interactives en arrière-plan -->
    <div class="particles-container">
      <div v-for="i in 30" :key="i" class="particle" :style="getParticleStyle(i)"></div>
    </div>

    <!-- Livres flottants -->
    <div class="floating-books">
      <div v-for="i in 6" :key="i" class="book" :style="getBookStyle(i)">
        <div class="book-cover"></div>
        <div class="book-pages"></div>
      </div>
    </div>

    <!-- Section Hero -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">
            <span class="title-line">Lumières</span>
            <span class="title-line">d'Ukraine</span>
          </h1>
          <p class="hero-subtitle">
            Découvrez la richesse culturelle et la beauté de l'Ukraine à travers nos livres, 
            nos événements et notre communauté passionnée
          </p>
          <div class="hero-buttons">
            <button class="btn-primary">
              <span class="btn-text">Explorer</span>
              <span class="btn-icon">→</span>
            </button>
            <button class="btn-secondary">
              <span class="btn-text">Rejoindre</span>
              <span class="btn-icon">❤</span>
            </button>
          </div>
        </div>
        
        <div class="hero-visual">
          <div class="floating-elements">
            <div class="element element-1">📚</div>
            <div class="element element-2">🎭</div>
            <div class="element element-3">🎨</div>
            <div class="element element-4">🎵</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section Fonctionnalités -->
    <section class="features-section">
      <div class="section-header">
        <h2 class="section-title">Nos Services</h2>
        <p class="section-subtitle">Une expérience culturelle unique</p>
      </div>
      
      <div class="features-grid">
        <div class="feature-card" v-for="(feature, index) in features" :key="index">
          <div class="card-icon">{{ feature.icon }}</div>
          <h3 class="card-title">{{ feature.title }}</h3>
          <p class="card-description">{{ feature.description }}</p>
          <div class="card-action">
            <span class="action-text">En savoir plus</span>
            <span class="action-arrow">→</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Section Statistiques -->
    <section class="stats-section">
      <div class="stats-container">
        <div class="stat-item" v-for="(stat, index) in stats" :key="index">
          <div class="stat-number">{{ stat.value }}+</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
      </div>
    </section>

    <!-- Section Call-to-Action -->
    <section class="cta-section">
      <div class="cta-content">
        <h2 class="cta-title">Prêt à découvrir l'Ukraine ?</h2>
        <p class="cta-subtitle">Rejoignez notre communauté et partagez votre passion</p>
        <button class="cta-button">
          <span class="button-text">Commencer l'aventure</span>
          <span class="button-sparkle">✨</span>
        </button>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-container {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #0056b3 100%);
  color: white;
}

/* Particules */
.particles-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.particle {
  position: absolute;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.3; }
  50% { transform: translateY(-20px) rotate(180deg); opacity: 0.8; }
}

/* Livres flottants */
.floating-books {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 2;
}

.book {
  position: absolute;
  width: 60px;
  height: 80px;
  animation: bookFloat 8s ease-in-out infinite;
}

.book-cover {
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  border-radius: 4px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  position: relative;
}

.book-pages {
  position: absolute;
  top: 2px;
  left: 2px;
  right: 2px;
  bottom: 2px;
  background: white;
  border-radius: 2px;
}

@keyframes bookFloat {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-30px) rotate(5deg); }
}

/* Section Hero */
.hero-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;
  z-index: 10;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  max-width: 1200px;
  margin: 0 auto;
  align-items: center;
}

.hero-text {
  text-align: left;
}

.hero-title {
  font-size: 4rem;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 2rem;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.title-line {
  display: block;
  background: linear-gradient(45deg, #ffffff, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: titleGlow 3s ease-in-out infinite;
}

@keyframes titleGlow {
  0%, 100% { filter: brightness(1); }
  50% { filter: brightness(1.2); }
}

.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
  margin-bottom: 3rem;
  opacity: 0.9;
  max-width: 500px;
}

.hero-buttons {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.btn-primary, .btn-secondary {
  padding: 1rem 2rem;
  border: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  overflow: hidden;
}

.btn-primary {
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  color: #1e3c72;
  box-shadow: 0 8px 32px rgba(255, 215, 0, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(255, 215, 0, 0.6);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-3px);
}

.btn-icon {
  transition: transform 0.3s ease;
}

.btn-primary:hover .btn-icon {
  transform: translateX(5px);
}

.btn-secondary:hover .btn-icon {
  transform: scale(1.2);
}

/* Section visuelle du hero */
.hero-visual {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 500px;
}

.floating-elements {
  position: relative;
  width: 300px;
  height: 300px;
}

.element {
  position: absolute;
  font-size: 3rem;
  animation: elementFloat 6s ease-in-out infinite;
  filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.3));
}

.element-1 { top: 0; left: 50%; transform: translateX(-50%); animation-delay: 0s; }
.element-2 { top: 25%; right: 0; animation-delay: 1.5s; }
.element-3 { bottom: 25%; left: 0; animation-delay: 3s; }
.element-4 { bottom: 0; left: 50%; transform: translateX(-50%); animation-delay: 4.5s; }

@keyframes elementFloat {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(10deg); }
}

/* Section Fonctionnalités */
.features-section {
  padding: 8rem 2rem;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  position: relative;
  z-index: 10;
}

.section-header {
  text-align: center;
  margin-bottom: 5rem;
}

.section-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, #ffffff, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-subtitle {
  font-size: 1.25rem;
  opacity: 0.8;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2.5rem;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.4s ease;
  text-align: center;
}

.feature-card:hover {
  transform: translateY(-10px);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
  display: block;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.card-description {
  line-height: 1.6;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.card-action {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.card-action:hover {
  gap: 1rem;
}

.action-arrow {
  transition: transform 0.3s ease;
}

.card-action:hover .action-arrow {
  transform: translateX(5px);
}

/* Section Statistiques */
.stats-section {
  padding: 6rem 2rem;
  background: linear-gradient(135deg, rgba(30, 60, 114, 0.8), rgba(42, 82, 152, 0.8));
  position: relative;
  z-index: 10;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 3rem;
  max-width: 1000px;
  margin: 0 auto;
  text-align: center;
}

.stat-item {
  color: white;
}

.stat-number {
  font-size: 3.5rem;
  font-weight: 900;
  margin-bottom: 0.5rem;
  background: linear-gradient(45deg, #ffffff, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 1.1rem;
  opacity: 0.8;
  font-weight: 500;
}

/* Section Call-to-Action */
.cta-section {
  padding: 8rem 2rem;
  position: relative;
  z-index: 10;
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 50%, #ffd700 100%);
  text-align: center;
  color: #1e3c72;
}

.cta-title {
  font-size: 3.5rem;
  font-weight: 900;
  margin-bottom: 1.5rem;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.cta-subtitle {
  font-size: 1.25rem;
  margin-bottom: 3rem;
  opacity: 0.8;
}

.cta-button {
  padding: 1.5rem 3rem;
  background: linear-gradient(45deg, #1e3c72, #2a5298);
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 12px 40px rgba(30, 60, 114, 0.4);
}

.cta-button:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 60px rgba(30, 60, 114, 0.6);
}

.button-sparkle {
  animation: sparkle 2s ease-in-out infinite;
}

@keyframes sparkle {
  0%, 100% { transform: scale(1) rotate(0deg); }
  50% { transform: scale(1.2) rotate(180deg); }
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-content {
    grid-template-columns: 1fr;
    gap: 2rem;
    text-align: center;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-buttons {
    justify-content: center;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .cta-title {
    font-size: 2.5rem;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .cta-title {
    font-size: 2rem;
  }
  
  .stats-container {
    grid-template-columns: 1fr;
  }
}
</style>
