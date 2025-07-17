# 🇺🇦 Lumières d'Ukraine – Plateforme collaborative de partage de livres

<div align="center">

![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.x-6DB33F?style=for-the-badge&logo=spring-boot&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.x-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

</div>

---

## 🌍 Présentation

**Lumières d'Ukraine** est une plateforme web collaborative ultra-moderne permettant le partage de livres entre particuliers, la gestion d'événements, et la mise en relation de passionnés de lecture. Le projet est fullstack : il combine un frontend Vue.js, un backend Java/Spring Boot, et une base de données MySQL.

---

## 🏗️ Architecture du projet

```mermaid
graph TD;
  A[Frontend Vue.js (JavaScript)] --API REST--> B[Backend Spring Boot (Java)]
  B --JPA/Hibernate--> C[(Base de données MySQL)]
```

- **Frontend** : Vue.js (JavaScript), Pinia, Tailwind CSS, Vite
- **Backend** : Java, Spring Boot, Spring Security, JPA/Hibernate
- **Base de données** : MySQL

---

## 📁 Structure des dossiers

```
Ukraine/
├── backend/           # Code Java Spring Boot (API REST, sécurité, logique métier)
├── frontend-vue/      # Application Vue.js (interface utilisateur moderne)
├── database/          # Scripts SQL, structure et données MySQL
├── docs/              # Documentation, cahier des charges, MCD
├── deploy-ovh.sh      # Script de déploiement OVH
├── setup_database.sql # Script d'initialisation de la base
├── README.md          # Ce fichier
└── ...
```

---

## ✨ Fonctionnalités principales

- Interface multilingue (français, anglais, ukrainien, allemand, polonais)
- Design moderne, animations, responsive, effets visuels Ukraine
- Authentification sécurisée (JWT)
- Gestion des utilisateurs, livres, réservations, événements
- Chatbot, newsletter, micro-interactions
- API REST performante
- Base de données relationnelle robuste

---

## 🚀 Démarrage rapide

### 1. **Backend (Spring Boot)**
```bash
cd backend
./mvnw spring-boot:run
```

### 2. **Frontend (Vue.js)**
```bash
cd frontend-vue
npm install
npm run dev
```

### 3. **Base de données (MySQL)**
- Importez le script `database/ukraines.sql` ou `setup_database.sql` dans votre MySQL local.
- Configurez l'URL de connexion dans `backend/src/main/resources/application.properties`.

---

## 🛠️ Technologies utilisées
- **Frontend** : Vue.js 3, Pinia, Tailwind CSS, Vite
- **Backend** : Java 17+, Spring Boot 3, Spring Security, JPA/Hibernate
- **Database** : MySQL 8+
- **Déploiement** : OVH, Docker (optionnel)

---

## 📚 Documentation
- [Cahier des charges](./CAHIER_DES_CHARGES.md)
- [MCD](./MCD_UKRAINES.md)
- [Guide de déploiement](./README-DEPLOIEMENT.md)

---

## 🤝 Contribution
Les contributions sont les bienvenues ! Merci de lire la documentation avant toute PR.

---

## 🏆 Auteurs
- Projet réalisé par l'association Lumières d'Ukraine et ses contributeurs.

---

## 💙💛 Gloire à l'Ukraine ! 