<script setup>
import { useI18n } from 'vue-i18n'
import NavBar from './components/NavBar.vue'
import SunflowerIcon from './components/icons/SunflowerIcon.vue'
import NotificationToast from './components/NotificationToast.vue'
import { onMounted, ref } from 'vue'

const { t } = useI18n()
const notificationToast = ref(null)

onMounted(() => {
  startFooterAnimations();
  // Exposer les notifications globalement
  window.$notify = {
    success: (title, message) => notificationToast.value?.success(title, message),
    error: (title, message) => notificationToast.value?.error(title, message),
    warning: (title, message) => notificationToast.value?.warning(title, message),
    info: (title, message) => notificationToast.value?.info(title, message)
  }
});

function getFooterParticleStyle(index) {
  const size = Math.random() * 3 + 1;
  const x = Math.random() * 100;
  const y = Math.random() * 100;
  const delay = Math.random() * 8;
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${x}%`,
    top: `${y}%`,
    animationDelay: `${delay}s`
  };
}

function getFooterBookStyle(index) {
  const x = Math.random() * 100;
  const y = Math.random() * 100;
  const rotation = Math.random() * 360;
  const delay = Math.random() * 12;
  return {
    left: `${x}%`,
    top: `${y}%`,
    transform: `rotate(${rotation}deg)`,
    animationDelay: `${delay}s`
  };
}

function startFooterAnimations() {
  // Animation des particules du footer
  setInterval(() => {
    document.querySelectorAll('.footer-particle').forEach(particle => {
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      particle.style.transform = `translate(${x}px, ${y}px)`;
    });
  }, 5000);
  
  // Animation des livres du footer
  setInterval(() => {
    document.querySelectorAll('.footer-book').forEach(book => {
      const rotation = Math.random() * 360;
      const scale = 0.4 + Math.random() * 0.3;
      book.style.transform = `rotate(${rotation}deg) scale(${scale})`;
    });
  }, 8000);
}
</script>

<template>
  <div id="app">
    <!-- Navbar -->
    <NavBar />
    
    <!-- Contenu principal -->
    <main class="main-content">
      <router-view />
    </main>
    
    <!-- Composant de notifications -->
    <NotificationToast ref="notificationToast" />
    
    <!-- Footer magnifique -->
    <footer class="footer">
      <!-- Effet de fond avec particules -->
      <div class="footer-background">
        <div class="footer-particles">
          <div v-for="i in 15" :key="i" class="footer-particle" :style="getFooterParticleStyle(i)"></div>
        </div>
        <div class="footer-gradient"></div>
      </div>
      
      <!-- Livres flottants dans le footer -->
      <div class="footer-floating-books">
        <div v-for="i in 6" :key="i" class="footer-book" :style="getFooterBookStyle(i)">
          <div class="footer-book-cover"></div>
          <div class="footer-book-pages"></div>
        </div>
      </div>
      
      <div class="footer-content">
        <div class="footer-container">
          <!-- Section principale -->
          <div class="footer-main">
                          <div class="footer-brand">
                <div class="footer-logo">
                  <div class="footer-logo-icon">
                    <SunflowerIcon size="medium" variant="icon" :animated="true" />
                  </div>
                  <div class="footer-logo-text">
                    <h3 class="footer-title">{{ t('footer.title') }}</h3>
                    <p class="footer-subtitle">{{ t('footer.subtitle') }}</p>
                  </div>
                </div>
              <p class="footer-description">{{ t('footer.description') }}</p>
            </div>
            
            <!-- Liens rapides -->
            <div class="footer-links">
              <div class="footer-section">
                <h4 class="footer-section-title">{{ t('footer.navigation') }}</h4>
                <ul class="footer-link-list">
                  <li><router-link to="/" class="footer-link">{{ t('nav.home') }}</router-link></li>
                  <li><router-link to="/books" class="footer-link">{{ t('nav.books') }}</router-link></li>
                  <li><router-link to="/events" class="footer-link">{{ t('nav.events') }}</router-link></li>
                  <li><router-link to="/association" class="footer-link">{{ t('nav.association') }}</router-link></li>
                  <li><router-link to="/chatbot" class="footer-link">{{ t('nav.chatbot') }}</router-link></li>
                </ul>
              </div>
              
              <div class="footer-section">
                <h4 class="footer-section-title">{{ t('footer.resources') }}</h4>
                <ul class="footer-link-list">
                  <li><a href="#" class="footer-link">{{ t('footer.library') }}</a></li>
                  <li><a href="#" class="footer-link">{{ t('footer.exhibitions') }}</a></li>
                  <li><a href="#" class="footer-link">{{ t('footer.music') }}</a></li>
                  <li><a href="#" class="footer-link">{{ t('footer.artists') }}</a></li>
                  <li><a href="#" class="footer-link">{{ t('footer.history') }}</a></li>
                </ul>
              </div>
              
              <div class="footer-section">
                <h4 class="footer-section-title">{{ t('footer.community') }}</h4>
                <ul class="footer-link-list">
                  <li><a href="#" class="footer-link">{{ t('footer.membership') }}</a></li>
                  <li><a href="#" class="footer-link">{{ t('footer.volunteering') }}</a></li>
                  <li><a href="#" class="footer-link">{{ t('footer.donations') }}</a></li>
                  <li><a href="#" class="footer-link">{{ t('footer.partners') }}</a></li>
                  <li><a href="#" class="footer-link">{{ t('footer.contact') }}</a></li>
                </ul>
              </div>
            </div>
          </div>
          
          <!-- Section réseaux sociaux -->
          <div class="footer-social">
            <h4 class="footer-section-title">{{ t('footer.followUs') }}</h4>
            <div class="social-links">
              <a href="#" class="social-link" title="Facebook">
                <span class="social-icon">📘</span>
              </a>
              <a href="#" class="social-link" title="Twitter">
                <span class="social-icon">🐦</span>
              </a>
              <a href="#" class="social-link" title="Instagram">
                <span class="social-icon">📷</span>
              </a>
              <a href="#" class="social-link" title="YouTube">
                <span class="social-icon">📺</span>
              </a>
              <a href="#" class="social-link" title="LinkedIn">
                <span class="social-icon">💼</span>
              </a>
            </div>
          </div>
    </div>
        
        <!-- Barre de copyright -->
        <div class="footer-bottom">
          <div class="footer-bottom-content">
            <p class="copyright">
              © 2024 Lumières d'Ukraine. {{ t('footer.allRightsReserved') }}.
            </p>
            <div class="footer-bottom-links">
              <a href="#" class="footer-bottom-link">{{ t('footer.legalNotices') }}</a>
              <a href="#" class="footer-bottom-link">{{ t('footer.privacyPolicy') }}</a>
              <a href="#" class="footer-bottom-link">{{ t('footer.termsOfUse') }}</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.main-content {
  min-height: calc(100vh - 80px);
  padding-top: 80px;
  position: relative;
  z-index: 10;
}

/* Footer */
.footer {
  position: relative;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #0056b3 100%);
  color: white;
  overflow: hidden;
  min-height: 400px;
}

/* Fond du footer avec particules */
.footer-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.footer-particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.footer-particle {
  position: absolute;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  animation: footerParticleFloat 10s ease-in-out infinite;
  pointer-events: none;
}

@keyframes footerParticleFloat {
  0%, 100% { transform: translateY(0px) scale(1); opacity: 0.2; }
  50% { transform: translateY(-25px) scale(1.3); opacity: 0.6; }
}

.footer-gradient {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 30% 20%, rgba(255, 215, 0, 0.2) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(0, 86, 179, 0.3) 0%, transparent 50%);
}

/* Livres flottants dans le footer */
.footer-floating-books {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

.footer-book {
  position: absolute;
  width: 25px;
  height: 35px;
  animation: footerBookFloat 12s ease-in-out infinite;
  opacity: 0.4;
}

.footer-book-cover {
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  border-radius: 2px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.2);
  position: relative;
}

.footer-book-pages {
  position: absolute;
  top: 1px;
  left: 1px;
  right: 1px;
  bottom: 1px;
  background: white;
  border-radius: 1px;
}

@keyframes footerBookFloat {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-30px) rotate(5deg); }
}

/* Contenu du footer */
.footer-content {
  position: relative;
  z-index: 10;
  padding: 4rem 2rem 2rem;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-main {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 4rem;
  margin-bottom: 3rem;
}

/* Section marque */
.footer-brand {
  max-width: 400px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.footer-logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}



@keyframes logoPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.footer-title {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 0.25rem;
  background: linear-gradient(45deg, #ffffff, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-subtitle {
  font-size: 0.9rem;
  opacity: 0.8;
  font-weight: 400;
}

.footer-description {
  line-height: 1.6;
  opacity: 0.9;
  margin-bottom: 2rem;
}

/* Liens du footer */
.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.footer-section-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #ffd700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.footer-link-list {
  list-style: none;
  padding: 0;
}

.footer-link-list li {
  margin-bottom: 0.75rem;
}

.footer-link {
  color: white;
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
  padding-left: 0;
}

.footer-link::before {
  content: '→';
  position: absolute;
  left: -15px;
  opacity: 0;
  transition: all 0.3s ease;
  color: #ffd700;
}

.footer-link:hover {
  color: #ffd700;
  padding-left: 15px;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.footer-link:hover::before {
  opacity: 1;
}

/* Réseaux sociaux */
.footer-social {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.social-links {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.social-link:hover {
  background: rgba(255, 215, 0, 0.2);
  transform: translateY(-3px) scale(1.1);
  box-shadow: 0 8px 25px rgba(255, 215, 0, 0.3);
}

.social-icon {
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

.social-link:hover .social-icon {
  transform: scale(1.2);
}

/* Barre de copyright */
.footer-bottom {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.footer-bottom-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.copyright {
  opacity: 0.8;
  font-size: 0.9rem;
}

.footer-bottom-links {
    display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.footer-bottom-link {
  color: white;
  text-decoration: none;
  font-size: 0.9rem;
  opacity: 0.8;
  transition: all 0.3s ease;
}

.footer-bottom-link:hover {
  color: #ffd700;
  opacity: 1;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .footer-main {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
  
  .footer-brand {
    max-width: 100%;
    text-align: center;
  }
  
  .footer-logo {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .footer-content {
    padding: 3rem 1rem 1.5rem;
  }
  
  .footer-links {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .footer-bottom-content {
    flex-direction: column;
    text-align: center;
  }
  
  .footer-bottom-links {
    justify-content: center;
  }
  
  .social-links {
    gap: 1rem;
  }
  
  .social-link {
    width: 45px;
    height: 45px;
  }
}

@media (max-width: 480px) {
  .footer-main {
    gap: 2rem;
  }
  
  .footer-title {
    font-size: 1.3rem;
  }
  
  .footer-section-title {
    font-size: 1rem;
  }
  
  .social-links {
    gap: 0.75rem;
  }
  
  .social-link {
    width: 40px;
    height: 40px;
  }
  
  .social-icon {
    font-size: 1.2rem;
  }
}
</style>
