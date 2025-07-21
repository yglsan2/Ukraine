# 📘 Cahier des Charges - Lumières d'Ukraine
## Application de Partage de Livres Communautaire

---

## 📋 Informations Générales

**Nom du projet :** Lumières d'Ukraine  
**Version :** 1.0  
**Date :** 20 Juillet 2025  
**Créateur :** Yglsan  
**Type :** Application Web Progressive (PWA)  

---

## 🎯 Objectif du Projet

Créer une plateforme communautaire de partage de livres entre particuliers, spécialement conçue pour les communautés ukrainiennes en France, permettant l'emprunt gratuit de livres avec gestion des adhésions, des événements culturels et des statistiques communautaires.

---

## 👥 Public Cible

### Utilisateurs Principaux
- **Communautés ukrainiennes** en France (Nancy et alentours)
- **Lecteurs passionnés** souhaitant partager leur bibliothèque
- **Membres d'associations** culturelles et littéraires
- **Familles** avec enfants (lecture jeunesse)

### Profils Utilisateurs
1. **Propriétaire de livres** : Partage ses ouvrages
2. **Emprunteur** : Emprunte des livres
3. **Administrateur** : Gère la plateforme
4. **Utilisateur hybride** : Propriétaire et emprunteur

---

## 🏗️ Architecture Technique

### Stack Technologique
- **Frontend :** Vue.js 3 + Tailwind CSS + Vite
- **Backend :** Spring Boot 3 + Java 21
- **Base de données :** PostgreSQL
- **Authentification :** JWT
- **Internationalisation :** 5 langues (FR, EN, UK, DE, PL)

---

## 📚 Fonctionnalités Principales

### 1. Gestion des Livres

#### 1.1 Ajout d'un Livre
**Acteur :** Propriétaire  
**Prérequis :** Compte valide + adhésion active

**Champs obligatoires :**
- Titre du livre
- Auteur
- Année de publication
- ISBN (avec recherche automatique)
- État du livre (Neuf, Bon, Moyen, Usé)
- Genre littéraire
- Âge cible
- **3 photos obligatoires :**
  - Couverture (devant)
  - 4ème de couverture (derrière)
  - Intérieur (page centrale)

#### 1.2 Visualisation des Livres
**Affichage en fiches avec :**
- ✅ **Disponible** : Bouton vert
- ❌ **Indisponible** : Date de disponibilité en rouge (format FR: dd/mm/yyyy)
- Nombre d'emprunts
- Informations de contact (après réservation)

#### 1.3 Gestion de la Disponibilité
- **Durée d'emprunt :** 30 jours
- **Réservation non récupérée :** Annulation automatique après 7 jours
- **Notification automatique** quand un livre redevient disponible
- **Mise à jour automatique** de la date (+30 jours) lors d'une réservation

### 2. Système de Réservation

#### 2.1 Processus de Réservation
1. **Sélection** : Ajout au panier
2. **Commande** : Affichage des coordonnées du propriétaire
3. **Contact** : Message automatique généré
4. **Récupération** : Bouton "Livre reçu"
5. **Transfert** : Le livre passe sur le compte de l'emprunteur

#### 2.2 Contraintes de Réservation
- **Compte valide** obligatoire
- **Adhésion active** obligatoire
- **Notification claire** si non-adhérent
- **Lien vers formulaire d'adhésion** si nécessaire

### 3. Recherche et Filtres

#### 3.1 Filtres Disponibles
- **Géolocalisation** : Ville et alentours
- **Langue** : FR, EN, UK, DE, PL
- **Genre** : Roman, Poésie, Essai, Jeunesse, etc.
- **État** : Neuf, Bon, Moyen, Usé
- **Âge cible** : Enfant, Adolescent, Adulte
- **Disponibilité** : Oui/Non + Date

#### 3.2 Tri et Classement
- Par nombre d'emprunts
- Par date d'ajout
- Par proximité géographique
- Par popularité

### 4. Gestion des Événements

#### 4.1 Création d'Événements
**Acteurs :** Propriétaire, Utilisateur ayant lu le livre, Administrateur

**Types d'événements :**
- Réunion de lecture
- Discussion autour d'un livre
- Événement culturel
- Cérémonie de remise de prix

#### 4.2 Fonctionnalités Événements
- **Bouton "Créer un événement"** sur chaque fiche livre
- **Notification automatique** à tous les lecteurs précédents
- **Filtrage par :**
  - Proximité géographique
  - Livre concerné
  - Date à venir
- **Gestion des participants**

### 5. Tableaux de Bord

#### 5.1 Tableau de Bord Propriétaire
- **Liste de ses livres** avec statistiques
- **Historique d'emprunt** par livre
- **CRUD complet** : Modifier, Supprimer, Voir détails, Ajouter
- **Statistiques :**
  - Nombre d'emprunts par livre
  - Tri par nombre ou par date
  - Détails des emprunteurs

#### 5.2 Tableau de Bord Administrateur
- **Gestion globale** de tous les livres
- **Vue par ville** avec statistiques
- **Classements :**
  - Meilleur lecteur du mois (par ville)
  - Meilleur enfant lecteur
  - Meilleur donateur
- **Suppression/retrait** de livres du réseau
- **Statistiques en temps réel**

### 6. Gestion des Comptes et Adhésions

#### 6.1 Création de Compte
- **Formulaire d'inscription** standard
- **Demande d'adhésion** intégrée
- **Lien vers formulaire** principal de l'association
- **Carte d'adhésion numérique** générée

#### 6.2 Contrôles d'Adhésion
- **Vérification automatique** du statut d'adhésion
- **Notification claire** si non-adhérent
- **Renouvellement d'adhésion** guidé
- **Conditions d'adhésion** explicites

---

## 🔐 Sécurité et Conformité

### Protection des Données
- **Conformité RGPD** complète
- **Données utilisateurs** protégées
- **Email et téléphone** visibles uniquement après réservation
- **Suppression sécurisée** des données

### Gestion des Accès
- **Authentification JWT** sécurisée
- **Rôles et permissions** bien définis
- **Validation des données** côté serveur
- **Protection contre les injections**

---

## 📱 Interface Utilisateur

### Design Responsive
- **Mobile-first** design
- **Adaptation** à tous les écrans
- **Accessibilité** WCAG 2.1
- **Couleurs ukrainiennes** : Bleu (#0057b8) et Jaune (#ffdd00)

### Expérience Utilisateur
- **Navigation intuitive**
- **Feedback visuel** immédiat
- **Animations fluides**
- **Micro-interactions** engageantes

---

## 📊 Métriques et Statistiques

### Statistiques Utilisateur
- Nombre de livres empruntés
- Historique de lecture
- Participation aux événements
- Durée moyenne d'emprunt

### Statistiques Communautaires
- Livres les plus populaires
- Lecteurs les plus actifs
- Donateurs les plus généreux
- Événements les plus fréquentés

### Statistiques Administratives
- Taux d'adhésion
- Taux de retour des livres
- Répartition géographique
- Croissance de la communauté

---

## 🚀 Roadmap de Développement

### Phase 1 - MVP (Version Actuelle)
- ✅ Gestion des livres et réservations
- ✅ Système d'authentification
- ✅ Interface multilingue
- ✅ Tableaux de bord de base

### Phase 2 - Fonctionnalités Avancées
- [ ] Système de recommandations IA
- [ ] Mode hors ligne PWA
- [ ] Notifications push
- [ ] Système de messagerie interne

### Phase 3 - Optimisations
- [ ] Cache Redis pour les performances
- [ ] CDN pour les images
- [ ] Tests automatisés complets
- [ ] CI/CD pipeline

### Phase 4 - Extensions
- [ ] Application mobile native
- [ ] API publique
- [ ] Intégration réseaux sociaux
- [ ] Système de badges et récompenses

---

## 📋 Critères d'Acceptation

### Fonctionnels
- [ ] Un utilisateur peut ajouter un livre avec 3 photos
- [ ] Un utilisateur peut réserver un livre s'il est adhérent
- [ ] Un propriétaire peut voir les statistiques de ses livres
- [ ] Un administrateur peut gérer tous les livres
- [ ] Les événements peuvent être créés et gérés
- [ ] La disponibilité est gérée automatiquement

### Techniques
- [ ] L'application fonctionne sur tous les navigateurs modernes
- [ ] Les performances sont optimales (< 3s de chargement)
- [ ] La sécurité est conforme aux standards
- [ ] L'accessibilité respecte WCAG 2.1
- [ ] L'internationalisation fonctionne parfaitement

### Qualité
- [ ] Code documenté et maintenable
- [ ] Tests unitaires et d'intégration
- [ ] Documentation utilisateur complète
- [ ] Formation des administrateurs

---

## 📞 Contact et Support

**Créateur :** Yglsan  
**Email :** contact@lumières-ukraine.com  
**Site web :** lumières-ukraine.com  
**GitHub :** https://github.com/yglsan2/Ukraine  

---

*Document créé le 20 Juillet 2025 - Version 1.0*
