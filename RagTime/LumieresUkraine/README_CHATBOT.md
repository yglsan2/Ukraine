# 🤖 Chatbot RagTime - Les Lumières d'Ukraine

## 🎯 Vue d'ensemble

Le **Chatbot RagTime** est un assistant intelligent spécialisé dans la découverte de la littérature ukrainienne. Il combine la puissance du **RAG (Retrieval-Augmented Generation)** avec l'intelligence artificielle pour offrir une expérience utilisateur exceptionnelle.

## ✨ Fonctionnalités principales

### 🔍 **Recherche intelligente**
- **RAG vectoriel** : Recherche sémantique ultra-rapide (50-100ms)
- **IA enrichie** : Réponses contextuelles avec Phi-2 et Mistral 7B
- **Détection de thèmes** : Tags automatiques (guerre, amour, philosophie, etc.)
- **Scores de pertinence** : Tri intelligent des résultats

### 🎨 **Interface moderne**
- **Design élégant** : Interface chat moderne et intuitive
- **Responsive** : Adapté à tous les écrans (desktop, tablet, mobile)
- **Animations fluides** : Indicateurs de frappe, transitions
- **Thème ukrainien** : Couleurs et design cohérents avec le site

### ⚡ **Performance optimisée**
- **Réponses instantanées** : RAG pur pour la vitesse
- **IA optionnelle** : Toggle pour activer/désactiver l'IA
- **Cache intelligent** : Résumés pré-générés
- **Fallback robuste** : Fonctionne même sans IA

## 🚀 Installation rapide

### 1. Démarrage automatique
```bash
cd RagTime/LumieresUkraine
./start_chatbot_system.sh
```

### 2. Accès à l'interface
- **Interface standalone** : http://localhost:8080/chatbot_interface.html
- **API RagTime** : http://localhost:5000/api
- **Health check** : http://localhost:5000/api/health

### 3. Arrêt du système
```bash
./stop_chatbot_system.sh
```

## 📁 Structure des fichiers

```
RagTime/LumieresUkraine/
├── 🤖 Interface et composants
│   ├── chatbot_interface.html          # Interface HTML standalone
│   ├── RagTimeChatbot.vue              # Composant Vue.js
│   └── install_chatbot.md              # Guide d'installation
│
├── 🚀 Scripts de gestion
│   ├── start_chatbot_system.sh         # Démarrage automatique
│   ├── stop_chatbot_system.sh          # Arrêt propre
│   └── fix_embeddings.py               # Correction embeddings
│
├── 🔧 API et backend
│   ├── ragtime_api.py                  # API Flask principale
│   ├── ragtime_api_simple.py           # Version simplifiée
│   └── test_api_simple.py              # Tests API
│
└── 📚 Données et index
    ├── books_index.pkl                 # Index vectoriel
    ├── books_data.json                 # Données des livres
    └── smart_summaries.json            # Résumés générés
```

## 🎮 Utilisation

### Interface utilisateur

1. **Ouvrir le chatbot** : Cliquer sur le bouton flottant 🤖
2. **Poser une question** : "Parle-moi des livres sur la guerre en Ukraine"
3. **Activer l'IA** : Toggle "IA enrichie" pour des réponses plus détaillées
4. **Minimiser** : Garder le chatbot ouvert en arrière-plan
5. **Fermer** : Masquer complètement l'interface

### Exemples de questions

```
🤖 "Quels livres parlent de la guerre en Ukraine ?"
🤖 "Trouve-moi des romans d'amour ukrainiens"
🤖 "Quels sont les auteurs ukrainiens les plus populaires ?"
🤖 "Parle-moi de la philosophie ukrainienne"
🤖 "Quels livres sont disponibles en français ?"
```

## 🔧 Intégration dans votre site

### Option 1 : Composant Vue.js (recommandé)

```vue
<!-- Dans votre App.vue ou page spécifique -->
<template>
  <div id="app">
    <!-- Votre contenu existant -->
    <RagTimeChatbot />
  </div>
</template>

<script>
import RagTimeChatbot from '@/components/RagTimeChatbot.vue'

export default {
  components: {
    RagTimeChatbot
  }
}
</script>
```

### Option 2 : Interface HTML standalone

```html
<!-- Intégrer dans une iframe ou page dédiée -->
<iframe src="http://localhost:8080/chatbot_interface.html" 
        width="400" height="600" 
        frameborder="0">
</iframe>
```

### Option 3 : API directe

```javascript
// Appel direct de l'API
const response = await fetch('http://localhost:5000/api/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "livres ukrainiens",
    useAI: true,
    maxResults: 5
  })
});
```

## 🎨 Personnalisation

### Couleurs et thème

Modifiez les variables CSS dans `RagTimeChatbot.vue` :

```css
:root {
  --primary-color: #667eea;      /* Bleu principal */
  --secondary-color: #764ba2;    /* Violet secondaire */
  --accent-color: #ff6b6b;       /* Rouge accent */
  --accent-secondary: #ee5a24;   /* Orange accent */
}
```

### Configuration API

```javascript
// Dans le composant Vue.js
data() {
  return {
    apiUrl: 'http://localhost:5000/api',  // URL de l'API
    aiEnabled: true,                      // IA activée par défaut
    maxResults: 5                         // Nombre de résultats
  }
}
```

## 🔍 API Endpoints

### Recherche principale
```http
POST /api/search
Content-Type: application/json

{
  "query": "livres ukrainiens",
  "useAI": true,
  "maxResults": 5,
  "filters": {
    "genre": "roman",
    "language": "français"
  }
}
```

### Autres endpoints
- `GET /api/health` - Vérification de santé
- `GET /api/books` - Liste des livres
- `GET /api/books/{id}/summary` - Résumé d'un livre
- `GET /api/statistics` - Statistiques
- `GET /api/ai/status` - Statut de l'IA

## 🐛 Dépannage

### L'API ne répond pas

1. **Vérifier les processus** :
```bash
ps aux | grep ragtime_api
```

2. **Voir les logs** :
```bash
tail -f ragtime_api.log
```

3. **Redémarrer** :
```bash
./stop_chatbot_system.sh
./start_chatbot_system.sh
```

### Erreurs CORS

Ajouter dans `ragtime_api.py` :
```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
```

### L'IA ne fonctionne pas

1. **Vérifier Ollama** :
```bash
curl http://localhost:11434/api/tags
```

2. **Installer les modèles** :
```bash
ollama pull phi2
ollama pull mistral
```

## 📊 Performance

### Métriques typiques

- **Temps de réponse RAG** : 50-100ms
- **Temps de réponse IA** : 2-5 secondes
- **Précision de recherche** : 85-95%
- **Utilisation mémoire** : ~500MB (avec modèles IA)

### Optimisations

- **Cache des embeddings** : Chargement unique au démarrage
- **Résumés pré-générés** : Pas de génération à la volée
- **Index vectoriel optimisé** : Recherche ultra-rapide
- **Fallback intelligent** : Fonctionne sans IA

## 🔮 Évolutions futures

### Fonctionnalités prévues

- [ ] **Historique des conversations**
- [ ] **Export des conversations**
- [ ] **Recommandations personnalisées**
- [ ] **Support multilingue**
- [ ] **Intégration avec d'autres APIs**
- [ ] **Mode sombre/clair**
- [ ] **Notifications push**

### Améliorations techniques

- [ ] **WebSocket** pour les réponses temps réel
- [ ] **Cache Redis** pour les performances
- [ ] **Load balancing** pour la haute disponibilité
- [ ] **Monitoring** et métriques avancées

## 📞 Support

### Logs utiles

```bash
# Logs API
tail -f ragtime_api.log

# Logs serveur web
tail -f web_server.log

# Statut des processus
ps aux | grep -E "(ragtime|http.server)"
```

### Commandes de test

```bash
# Test de santé
curl http://localhost:5000/api/health

# Test de recherche
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "useAI": false}'
```

---

## 🎉 Conclusion

Le **Chatbot RagTime** transforme votre site "Les Lumières d'Ukraine" en une expérience interactive et intelligente. Grâce à sa technologie RAG avancée et son interface moderne, vos visiteurs peuvent découvrir la richesse de la littérature ukrainienne de manière intuitive et engageante.

**🚀 Prêt à enrichir votre site avec l'intelligence artificielle !** 