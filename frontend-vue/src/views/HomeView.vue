<script setup lang="js">
import { ref, onMounted, computed } from 'vue'
import { useAppStore } from '@/stores/app.mjs'

const appStore = useAppStore()

// État réactif
const totalBooks = ref(0)
const totalUsers = ref(0)
const totalExchanges = ref(0)

// Computed
const recentBooks = computed(() => {
  return appStore.recentBooks
})

// Méthodes
const addToFavorites = (book) => {
  appStore.addToFavorites(book)
  // Afficher une notification
  showNotification('Livre ajouté aux favoris !')
}

const showNotification = (message) => {
  // Ici on pourrait utiliser un système de notifications global
  console.log(message)
}

// Initialisation
onMounted(async () => {
  // Charger les livres si pas encore fait
  if (appStore.books.length === 0) {
    await appStore.loadBooks()
  }
  
  // Mettre à jour les statistiques avec les vraies données
  totalBooks.value = appStore.totalBooks
  totalUsers.value = appStore.totalUsers
  totalExchanges.value = appStore.totalExchanges
})
</script>

<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="row align-items-center min-vh-100">
          <div class="col-lg-6">
            <div class="hero-content">
              <h1 class="hero-title">
                <span class="text-primary">Lumières</span> d'Ukraine
              </h1>
              <p class="hero-subtitle">
                Partagez et découvrez la culture ukrainienne à travers le partage de livres
              </p>
              <div class="hero-stats">
                <div class="stat-item">
                  <div class="stat-number">{{ totalBooks }}</div>
                  <div class="stat-label">Livres disponibles</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ totalUsers }}</div>
                  <div class="stat-label">Membres actifs</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ totalExchanges }}</div>
                  <div class="stat-label">Échanges réalisés</div>
                </div>
              </div>
              <div class="hero-buttons">
                <router-link to="/explorer" class="btn btn-primary btn-lg me-3">
                  <i class="fas fa-search me-2"></i>Explorer les livres
                </router-link>
                <router-link to="/proposer" class="btn btn-outline-primary btn-lg">
                  <i class="fas fa-plus me-2"></i>Proposer un livre
                </router-link>
              </div>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="hero-image">
              <div class="floating-books">
                <div class="book book-1">
                  <i class="fas fa-book"></i>
                </div>
                <div class="book book-2">
                  <i class="fas fa-book-open"></i>
                </div>
                <div class="book book-3">
                  <i class="fas fa-bookmark"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section py-5">
      <div class="container">
        <div class="row text-center mb-5">
          <div class="col-12">
            <h2 class="section-title">Pourquoi nous rejoindre ?</h2>
            <p class="section-subtitle">Découvrez les avantages de notre communauté</p>
          </div>
        </div>
        <div class="row">
          <div class="col-lg-4 col-md-6 mb-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="fas fa-share-alt"></i>
              </div>
              <h3>Partagez vos livres</h3>
              <p>Donnez une seconde vie à vos livres en les partageant avec la communauté</p>
            </div>
          </div>
          <div class="col-lg-4 col-md-6 mb-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="fas fa-globe"></i>
              </div>
              <h3>Découvrez la culture</h3>
              <p>Explorez la riche culture ukrainienne à travers la littérature</p>
            </div>
          </div>
          <div class="col-lg-4 col-md-6 mb-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="fas fa-users"></i>
              </div>
              <h3>Rejoignez la communauté</h3>
              <p>Participez à des événements et rencontrez d'autres passionnés</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Recent Books Section -->
    <section class="recent-books-section py-5 bg-light">
      <div class="container">
        <div class="row mb-4">
          <div class="col-12">
            <h2 class="section-title">Livres récents</h2>
            <p class="section-subtitle">Découvrez les derniers livres ajoutés</p>
          </div>
        </div>
        <div class="row">
          <div v-for="book in recentBooks" :key="book.id" class="col-lg-4 col-md-6 mb-4">
            <div class="book-card">
              <div class="book-image">
                <img :src="book.photo" :alt="book.title" class="img-fluid">
                <div class="book-overlay">
                  <button class="btn btn-primary btn-sm" @click="addToFavorites(book)">
                    <i class="fas fa-heart"></i>
                  </button>
                </div>
              </div>
              <div class="book-content">
                <h5 class="book-title">{{ book.title }}</h5>
                <p class="book-author">{{ book.author }}</p>
                <div class="book-meta">
                  <span class="badge bg-primary">{{ book.genre }}</span>
                  <span class="badge bg-secondary">{{ book.language }}</span>
                </div>
                <p class="book-description">{{ book.description }}</p>
                <div class="book-footer">
                  <small class="text-muted">
                    <i class="fas fa-map-marker-alt me-1"></i>{{ book.city }}
                  </small>
                  <button class="btn btn-outline-primary btn-sm">
                    <i class="fas fa-eye me-1"></i>Voir détails
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="text-center mt-4">
          <router-link to="/explorer" class="btn btn-primary btn-lg">
            Voir tous les livres
          </router-link>
        </div>
      </div>
    </section>

    <!-- Events Section -->
    <section class="events-section py-5">
      <div class="container">
        <div class="row mb-4">
          <div class="col-12">
            <h2 class="section-title">Événements à venir</h2>
            <p class="section-subtitle">Participez à nos événements culturels</p>
          </div>
        </div>
        <div class="row">
          <div class="col-lg-6 mb-4">
            <div class="event-card">
              <div class="event-date">
                <div class="date-day">15</div>
                <div class="date-month">Juil</div>
              </div>
              <div class="event-content">
                <h4>Club de Lecture</h4>
                <p>Discussion autour des poèmes de Taras Chevtchenko</p>
                <div class="event-meta">
                  <i class="fas fa-clock me-2"></i>19h00
                  <i class="fas fa-map-marker-alt ms-3 me-2"></i>Nancy
                </div>
                <button class="btn btn-primary btn-sm mt-2">Participer</button>
              </div>
            </div>
          </div>
          <div class="col-lg-6 mb-4">
            <div class="event-card">
              <div class="event-date">
                <div class="date-day">22</div>
                <div class="date-month">Juil</div>
              </div>
              <div class="event-content">
                <h4>Atelier d'Écriture</h4>
                <p>Découvrez l'art de l'écriture ukrainienne</p>
                <div class="event-meta">
                  <i class="fas fa-clock me-2"></i>14h00
                  <i class="fas fa-map-marker-alt ms-3 me-2"></i>Paris
                </div>
                <button class="btn btn-primary btn-sm mt-2">S'inscrire</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section py-5 bg-primary text-white">
      <div class="container text-center">
        <h2>Prêt à rejoindre notre communauté ?</h2>
        <p class="lead mb-4">
          Inscrivez-vous gratuitement et commencez à partager vos livres dès aujourd'hui
        </p>
        <div class="cta-buttons">
          <router-link to="/register" class="btn btn-light btn-lg me-3">
            <i class="fas fa-user-plus me-2"></i>S'inscrire
          </router-link>
          <router-link to="/about" class="btn btn-outline-light btn-lg">
            <i class="fas fa-info-circle me-2"></i>En savoir plus
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #0057b8 0%, #1e3a8a 50%, #ffdd00 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.3;
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  color: white;
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.hero-title {
  font-size: 4rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.3rem;
  margin-bottom: 2rem;
  opacity: 0.9;
  line-height: 1.6;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 3rem;
  margin: 3rem 0;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  border-radius: 15px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  min-width: 150px;
  transition: transform 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-5px);
}

.stat-number {
  font-size: 3rem;
  font-weight: bold;
  color: #ffdd00;
  display: block;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1rem;
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.hero-buttons {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.hero-buttons .btn {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 50px;
  transition: all 0.3s ease;
  min-width: 200px;
}

.hero-buttons .btn-primary {
  background: #ffdd00;
  border-color: #ffdd00;
  color: #0057b8;
  box-shadow: 0 4px 15px rgba(255, 221, 0, 0.3);
}

.hero-buttons .btn-primary:hover {
  background: #e6c700;
  border-color: #e6c700;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 221, 0, 0.4);
}

.hero-buttons .btn-outline-primary {
  border-color: white;
  color: white;
  background: transparent;
}

.hero-buttons .btn-outline-primary:hover {
  background: white;
  color: #0057b8;
  transform: translateY(-2px);
}

/* Floating books animation */
.floating-books {
  position: relative;
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.book {
  position: absolute;
  width: 80px;
  height: 100px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #0057b8;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  animation: float 6s ease-in-out infinite;
}

.book-1 {
  top: 20%;
  left: 20%;
  animation-delay: 0s;
}

.book-2 {
  top: 40%;
  right: 30%;
  animation-delay: 2s;
}

.book-3 {
  bottom: 30%;
  left: 40%;
  animation-delay: 4s;
}

/* Features Section */
.features-section {
  background: #f8f9fa;
  padding: 5rem 0;
}

.section-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #0057b8;
  margin-bottom: 1rem;
  text-align: center;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #666;
  text-align: center;
  margin-bottom: 3rem;
}

.feature-card {
  text-align: center;
  padding: 2.5rem 1.5rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  width: 100px;
  height: 100px;
  background: linear-gradient(45deg, #0057b8, #ffdd00);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  font-size: 2.5rem;
  color: white;
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.1);
}

.feature-card h3 {
  font-size: 1.5rem;
  font-weight: bold;
  color: #0057b8;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
  flex-grow: 1;
}

/* Recent Books Section */
.recent-books-section {
  background: white;
  padding: 5rem 0;
}

.book-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.book-image {
  position: relative;
  height: 250px;
  overflow: hidden;
  background: linear-gradient(45deg, #0057b8, #ffdd00);
  display: flex;
  align-items: center;
  justify-content: center;
}

.book-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.book-overlay {
  position: absolute;
  top: 15px;
  right: 15px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.book-card:hover .book-overlay {
  opacity: 1;
}

.book-content {
  padding: 1.5rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.book-title {
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #0057b8;
  font-size: 1.2rem;
}

.book-author {
  color: #666;
  margin-bottom: 1rem;
  font-style: italic;
}

.book-meta {
  margin-bottom: 1rem;
}

.book-meta .badge {
  margin-right: 0.5rem;
  font-size: 0.8rem;
}

.book-description {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.4;
  flex-grow: 1;
}

.book-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

/* Events Section */
.events-section {
  background: #f8f9fa;
  padding: 5rem 0;
}

.event-card {
  display: flex;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  height: 100%;
}

.event-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.event-date {
  background: linear-gradient(45deg, #0057b8, #ffdd00);
  color: white;
  padding: 2rem;
  text-align: center;
  min-width: 120px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.date-day {
  font-size: 2.5rem;
  font-weight: bold;
}

.date-month {
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.event-content {
  padding: 2rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.event-content h4 {
  margin-bottom: 0.5rem;
  color: #0057b8;
  font-size: 1.3rem;
}

.event-meta {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

/* Animations */
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

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* Responsive improvements */
@media (max-width: 1199.98px) {
  .hero-title {
    font-size: 3.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
  }
  
  .stat-number {
    font-size: 2.5rem;
  }
  
  .hero-stats {
    gap: 2rem;
  }
}

@media (max-width: 991.98px) {
  .hero-title {
    font-size: 3rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .hero-stats {
    gap: 1.5rem;
  }
  
  .stat-number {
    font-size: 2rem;
  }
  
  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .hero-buttons .btn {
    width: 100%;
    max-width: 300px;
  }
  
  .floating-books {
    display: none;
  }
}

@media (max-width: 767.98px) {
  .hero-section {
    min-height: 80vh;
    padding: 2rem 0;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .hero-stats {
    flex-direction: column;
    gap: 1rem;
    margin: 2rem 0;
  }
  
  .stat-item {
    min-width: auto;
    width: 100%;
    max-width: 250px;
    margin: 0 auto;
  }
  
  .stat-number {
    font-size: 2rem;
  }
  
  .hero-buttons .btn {
    width: 100%;
    max-width: 250px;
  }
  
  .feature-card {
    padding: 2rem 1rem;
    margin-bottom: 1rem;
  }
  
  .feature-icon {
    width: 80px;
    height: 80px;
    font-size: 2rem;
  }
  
  .book-card {
    margin-bottom: 1rem;
  }
  
  .book-content {
    padding: 1rem;
  }
  
  .event-card {
    flex-direction: column;
    margin-bottom: 1rem;
  }
  
  .event-date {
    min-width: auto;
    padding: 1.5rem;
    flex-direction: row;
    justify-content: center;
    gap: 1rem;
  }
  
  .date-day {
    font-size: 2rem;
  }
  
  .event-content {
    padding: 1.5rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .section-subtitle {
    font-size: 1rem;
  }
}

@media (max-width: 575.98px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 0.9rem;
  }
  
  .stat-number {
    font-size: 1.8rem;
  }
  
  .stat-label {
    font-size: 0.8rem;
  }
  
  .hero-buttons .btn {
    font-size: 1rem;
    padding: 0.75rem 1rem;
  }
  
  .section-title {
    font-size: 1.8rem;
  }
  
  .section-subtitle {
    font-size: 0.9rem;
  }
  
  .feature-card {
    padding: 1.5rem 1rem;
  }
  
  .feature-card h3 {
    font-size: 1.3rem;
  }
  
  .feature-card p {
    font-size: 0.9rem;
  }
  
  .book-title {
    font-size: 1.1rem;
  }
  
  .book-author {
    font-size: 0.9rem;
  }
  
  .book-description {
    font-size: 0.85rem;
  }
  
  .event-content h4 {
    font-size: 1.2rem;
  }
  
  .event-meta {
    font-size: 0.85rem;
  }
}

/* Container and layout improvements */
.container {
  max-width: 100%;
  margin: 0;
  padding: 0;
}

@media (max-width: 575.98px) {
  .container {
    padding: 0;
  }
}

/* Ensure proper spacing and flex layout */
.row {
  display: flex;
  flex-wrap: wrap;
  margin: 0;
  width: 100%;
}

@media (max-width: 575.98px) {
  .row {
    margin: 0;
  }
}

.col, .col-1, .col-2, .col-3, .col-4, .col-5, .col-6, .col-7, .col-8, .col-9, .col-10, .col-11, .col-12,
.col-auto, .col-sm, .col-sm-1, .col-sm-2, .col-sm-3, .col-sm-4, .col-sm-5, .col-sm-6, .col-sm-7, .col-sm-8, .col-sm-9, .col-sm-10, .col-sm-11, .col-sm-12,
.col-sm-auto, .col-md, .col-md-1, .col-md-2, .col-md-3, .col-md-4, .col-md-5, .col-md-6, .col-md-7, .col-md-8, .col-md-9, .col-md-10, .col-md-11, .col-md-12,
.col-md-auto, .col-lg, .col-lg-1, .col-lg-2, .col-lg-3, .col-lg-4, .col-lg-5, .col-lg-6, .col-lg-7, .col-lg-8, .col-lg-9, .col-lg-10, .col-lg-11, .col-lg-12,
.col-lg-auto, .col-xl, .col-xl-1, .col-xl-2, .col-xl-3, .col-xl-4, .col-xl-5, .col-xl-6, .col-xl-7, .col-xl-8, .col-xl-9, .col-xl-10, .col-xl-11, .col-xl-12,
.col-xl-auto {
  padding: 0;
  display: flex;
  flex-direction: column;
}

@media (max-width: 575.98px) {
  .col, .col-1, .col-2, .col-3, .col-4, .col-5, .col-6, .col-7, .col-8, .col-9, .col-10, .col-11, .col-12,
  .col-auto, .col-sm, .col-sm-1, .col-sm-2, .col-sm-3, .col-sm-4, .col-sm-5, .col-sm-6, .col-sm-7, .col-sm-8, .col-sm-9, .col-sm-10, .col-sm-11, .col-sm-12,
  .col-sm-auto, .col-md, .col-md-1, .col-md-2, .col-md-3, .col-md-4, .col-md-5, .col-md-6, .col-md-7, .col-md-8, .col-md-9, .col-md-10, .col-md-11, .col-md-12,
  .col-md-auto, .col-lg, .col-lg-1, .col-lg-2, .col-lg-3, .col-lg-4, .col-lg-5, .col-lg-6, .col-lg-7, .col-lg-8, .col-lg-9, .col-lg-10, .col-lg-11, .col-lg-12,
  .col-lg-auto, .col-xl, .col-xl-1, .col-xl-2, .col-xl-3, .col-xl-4, .col-xl-5, .col-xl-6, .col-xl-7, .col-xl-8, .col-xl-9, .col-xl-10, .col-xl-11, .col-xl-12,
  .col-xl-auto {
    padding: 0;
  }
}

/* Ensure proper spacing */
.py-5 {
  padding-top: 3rem !important;
  padding-bottom: 3rem !important;
}

@media (max-width: 767.98px) {
  .py-5 {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
  }
  
  .features-section .container,
  .recent-books-section .container,
  .events-section .container {
    padding: 0 1rem;
  }
}

/* Fix for overlapping elements */
.navbar {
  z-index: 1030;
  width: 100%;
}

.main-content {
  position: relative;
  z-index: 1;
  width: 100%;
  margin: 0;
  padding: 0;
}

/* Remove any default margins */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  width: 100%;
  overflow-x: hidden;
}

#app {
  width: 100%;
  margin: 0;
  padding: 0;
}

.home {
  width: 100%;
  margin: 0;
  padding: 0;
}
</style>
