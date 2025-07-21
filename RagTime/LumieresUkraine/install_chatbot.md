# 🤖 Installation du Chatbot RagTime

## 📋 Prérequis

- API RagTime fonctionnelle sur le port 5000
- Site web avec Vue.js 3
- Serveur web (Apache, Nginx, ou serveur de développement)

## 🚀 Installation Rapide

### 1. Copier les fichiers

```bash
# Copier le composant Vue.js
cp RagTimeChatbot.vue /chemin/vers/votre/projet/src/components/

# Copier l'interface HTML standalone (optionnel)
cp chatbot_interface.html /chemin/vers/votre/projet/public/
```

### 2. Intégrer dans votre application Vue.js

#### Dans votre fichier principal (main.js ou App.vue) :

```javascript
import RagTimeChatbot from './components/RagTimeChatbot.vue'

// Dans votre composant principal
export default {
  components: {
    RagTimeChatbot
  }
}
```

#### Dans votre template :

```vue
<template>
  <div id="app">
    <!-- Votre contenu existant -->
    
    <!-- Chatbot RagTime -->
    <RagTimeChatbot />
  </div>
</template>
```

### 3. Intégration dans une page spécifique

Si vous voulez l'intégrer uniquement dans la page "Chatbot" :

```vue
<!-- Dans ChatbotView.vue -->
<template>
  <div class="chatbot-page">
    <h1>Assistant RagTime</h1>
    <p>Découvrez notre bibliothèque ukrainienne</p>
    
    <!-- Interface complète du chatbot -->
    <RagTimeChatbot />
  </div>
</template>

<script>
import RagTimeChatbot from '@/components/RagTimeChatbot.vue'

export default {
  name: 'ChatbotView',
  components: {
    RagTimeChatbot
  }
}
</script>
```

## 🎨 Personnalisation

### Changer l'URL de l'API

Dans le composant `RagTimeChatbot.vue`, modifiez la ligne :

```javascript
apiUrl: 'http://localhost:5000/api'
```

Par exemple :
```javascript
apiUrl: 'https://votre-domaine.com/api/ragtime'
```

### Personnaliser les couleurs

Modifiez les variables CSS dans le style du composant :

```css
/* Couleurs principales */
--primary-color: #667eea;
--secondary-color: #764ba2;
--accent-color: #ff6b6b;
--accent-secondary: #ee5a24;
```

### Ajouter des fonctionnalités

Le composant est extensible. Vous pouvez ajouter :

- Historique des conversations
- Export des conversations
- Thèmes personnalisés
- Intégration avec d'autres APIs

## 🔧 Configuration avancée

### Variables d'environnement

Créez un fichier `.env` :

```env
VUE_APP_RAGTIME_API_URL=http://localhost:5000/api
VUE_APP_CHATBOT_ENABLED=true
```

### Configuration dans le composant

```javascript
data() {
  return {
    apiUrl: process.env.VUE_APP_RAGTIME_API_URL || 'http://localhost:5000/api',
    enabled: process.env.VUE_APP_CHATBOT_ENABLED === 'true'
  }
}
```

## 📱 Responsive Design

Le chatbot est entièrement responsive :

- **Desktop** : Interface flottante en bas à droite
- **Mobile** : Interface plein écran adaptée
- **Tablet** : Interface adaptative

## 🎯 Fonctionnalités

### ✅ Fonctionnalités incluses

- 🔍 **Recherche intelligente** : RAG vectoriel + IA optionnelle
- 📚 **Affichage des livres** : Titre, auteur, genre, pertinence
- ⚡ **Performance** : Réponses rapides (50-100ms)
- 🎨 **Interface moderne** : Design élégant et intuitif
- 📱 **Responsive** : Adapté à tous les écrans
- 🔄 **IA toggle** : Activation/désactivation de l'IA
- 📊 **Statut API** : Indicateur de connexion
- 💬 **Messages temps réel** : Indicateur de frappe
- 🕐 **Horodatage** : Heure des messages

### 🎮 Utilisation

1. **Cliquer** sur le bouton flottant pour ouvrir
2. **Taper** votre question sur les livres ukrainiens
3. **Activer/désactiver** l'IA avec le toggle
4. **Minimiser** pour garder le chatbot ouvert
5. **Fermer** pour masquer complètement

## 🐛 Dépannage

### L'API ne répond pas

1. Vérifiez que l'API RagTime est démarrée :
```bash
cd RagTime/LumieresUkraine
python3 ragtime_api.py
```

2. Testez l'API :
```bash
curl http://localhost:5000/api/health
```

### Erreurs CORS

Si vous avez des erreurs CORS, ajoutez dans votre API Flask :

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
```

### Le chatbot ne s'affiche pas

1. Vérifiez que le composant est bien importé
2. Vérifiez la console du navigateur pour les erreurs
3. Assurez-vous que Vue.js est correctement configuré

## 🚀 Déploiement

### Production

1. **Build** de votre application Vue.js :
```bash
npm run build
```

2. **Déployer** sur votre serveur web

3. **Configurer** l'URL de l'API pour la production

### Docker (optionnel)

```dockerfile
# Dockerfile pour l'API RagTime
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "ragtime_api.py"]
```

## 📞 Support

Pour toute question ou problème :

1. Vérifiez les logs de l'API
2. Consultez la console du navigateur
3. Testez l'API directement avec curl
4. Vérifiez la configuration réseau

---

**🎉 Votre chatbot RagTime est maintenant prêt à enrichir votre site "Les Lumières d'Ukraine" !** 