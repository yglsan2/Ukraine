# 🌟 Lumières d'Ukraine

> **Partagez la culture ukrainienne à travers les livres**

[![Vue.js](https://img.shields.io/badge/Vue.js-3.4.21-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4.1-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.x-6DB33F?style=for-the-badge&logo=spring-boot&logoColor=white)](https://spring.io/projects/spring-boot)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

## 🎯 À propos du projet

**Lumières d'Ukraine** est une plateforme moderne dédiée au partage et à la découverte de la culture ukrainienne à travers la littérature. Notre mission est de créer un pont culturel entre l'Ukraine et le monde entier.

### ✨ Fonctionnalités principales

- 📚 **Bibliothèque Virtuelle** - Collection unique de livres ukrainiens
- 🌍 **Interface Multilingue** - 5 langues : Français, Anglais, Ukrainien, Allemand, Polonais
- 🎉 **Événements Culturels** - Rencontres littéraires et événements culturels
- 🤖 **Assistant IA** - Chatbot intelligent pour guider vos découvertes
- 🔒 **Sécurité Avancée** - Authentification JWT et protection des données
- 💙💛 **Communauté** - Rejoignez une communauté passionnée

## 🚀 Technologies utilisées

### Frontend
- **Vue.js 3** - Framework JavaScript progressif
- **Tailwind CSS** - Framework CSS utilitaire
- **Vite** - Outil de build ultra-rapide
- **Vue Router** - Routage côté client
- **Pinia** - Gestion d'état

### Backend
- **Spring Boot 3** - Framework Java
- **Spring Security** - Sécurité et authentification
- **Spring Data JPA** - Persistance des données
- **PostgreSQL** - Base de données

## 📦 Installation

### Prérequis
- Node.js 18+ 
- Java 17+
- PostgreSQL 14+

### Frontend
```bash
# Cloner le repository
git clone https://github.com/yglsan2/Ukraine.git
cd Ukraine/frontend-vue

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

### Backend
```bash
# Aller dans le dossier backend
cd backend

# Compiler avec Maven
./mvnw clean install

# Lancer l'application
./mvnw spring-boot:run
```

## 🎨 Design & UX

Notre interface utilisateur combine modernité et élégance :

- **Design Responsive** - Adapté à tous les écrans
- **Animations Naturelles** - Livres flottants et effets visuels
- **Couleurs Ukraine** - Bleu et jaune du drapeau ukrainien
- **Glassmorphism** - Effets de transparence et flou
- **Micro-interactions** - Feedback visuel intuitif

## 🌐 Déploiement

### Frontend (Vercel/Netlify)
```bash
# Build de production
npm run build

# Déployer le dossier dist/
```

### Backend (Heroku/Railway)
```bash
# Configuration des variables d'environnement
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret-key

# Déploiement automatique via Git
```

## 📁 Structure du projet

```
Ukraine/
├── frontend-vue/          # Application Vue.js
│   ├── src/
│   │   ├── components/    # Composants réutilisables
│   │   ├── views/         # Pages de l'application
│   │   ├── router/        # Configuration des routes
│   │   └── stores/        # Gestion d'état Pinia
│   ├── public/            # Assets statiques
│   └── package.json       # Dépendances frontend
├── backend/               # API Spring Boot
│   ├── src/main/java/     # Code source Java
│   ├── src/main/resources/# Configuration
│   └── pom.xml           # Dépendances backend
└── docs/                 # Documentation
```

## 🤝 Contribution

Nous accueillons toutes les contributions ! Voici comment participer :

1. **Fork** le projet
2. **Créer** une branche feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrir** une Pull Request

### Branches
- `main` - Code de production stable
- `develop` - Développement en cours
- `feature/*` - Nouvelles fonctionnalités
- `hotfix/*` - Corrections urgentes

## 📝 Roadmap

- [ ] **Système de recommandations** - IA pour suggérer des livres
- [ ] **Mode hors ligne** - PWA avec cache intelligent
- [ ] **Audio books** - Livres audio en ukrainien
- [ ] **Réseau social** - Partage de critiques et discussions
- [ ] **API publique** - Documentation et accès tiers
- [ ] **Mobile app** - Applications iOS et Android

## 🏆 Statistiques

- 📚 **500+** Livres partagés
- 👥 **200+** Membres actifs
- 🎉 **50+** Événements culturels
- 🌍 **5** Langues supportées

## 📞 Contact

- **Site web** : [lumières-ukraine.com](https://lumières-ukraine.com)
- **Email** : contact@lumières-ukraine.com
- **Discord** : [Rejoindre notre communauté](https://discord.gg/lumieres-ukraine)

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<div align="center">

**💙💛 Fait avec amour pour la culture ukrainienne 💙💛**

*Soutenez l'Ukraine - Partagez la culture*

</div> 