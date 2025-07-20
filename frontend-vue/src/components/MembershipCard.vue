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
          <div class="card-overlay front-overlay">
            <div class="member-info">
              <h3 class="member-name">{{ memberData.firstName }} {{ memberData.name }}</h3>
              <p class="member-number">N° {{ memberData.memberNumber || '2024-001' }}</p>
              <p class="member-date">Adhésion: {{ memberData.joinDate || '17/07/2024' }}</p>
            </div>
          </div>
        </div>

        <!-- Verso de la carte -->
        <div class="card-side card-back">
          <div class="card-back-content">
            <div class="card-back-header">
              <h3>Les Lumières d'Ukraine</h3>
              <p>Carte d'Adhésion</p>
            </div>
            <div class="member-details">
              <div class="detail-row">
                <span class="detail-label">Nom:</span>
                <span class="detail-value">{{ memberData.name || 'Dupont' }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Prénom:</span>
                <span class="detail-value">{{ memberData.firstName || 'Jean' }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Date de naissance:</span>
                <span class="detail-value">{{ memberData.birthDate || '15/03/1985' }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Adresse:</span>
                <span class="detail-value">{{ memberData.address || '123 Rue de la Paix' }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Code Postal:</span>
                <span class="detail-value">{{ memberData.postalCode || '54000' }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Ville:</span>
                <span class="detail-value">{{ memberData.city || 'Nancy' }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Téléphone:</span>
                <span class="detail-value">{{ memberData.phone || '03 83 12 34 56' }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Email:</span>
                <span class="detail-value">{{ memberData.email || 'jean.dupont@email.com' }}</span>
              </div>
            </div>
            <div class="card-back-footer">
              <div class="barcode">
                <div class="barcode-lines">
                  <div
                    v-for="i in 20"
                    :key="i"
                    class="barcode-line"
                    :style="{ height: Math.random() * 40 + 20 + 'px' }"
                  ></div>
                </div>
                <p class="barcode-number">{{ memberData.memberNumber || '2024-001' }}</p>
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
      <button @click="sendCardToMember" class="action-btn send-btn">
        <span class="btn-icon">📧</span>
        <span class="btn-text">Envoyer par Email</span>
      </button>
      <button @click="printCard" class="action-btn print-btn">
        <span class="btn-icon">🖨️</span>
        <span class="btn-text">Imprimer</span>
      </button>
    </div>

    <!-- Modal pour l'envoi par email -->
    <div v-if="showEmailModal" class="email-modal-overlay" @click="closeEmailModal">
      <div class="email-modal" @click.stop>
        <h3>Envoyer la carte d'adhésion</h3>
        <form @submit.prevent="sendEmail">
          <div class="form-group">
            <label for="email">Email de l'abonné:</label>
            <input
              type="email"
              id="email"
              v-model="emailData.email"
              required
              placeholder="exemple@email.com"
            />
          </div>
          <div class="form-group">
            <label for="subject">Sujet:</label>
            <input
              type="text"
              id="subject"
              v-model="emailData.subject"
              required
              placeholder="Votre carte d'adhésion - Les Lumières d'Ukraine"
            />
          </div>
          <div class="form-group">
            <label for="message">Message:</label>
            <textarea
              id="message"
              v-model="emailData.message"
              rows="4"
              placeholder="Message personnalisé..."
            ></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeEmailModal" class="btn-cancel">Annuler</button>
            <button type="submit" class="btn-send">Envoyer</button>
          </div>
        </form>
      </div>
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
        email: 'jean.dupont@email.com',
      }),
    },
  },
  data() {
    return {
      showFront: true,
      showEmailModal: false,
      emailData: {
        email: '',
        subject: "Votre carte d'adhésion - Les Lumières d'Ukraine",
        message: `Bonjour ${this.memberData.firstName || 'Jean'} ${this.memberData.name || 'Dupont'},

Nous avons le plaisir de vous confirmer votre adhésion à l'association "Les Lumières d'Ukraine".

Votre numéro d'adhésion est : ${this.memberData.memberNumber || '2024-001'}

Vous trouverez ci-joint votre carte d'adhésion recto-verso.

Bienvenue dans notre association !

L'équipe des Lumières d'Ukraine`,
      },
    }
  },
  computed: {
    cardFrontSrc() {
      return '/images/membership-card-front.png'
    },
  },
  methods: {
    downloadCard() {
      // Logique simplifiée pour le téléchargement
      console.log('Téléchargement de la carte...')
      alert('Fonctionnalité de téléchargement en cours de développement')
    },

    sendCardToMember() {
      this.emailData.email = this.memberData.email || 'exemple@email.com'
      this.showEmailModal = true
    },

    closeEmailModal() {
      this.showEmailModal = false
    },

    sendEmail() {
      // Logique simplifiée pour l'envoi d'email
      console.log('Envoi de la carte par email...')
      alert("Fonctionnalité d'envoi par email en cours de développement")
      this.closeEmailModal()
    },

    printCard() {
      window.print()
    },
  },
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
  background: linear-gradient(135deg, #0057b8, #1e3c72);
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: white;
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

.front-overlay {
  background: rgba(0, 0, 0, 0.05);
  justify-content: flex-end;
  align-items: flex-end;
  padding: 1rem;
}

.card-side:hover .card-overlay {
  opacity: 1;
}

.member-info {
  text-align: center;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  background: rgba(0, 0, 0, 0.3);
  padding: 0.5rem;
  border-radius: 8px;
  backdrop-filter: blur(5px);
}

.member-name {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.member-number {
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.member-date {
  font-size: 0.8rem;
  opacity: 0.9;
}

.card-back-content {
  padding: 1rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  color: white;
}

.card-back-header {
  text-align: center;
  margin-bottom: 1rem;
}

.card-back-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #ffd700;
}

.card-back-header p {
  margin: 0.25rem 0 0 0;
  font-size: 0.9rem;
  opacity: 0.9;
}

.member-details {
  flex: 1;
  background: rgba(255, 255, 255, 0.95);
  padding: 1rem;
  border-radius: 10px;
  font-size: 0.8rem;
  color: #333;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.detail-label {
  font-weight: bold;
  color: #0057b8;
}

.detail-value {
  color: #333;
}

.card-back-footer {
  margin-top: 1rem;
  text-align: center;
}

.barcode {
  display: inline-block;
  background: white;
  padding: 0.5rem;
  border-radius: 5px;
}

.barcode-lines {
  display: flex;
  gap: 1px;
  margin-bottom: 0.25rem;
}

.barcode-line {
  width: 2px;
  background: black;
  min-height: 20px;
}

.barcode-number {
  font-size: 0.7rem;
  color: #333;
  margin: 0;
  font-family: monospace;
}

.card-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #0057b8, #1e3c72);
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

.send-btn {
  background: linear-gradient(135deg, #007bff, #0056b3);
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
}

.send-btn:hover {
  box-shadow: 0 6px 20px rgba(0, 123, 255, 0.4);
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

/* Modal Email */
.email-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.email-modal {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.email-modal h3 {
  margin: 0 0 1.5rem 0;
  color: #0057b8;
  text-align: center;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #0057b8;
  box-shadow: 0 0 0 3px rgba(0, 87, 184, 0.1);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.btn-cancel,
.btn-send {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-cancel {
  background: #6c757d;
  color: white;
}

.btn-cancel:hover {
  background: #5a6268;
}

.btn-send {
  background: #28a745;
  color: white;
}

.btn-send:hover {
  background: #218838;
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

  .email-modal {
    margin: 1rem;
    padding: 1.5rem;
  }

  .modal-actions {
    flex-direction: column;
  }
}

@media print {
  .card-controls,
  .card-actions,
  .email-modal-overlay {
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
