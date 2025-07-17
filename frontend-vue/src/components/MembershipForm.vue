<template>
  <div class="membership-form-container">
    <div class="form-header">
      <h2 class="form-title">Bulletin d'Adhésion</h2>
      <p class="form-subtitle">Rejoignez l'association Les Lumières d'Ukraine</p>
    </div>
    
    <div class="form-content">
      <!-- Formulaire interactif -->
      <div class="interactive-form">
        <form @submit.prevent="submitForm" class="membership-form">
          <div class="form-section">
            <h3 class="section-title">Informations Personnelles</h3>
            
            <div class="form-row">
              <div class="form-group">
                <label for="lastName" class="form-label">Nom *</label>
                <input 
                  id="lastName"
                  v-model="formData.lastName"
                  type="text" 
                  class="form-input" 
                  required
                  placeholder="Votre nom"
                />
              </div>
              
              <div class="form-group">
                <label for="firstName" class="form-label">Prénom *</label>
                <input 
                  id="firstName"
                  v-model="formData.firstName"
                  type="text" 
                  class="form-input" 
                  required
                  placeholder="Votre prénom"
                />
              </div>
            </div>
            
            <div class="form-group">
              <label for="address" class="form-label">Adresse *</label>
              <input 
                id="address"
                v-model="formData.address"
                type="text" 
                class="form-input" 
                required
                placeholder="Votre adresse complète"
              />
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="postalCode" class="form-label">Code Postal *</label>
                <input 
                  id="postalCode"
                  v-model="formData.postalCode"
                  type="text" 
                  class="form-input" 
                  required
                  placeholder="54000"
                />
              </div>
              
              <div class="form-group">
                <label for="city" class="form-label">Ville *</label>
                <input 
                  id="city"
                  v-model="formData.city"
                  type="text" 
                  class="form-input" 
                  required
                  placeholder="Nancy"
                />
              </div>
            </div>
            
            <div class="form-group">
              <label for="birthDate" class="form-label">Date de naissance *</label>
              <input 
                id="birthDate"
                v-model="formData.birthDate"
                type="date" 
                class="form-input" 
                required
              />
            </div>
            
            <div class="form-group">
              <label for="phone" class="form-label">Téléphone *</label>
              <input 
                id="phone"
                v-model="formData.phone"
                type="tel" 
                class="form-input" 
                required
                placeholder="03 83 12 34 56"
              />
            </div>
            
            <div class="form-group">
              <label for="email" class="form-label">Email *</label>
              <input 
                id="email"
                v-model="formData.email"
                type="email" 
                class="form-input" 
                required
                placeholder="votre.email@example.com"
              />
            </div>
          </div>
          
          <div class="form-section">
            <h3 class="section-title">Adhésion</h3>
            
            <div class="form-group">
              <label for="membershipType" class="form-label">Type d'adhésion *</label>
              <select 
                id="membershipType"
                v-model="formData.membershipType"
                class="form-select" 
                required
              >
                <option value="">Choisissez un type</option>
                <option value="individual">Adhésion individuelle (25€/an)</option>
                <option value="family">Adhésion familiale (40€/an)</option>
                <option value="student">Adhésion étudiant (15€/an)</option>
                <option value="senior">Adhésion senior (20€/an)</option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label">Montant de la cotisation</label>
              <div class="membership-amount">
                <span class="amount-value">{{ getMembershipAmount() }}€</span>
                <span class="amount-period">/ année</span>
              </div>
            </div>
          </div>
          
          <div class="form-section">
            <h3 class="section-title">Déclaration</h3>
            
            <div class="declaration-box">
              <p class="declaration-text">
                Je déclare par la présente souhaiter devenir membre de l'association 
                Les Lumières d'Ukraine à Nancy.
              </p>
              <p class="declaration-text">
                J'ai pris bonne note des droits et des devoirs des membres de l'association, 
                et accepte de verser ma cotisation due pour l'année en cours.
              </p>
            </div>
            
            <div class="form-group checkbox-group">
              <label class="checkbox-label">
                <input 
                  v-model="formData.agreement"
                  type="checkbox" 
                  class="form-checkbox" 
                  required
                />
                <span class="checkbox-text">
                  J'accepte les conditions d'adhésion et la politique de confidentialité *
                </span>
              </label>
            </div>
          </div>
          
          <div class="form-actions">
            <button type="submit" class="submit-btn" :disabled="!isFormValid">
              <span class="btn-icon">📝</span>
              <span class="btn-text">Soumettre l'adhésion</span>
            </button>
            
            <button type="button" @click="previewForm" class="preview-btn">
              <span class="btn-icon">👁️</span>
              <span class="btn-text">Aperçu du bulletin</span>
            </button>
          </div>
        </form>
      </div>
      
      <!-- Aperçu du bulletin -->
      <div v-if="showPreview" class="form-preview">
        <div class="preview-header">
          <h3>Aperçu du Bulletin d'Adhésion</h3>
          <button @click="showPreview = false" class="close-btn">×</button>
        </div>
        <div class="preview-content">
          <img :src="formPreviewSrc" alt="Aperçu du bulletin d'adhésion" class="preview-image" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MembershipForm',
  data() {
    return {
      showPreview: false,
      formData: {
        lastName: '',
        firstName: '',
        address: '',
        postalCode: '',
        city: '',
        birthDate: '',
        phone: '',
        email: '',
        membershipType: '',
        agreement: false
      }
    }
  },
  computed: {
    formPreviewSrc() {
      return '/images/membership-form.svg'
    },
    isFormValid() {
      return this.formData.lastName && 
             this.formData.firstName && 
             this.formData.address && 
             this.formData.postalCode && 
             this.formData.city && 
             this.formData.birthDate && 
             this.formData.phone && 
             this.formData.email && 
             this.formData.membershipType && 
             this.formData.agreement
    }
  },
  methods: {
    getMembershipAmount() {
      const amounts = {
        individual: 25,
        family: 40,
        student: 15,
        senior: 20
      }
      return amounts[this.formData.membershipType] || 0
    },
    submitForm() {
      if (this.isFormValid) {
        // Logique pour soumettre le formulaire
        console.log('Soumission du formulaire:', this.formData)
        alert('Votre demande d\'adhésion a été soumise avec succès !')
      }
    },
    previewForm() {
      this.showPreview = true
    }
  }
}
</script>

<style scoped>
.membership-form-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.form-header {
  text-align: center;
  margin-bottom: 3rem;
}

.form-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #0057B8;
  margin-bottom: 0.5rem;
}

.form-subtitle {
  font-size: 1.2rem;
  color: #666;
}

.form-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

.interactive-form {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.3rem;
  font-weight: bold;
  color: #0057B8;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #FFD700;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.form-input,
.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #0057B8;
  box-shadow: 0 0 0 3px rgba(0, 87, 184, 0.1);
}

.membership-amount {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  padding: 1rem;
  background: linear-gradient(135deg, #0057B8, #1e3c72);
  color: white;
  border-radius: 8px;
}

.amount-value {
  font-size: 2rem;
  font-weight: bold;
}

.amount-period {
  font-size: 1rem;
  opacity: 0.9;
}

.declaration-box {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #0057B8;
  margin-bottom: 1rem;
}

.declaration-text {
  margin-bottom: 1rem;
  line-height: 1.6;
  color: #333;
}

.checkbox-group {
  margin-top: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  cursor: pointer;
}

.form-checkbox {
  margin-top: 0.25rem;
  transform: scale(1.2);
}

.checkbox-text {
  line-height: 1.4;
  color: #333;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.submit-btn,
.preview-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.preview-btn {
  background: linear-gradient(135deg, #ffc107, #fd7e14);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
}

.preview-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 193, 7, 0.4);
}

.btn-icon {
  font-size: 1.2rem;
}

/* Aperçu du bulletin */
.form-preview {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #0057B8, #1e3c72);
  color: white;
}

.preview-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.preview-content {
  padding: 2rem;
  text-align: center;
}

.preview-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

/* Responsive Design */
@media (max-width: 768px) {
  .membership-form-container {
    padding: 1rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .submit-btn,
  .preview-btn {
    width: 100%;
    justify-content: center;
  }
  
  .preview-header {
    padding: 1rem;
  }
  
  .preview-content {
    padding: 1rem;
  }
}

@media (min-width: 1024px) {
  .form-content {
    grid-template-columns: 1fr 1fr;
  }
}
</style> 