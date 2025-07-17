<template>
  <div class="membership-card-container">
    <div class="card-controls">
      <button @click="showFront = true" :class="{ active: showFront }" class="card-control-btn">
        Recto
      </button>
      <button @click="showFront = false" :class="{ active: !showFront }" class="card-control-btn">
        Verso
      </button>
    </div>
    
    <div class="card-display">
      <div class="card-wrapper" :class="{ flipped: !showFront }">
        <!-- Recto de la carte -->
        <div class="card-side card-front">
          <img :src="cardFrontSrc" :alt="'Recto de la carte d\'adhésion'" class="card-image" />
          <div class="card-overlay">
            <div class="member-info">
              <h3 class="member-name">{{ memberData.name }} {{ memberData.firstName }}</h3>
              <p class="member-number">N° {{ memberData.memberNumber }}</p>
              <p class="member-date">Adhésion: {{ memberData.joinDate }}</p>
            </div>
          </div>
        </div>
        
        <!-- Verso de la carte -->
        <div class="card-side card-back">
          <img :src="cardBackSrc" :alt="'Verso de la carte d\'adhésion'" class="card-image" />
          <div class="card-overlay">
            <div class="member-details">
              <div class="detail-row">
                <span class="detail-label">Nom:</span>
                <span class="detail-value">{{ memberData.name }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Prénom:</span>
                <span class="detail-value">{{ memberData.firstName }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Date de naissance:</span>
                <span class="detail-value">{{ memberData.birthDate }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Adresse:</span>
                <span class="detail-value">{{ memberData.address }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Code Postal:</span>
                <span class="detail-value">{{ memberData.postalCode }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Ville:</span>
                <span class="detail-value">{{ memberData.city }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Téléphone:</span>
                <span class="detail-value">{{ memberData.phone }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Email:</span>
                <span class="detail-value">{{ memberData.email }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="card-actions">
      <button @click="downloadCard" class="action-btn download-btn">
        <span class="btn-icon">📥</span>
        <span class="btn-text">Télécharger</span>
      </button>
      <button @click="printCard" class="action-btn print-btn">
        <span class="btn-icon">🖨️</span>
        <span class="btn-text">Imprimer</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MembershipCard',
  props: {
    memberData: {
      type: Object,
      default: () => ({
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
      })
    }
  },
  data() {
    return {
      showFront: true
    }
  },
  computed: {
    cardFrontSrc() {
      return '/images/membership-card-front.svg'
    },
    cardBackSrc() {
      return '/images/membership-card-back.svg'
    }
  },
  methods: {
    downloadCard() {
      // Logique pour télécharger la carte
      console.log('Téléchargement de la carte...')
    },
    printCard() {
      // Logique pour imprimer la carte
      console.log('Impression de la carte...')
      window.print()
    }
  }
}
</script>

<style scoped>
.membership-card-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 2rem;
}

.card-controls {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.card-control-btn {
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 25px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.card-control-btn:hover,
.card-control-btn.active {
  background: rgba(255, 215, 0, 0.2);
  transform: translateY(-2px);
}

.card-display {
  perspective: 1000px;
  margin-bottom: 2rem;
}

.card-wrapper {
  position: relative;
  width: 400px;
  height: 250px;
  margin: 0 auto;
  transform-style: preserve-3d;
  transition: transform 0.8s ease;
}

.card-wrapper.flipped {
  transform: rotateY(180deg);
}

.card-side {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.card-front {
  transform: rotateY(0deg);
}

.card-back {
  transform: rotateY(180deg);
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.card-side:hover .card-overlay {
  opacity: 1;
}

.member-info {
  text-align: center;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.member-name {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.member-number {
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.member-date {
  font-size: 0.9rem;
  opacity: 0.9;
}

.member-details {
  background: rgba(255, 255, 255, 0.95);
  padding: 1rem;
  border-radius: 10px;
  max-width: 300px;
  font-size: 0.8rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.detail-label {
  font-weight: bold;
  color: #0057B8;
}

.detail-value {
  color: #333;
}

.card-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #0057B8, #1e3c72);
  border: none;
  border-radius: 25px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 87, 184, 0.3);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 87, 184, 0.4);
}

.download-btn {
  background: linear-gradient(135deg, #28a745, #20c997);
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

.download-btn:hover {
  box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
}

.print-btn {
  background: linear-gradient(135deg, #ffc107, #fd7e14);
  box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
}

.print-btn:hover {
  box-shadow: 0 6px 20px rgba(255, 193, 7, 0.4);
}

.btn-icon {
  font-size: 1.2rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .membership-card-container {
    padding: 1rem;
  }
  
  .card-wrapper {
    width: 300px;
    height: 188px;
  }
  
  .member-details {
    max-width: 250px;
    font-size: 0.7rem;
  }
  
  .card-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .action-btn {
    width: 200px;
    justify-content: center;
  }
}

@media print {
  .card-controls,
  .card-actions {
    display: none;
  }
  
  .card-wrapper {
    transform: none !important;
  }
  
  .card-side {
    position: relative;
    margin-bottom: 2rem;
  }
  
  .card-back {
    transform: none;
  }
}
</style> 