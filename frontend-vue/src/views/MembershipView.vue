<template>
  <div class="membership-view">
    <!-- En-tête avec tournesol -->
    <div class="membership-header">
      <div class="header-content">
        <div class="header-symbol">
          <SunflowerIcon size="xlarge" variant="full" :animated="true" />
        </div>
        <div class="header-text">
          <h1 class="page-title">Adhésion à l'Association</h1>
          <p class="page-subtitle">
            Rejoignez Les Lumières d'Ukraine et découvrez la richesse de la culture ukrainienne
          </p>
        </div>
      </div>
    </div>

    <!-- Navigation des sections -->
    <div class="section-nav">
      <button 
        @click="activeSection = 'form'" 
        :class="{ active: activeSection === 'form' }" 
        class="nav-btn"
      >
        <span class="nav-icon">📝</span>
        <span class="nav-text">Bulletin d'Adhésion</span>
      </button>
      <button 
        @click="activeSection = 'card'" 
        :class="{ active: activeSection === 'card' }" 
        class="nav-btn"
      >
        <span class="nav-icon">🪪</span>
        <span class="nav-text">Carte d'Adhésion</span>
      </button>
      <button 
        @click="activeSection = 'info'" 
        :class="{ active: activeSection === 'info' }" 
        class="nav-btn"
      >
        <span class="nav-icon">ℹ️</span>
        <span class="nav-text">Informations</span>
      </button>
    </div>

    <!-- Contenu des sections -->
    <div class="section-content">
      <!-- Section Formulaire -->
      <div v-if="activeSection === 'form'" class="section-panel">
        <MembershipForm />
      </div>

      <!-- Section Carte d'adhésion -->
      <div v-if="activeSection === 'card'" class="section-panel">
        <div class="card-demo">
          <h2 class="section-title">Votre Carte d'Adhésion</h2>
          <p class="section-description">
            Découvrez à quoi ressemblera votre carte d'adhésion personnalisée
          </p>
          <MembershipCard :memberData="demoMemberData" />
        </div>
      </div>

      <!-- Section Informations -->
      <div v-if="activeSection === 'info'" class="section-panel">
        <div class="info-content">
          <h2 class="section-title">Informations sur l'Adhésion</h2>
          
          <div class="info-grid">
            <div class="info-card">
              <div class="info-icon">💰</div>
              <h3 class="info-title">Tarifs d'Adhésion</h3>
              <ul class="info-list">
                <li><strong>Adhésion individuelle :</strong> 25€/an</li>
                <li><strong>Adhésion familiale :</strong> 40€/an</li>
                <li><strong>Adhésion étudiant :</strong> 15€/an</li>
                <li><strong>Adhésion senior :</strong> 20€/an</li>
              </ul>
            </div>

            <div class="info-card">
              <div class="info-icon">🎁</div>
              <h3 class="info-title">Avantages Membres</h3>
              <ul class="info-list">
                <li>Accès à la bibliothèque virtuelle</li>
                <li>Invitations aux événements culturels</li>
                <li>Réductions sur les activités</li>
                <li>Newsletter mensuelle</li>
                <li>Support à la culture ukrainienne</li>
              </ul>
            </div>

            <div class="info-card">
              <div class="info-icon">📋</div>
              <h3 class="info-title">Processus d'Adhésion</h3>
              <ol class="info-list">
                <li>Remplir le bulletin d'adhésion</li>
                <li>Payer la cotisation annuelle</li>
                <li>Recevoir votre carte d'adhésion</li>
                <li>Accéder aux services membres</li>
              </ol>
            </div>

            <div class="info-card">
              <div class="info-icon">📞</div>
              <h3 class="info-title">Contact</h3>
              <div class="contact-info">
                <p><strong>Adresse :</strong><br>Centre d'action Social<br>7, rue Léopold Lallement<br>54000 NANCY</p>
                <p><strong>Téléphone :</strong> 03 83 XX XX XX</p>
                <p><strong>Email :</strong> contact@lumières-ukraine.fr</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Call-to-action -->
    <div class="cta-section">
      <div class="cta-content">
        <h2 class="cta-title">Prêt à nous rejoindre ?</h2>
        <p class="cta-subtitle">
          Rejoignez notre communauté et participez à la promotion de la culture ukrainienne
        </p>
        <button @click="activeSection = 'form'" class="cta-button">
          <span class="btn-icon">🌟</span>
          <span class="btn-text">Devenir Membre</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import SunflowerIcon from '../components/icons/SunflowerIcon.vue'
import MembershipForm from '../components/MembershipForm.vue'
import MembershipCard from '../components/MembershipCard.vue'

export default {
  name: 'MembershipView',
  components: {
    SunflowerIcon,
    MembershipForm,
    MembershipCard
  },
  data() {
    return {
      activeSection: 'form',
      demoMemberData: {
        name: 'Dupont',
        firstName: 'Jean',
        memberNumber: '2024-001',
        joinDate: '17/07/2024',
        birthDate: '15/03/1985',
        address: '123 Rue de la Paix',
        postalCode: '54000',
        city: 'Nancy',
        phone: '03 83 12 34 56',
        email: 'jean.dupont@email.com'
      }
    }
  }
}
</script>

<style scoped>
.membership-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #0056b3 100%);
  color: white;
}

/* En-tête */
.membership-header {
  padding: 4rem 2rem;
  text-align: center;
}

.header-content {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.header-symbol {
  animation: headerFloat 6s ease-in-out infinite;
}

@keyframes headerFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.page-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, #ffffff, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 1.3rem;
  opacity: 0.9;
  line-height: 1.6;
}

/* Navigation des sections */
.section-nav {
  display: flex;
  justify-content: center;
  gap: 1rem;
  padding: 0 2rem 2rem;
  flex-wrap: wrap;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 25px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.nav-btn:hover,
.nav-btn.active {
  background: rgba(255, 215, 0, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.nav-icon {
  font-size: 1.2rem;
}

/* Contenu des sections */
.section-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem 4rem;
}

.section-panel {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-align: center;
  color: #ffd700;
}

.section-description {
  text-align: center;
  font-size: 1.1rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

/* Section Carte */
.card-demo {
  text-align: center;
}

/* Section Informations */
.info-content {
  max-width: 1000px;
  margin: 0 auto;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.info-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 2rem;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s ease;
}

.info-card:hover {
  transform: translateY(-5px);
}

.info-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.info-title {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #ffd700;
}

.info-list {
  text-align: left;
  list-style: none;
  padding: 0;
}

.info-list li {
  margin-bottom: 0.5rem;
  padding-left: 1rem;
  position: relative;
}

.info-list li::before {
  content: '•';
  color: #ffd700;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.contact-info p {
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

/* Call-to-action */
.cta-section {
  background: rgba(0, 0, 0, 0.3);
  padding: 4rem 2rem;
  text-align: center;
}

.cta-content {
  max-width: 600px;
  margin: 0 auto;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #ffd700;
}

.cta-subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  border: none;
  border-radius: 25px;
  color: #1e3c72;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
}

.btn-icon {
  font-size: 1.2rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .membership-header {
    padding: 2rem 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .page-subtitle {
    font-size: 1.1rem;
  }
  
  .section-nav {
    padding: 0 1rem 1rem;
  }
  
  .nav-btn {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }
  
  .section-content {
    padding: 0 1rem 2rem;
  }
  
  .section-panel {
    padding: 1rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .cta-section {
    padding: 2rem 1rem;
  }
  
  .cta-title {
    font-size: 2rem;
  }
}
</style> 