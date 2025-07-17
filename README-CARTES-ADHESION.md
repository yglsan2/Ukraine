# 🌻 Système de Cartes d'Adhésion - Les Lumières d'Ukraine

## 📋 Vue d'ensemble

Ce système permet de générer, personnaliser et envoyer des cartes d'adhésion recto-verso aux membres de l'association "Les Lumières d'Ukraine".

## ✨ Fonctionnalités

### 🎨 Interface Frontend
- **Formulaire d'adhésion** : Saisie des informations du membre
- **Aperçu en temps réel** : Visualisation de la carte avant génération
- **Génération automatique** : Numéros d'adhésion uniques
- **Animation 3D** : Effet de retournement recto/verso
- **Design responsive** : Compatible mobile et desktop

### 🔧 Backend API
- **Génération de cartes** : Création d'images PNG/PDF
- **Envoi par email** : Envoi automatique avec pièces jointes
- **Validation des données** : Vérification des informations
- **Stockage sécurisé** : Sauvegarde des cartes générées
- **Gestion des numéros** : Attribution automatique d'identifiants uniques

## 🚀 Installation et Configuration

### Prérequis
- Node.js 18+ et npm
- Java 17+ et Maven
- Base de données PostgreSQL (optionnel pour le développement)

### Frontend (Vue.js)
```bash
cd frontend-vue
npm install
npm run dev
```

### Backend (Spring Boot)
```bash
cd backend
mvn clean install
mvn spring-boot:run
```

## 📱 Utilisation

### 1. Accès à l'interface
- Ouvrir `http://localhost:5194/association` dans votre navigateur
- Cliquer sur "Adhésion" dans la navigation

### 2. Saisie des informations
- Remplir le formulaire avec les données du membre
- Champs obligatoires : Prénom, Nom, Email
- Champs optionnels : Date de naissance, adresse, téléphone

### 3. Génération du numéro d'adhésion
- Cliquer sur "🔢 Générer numéro" pour obtenir un identifiant unique
- Format : `YYYY-NNN` (ex: 2024-001)

### 4. Aperçu de la carte
- La carte s'affiche automatiquement une fois le numéro généré
- Utiliser les boutons "Recto" et "Verso" pour voir les deux faces
- Effet de retournement 3D avec animation

### 5. Actions disponibles
- **Générer & Télécharger** : Crée un PDF avec recto et verso
- **Envoyer par Email** : Envoie la carte par email au membre
- **Imprimer** : Impression directe depuis le navigateur

## 🎨 Design de la Carte

### Recto (Face avant)
- Image officielle de l'association avec tournesol
- Nom et prénom du membre
- Numéro d'adhésion
- Date d'adhésion

### Verso (Face arrière)
- Informations complètes du membre
- Code-barres avec numéro d'adhésion
- Design aux couleurs de l'Ukraine (bleu et jaune)

## 📧 Système d'Email

### Configuration
```yaml
# application.yml
spring:
  mail:
    host: smtp.gmail.com
    port: 587
    username: votre-email@gmail.com
    password: votre-mot-de-passe-app
    properties:
      mail:
        smtp:
          auth: true
          starttls:
            enable: true
```

### Template d'email
- Design HTML professionnel
- Couleurs de l'Ukraine
- Informations du membre
- Pièces jointes : recto et verso de la carte

## 🔌 API Endpoints

### Génération de cartes
```http
POST /api/membership/generate-card
Content-Type: application/json

{
  "memberData": {
    "name": "Dupont",
    "firstName": "Jean",
    "memberNumber": "2024-001",
    "email": "jean.dupont@email.com",
    ...
  }
}
```

### Envoi par email
```http
POST /api/membership/send-card
Content-Type: application/json

{
  "memberData": {...},
  "emailData": {
    "to": "membre@email.com",
    "subject": "Votre carte d'adhésion",
    "message": "Message personnalisé..."
  }
}
```

### Téléchargement PDF
```http
POST /api/membership/download-pdf
Content-Type: application/json

{
  "memberData": {...}
}
```

## 🛠️ Personnalisation

### Modification du design
1. **Recto** : Remplacer `/public/images/membership-card-front.png`
2. **Styles** : Modifier `MembershipCard.vue`
3. **Couleurs** : Ajuster les variables CSS dans les composants

### Ajout de champs
1. Modifier `MembershipCardRequest.MemberData`
2. Mettre à jour le formulaire dans `MembershipView.vue`
3. Adapter l'affichage dans `MembershipCard.vue`

### Intégration avec une base de données
1. Créer les entités JPA correspondantes
2. Ajouter les repositories Spring Data
3. Modifier les services pour persister les données

## 🔒 Sécurité

### Validation des données
- Vérification des champs obligatoires
- Validation du format email
- Sanitisation des entrées utilisateur

### Stockage sécurisé
- Chiffrement des données sensibles
- Accès contrôlé aux fichiers de cartes
- Logs d'audit pour les générations

## 📊 Monitoring

### Métriques disponibles
- Nombre de cartes générées
- Taux de succès des envois d'email
- Temps de génération moyen
- Erreurs de validation

### Logs
- Génération de cartes
- Envois d'email
- Erreurs système
- Accès aux fichiers

## 🐛 Dépannage

### Problèmes courants

#### L'image ne s'affiche pas
- Vérifier que `/public/images/membership-card-front.png` existe
- Contrôler les permissions du fichier
- Vérifier la console du navigateur pour les erreurs

#### Erreur lors de la génération
- Vérifier que le backend est démarré
- Contrôler les logs Spring Boot
- S'assurer que les dépendances sont installées

#### Email non envoyé
- Vérifier la configuration SMTP
- Contrôler les logs d'email
- Tester avec un email valide

#### Problème de responsive
- Vérifier les media queries CSS
- Tester sur différents appareils
- Contrôler la console pour les erreurs

## 🔄 Mise à jour

### Frontend
```bash
cd frontend-vue
git pull
npm install
npm run build
```

### Backend
```bash
cd backend
git pull
mvn clean install
mvn spring-boot:run
```

## 📞 Support

Pour toute question ou problème :
- Email : contact@leslumieresdukraine.fr
- Documentation : `/docs` du projet
- Issues : Repository GitHub

---

**Les Lumières d'Ukraine** - Système de gestion des adhésions  
Version 1.0 - 2024 