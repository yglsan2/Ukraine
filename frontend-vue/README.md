# 🌟 Lumières d'Ukraine - Application de Partage de Livres

Une application moderne et progressive (PWA) pour partager et découvrir la culture ukrainienne à travers le partage de livres.

## 🚀 Fonctionnalités

### ✨ Interface Moderne
- **Design responsive** : Adapté à tous les écrans (mobile, tablette, desktop)
- **Mode sombre/clair** : Basculement automatique selon les préférences
- **Animations fluides** : Transitions et micro-interactions modernes
- **Navigation intuitive** : Menu sticky et navigation mobile bottom

### 📚 Gestion des Livres
- **Catalogue complet** : Recherche et filtrage avancés
- **Favoris** : Système de wishlist personnel
- **Propositions** : Ajout facile de nouveaux livres
- **Statuts** : Suivi de disponibilité en temps réel

### 👥 Communauté
- **Profils utilisateurs** : Badges et statistiques
- **Messagerie intégrée** : Communication directe entre membres
- **Événements** : Club de lecture et ateliers
- **Notifications** : Système de notifications push

### 🔧 Technologies Avancées
- **PWA** : Installation sur mobile et desktop
- **Hors ligne** : Fonctionnement sans connexion
- **Performance** : Chargement rapide et optimisé
- **Sécurité** : Authentification et autorisation

## 🛠️ Installation

### Prérequis
- Node.js 18+ 
- npm ou yarn

### Développement
```bash
# Cloner le projet
git clone https://github.com/lumieres-ukraine/frontend-vue.git
cd frontend-vue

# Installer les dépendances
npm install

# Lancer en mode développement
npm run dev

# Lancer avec Electron (desktop)
npm run electron:dev
```

### Production
```bash
# Build pour production
npm run build

# Build pour Electron (desktop)
npm run electron:build

# Créer les installateurs
npm run electron:dist
```

## 📱 Utilisation

### Application Web
1. Ouvrez votre navigateur
2. Accédez à `http://localhost:5173`
3. L'application se charge automatiquement

### Installation PWA
1. Ouvrez l'application dans Chrome/Edge
2. Cliquez sur "Installer" dans la barre d'adresse
3. L'application apparaît dans votre menu

### Application Desktop
1. Téléchargez l'installateur pour votre OS
2. Installez l'application
3. Lancez depuis le menu ou le bureau

## 🏗️ Architecture

### Frontend (Vue.js 3)
```
src/
├── components/     # Composants réutilisables
├── views/         # Pages de l'application
├── stores/        # État global (Pinia)
├── router/        # Configuration des routes
└── assets/        # Ressources statiques
```

### PWA Configuration
```
public/
├── manifest.json  # Configuration PWA
├── sw.js         # Service Worker
└── offline.html   # Page hors ligne
```

### Electron (Desktop)
```
electron/
└── main.js       # Point d'entrée Electron
```

## 🎨 Design System

### Couleurs Ukraine
- **Bleu** : `#0057b8` (couleur nationale ukrainienne)
- **Jaune** : `#ffdd00` (couleur nationale ukrainienne)
- **Gradients** : Combinaisons harmonieuses

### Typographie
- **Titres** : Segoe UI, Tahoma, Geneva, Verdana
- **Corps** : Système de police moderne
- **Hiérarchie** : Tailles et poids cohérents

### Composants
- **Boutons** : Styles Bootstrap avec animations
- **Cartes** : Ombres et bordures arrondies
- **Modales** : Transitions fluides
- **Formulaires** : Validation en temps réel

## 🔧 Configuration

### Variables d'Environnement
```env
VITE_API_URL=http://localhost:8082
VITE_APP_NAME=Lumières d'Ukraine
VITE_APP_VERSION=1.0.0
```

### Build Configuration
```javascript
// vite.config.js
export default defineConfig({
  plugins: [vue()],
  base: '/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  }
})
```

## 📦 Scripts Disponibles

```bash
# Développement
npm run dev              # Serveur de développement
npm run electron:dev     # Electron + dev server

# Build
npm run build           # Build production
npm run preview         # Prévisualiser le build

# Tests
npm run test            # Tests unitaires
npm run test:e2e        # Tests end-to-end

# Linting
npm run lint            # ESLint
npm run format          # Prettier

# Electron
npm run electron:build  # Build desktop
npm run electron:dist   # Créer installateurs
```

## 🚀 Déploiement

### Web (PWA)
1. Build de production : `npm run build`
2. Déployer le dossier `dist/` sur votre serveur
3. Configurer HTTPS pour les fonctionnalités PWA

### Desktop (Electron)
1. Build complet : `npm run electron:dist`
2. Installateurs créés dans `dist-electron/`
3. Distribuer selon la plateforme :
   - **Windows** : `.exe` (NSIS)
   - **macOS** : `.dmg` ou `.pkg`
   - **Linux** : `.AppImage` ou `.deb`

## 🔒 Sécurité

- **HTTPS obligatoire** pour les fonctionnalités PWA
- **CSP** (Content Security Policy) configuré
- **Authentification** JWT sécurisée
- **Validation** côté client et serveur

## 📊 Performance

- **Lighthouse Score** : 95+ sur tous les critères
- **First Contentful Paint** : < 1.5s
- **Largest Contentful Paint** : < 2.5s
- **Cumulative Layout Shift** : < 0.1

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature : `git checkout -b feature/nouvelle-fonctionnalite`
3. Commit les changements : `git commit -am 'Ajout nouvelle fonctionnalité'`
4. Push la branche : `git push origin feature/nouvelle-fonctionnalite`
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- **Vue.js** pour le framework moderne
- **Bootstrap** pour le design system
- **Electron** pour l'application desktop
- **PWA** pour l'expérience mobile native

## 📞 Support

- **Email** : contact@lumieres-ukraine.fr
- **GitHub** : https://github.com/lumieres-ukraine
- **Documentation** : https://docs.lumieres-ukraine.fr

---

**Lumières d'Ukraine** - Partagez la culture, partagez l'espoir 🌟
