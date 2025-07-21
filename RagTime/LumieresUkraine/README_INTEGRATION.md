# 🔗 **Intégration RagTime - Java**

## 📋 **Vue d'ensemble**

Cette intégration permet d'utiliser RagTime (Python) depuis votre backend Java via une API REST. Le système offre :

- **Recherche RAG pure** : Rapide et efficace
- **IA optionnelle** : Phi-2 2.7B (rapide) et Mistral 7B (qualité)
- **Résumés intelligents** : Avec ou sans IA
- **API REST complète** : Intégration facile avec Spring Boot

## 🏗️ **Architecture**

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   Frontend Vue  │ ──────────────► │  Backend Java   │
│                 │                 │  (Spring Boot)  │
└─────────────────┘                 └─────────────────┘
                                              │
                                              │ HTTP/REST
                                              ▼
                                    ┌─────────────────┐
                                    │  API RagTime    │
                                    │    (Python)     │
                                    │   (Flask)       │
                                    └─────────────────┘
                                              │
                                              │ Ollama
                                              ▼
                                    ┌─────────────────┐
                                    │   Modèles IA    │
                                    │  Phi-2 / Mistral│
                                    └─────────────────┘
```

## 🚀 **Installation et démarrage**

### 1. **Prérequis**

```bash
# Python 3.8+
python3 --version

# Modules Python
pip3 install flask flask-cors sentence-transformers scikit-learn numpy requests

# Ollama (optionnel - pour l'IA)
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. **Démarrage de l'API RagTime**

```bash
cd RagTime/LumieresUkraine
chmod +x start_ragtime_api.sh
./start_ragtime_api.sh 5000
```

L'API sera disponible sur `http://localhost:5000`

### 3. **Intégration dans le backend Java**

Copiez les fichiers Java dans votre projet :

```bash
# Client RagTime
cp RagTimeClient.java backend/src/main/java/com/ukraine/ragtime/

# Contrôleur Spring Boot
cp RagTimeController.java backend/src/main/java/com/ukraine/controller/
```

## 📡 **Endpoints disponibles**

### **Recherche**

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/api/ragtime/search` | Recherche avec IA optionnelle |
| `POST` | `/api/ragtime/search/simple` | Recherche RAG pure |
| `POST` | `/api/ragtime/search/fast` | Recherche avec IA rapide (Phi-2) |
| `POST` | `/api/ragtime/search/quality` | Recherche avec IA qualité (Mistral) |
| `GET` | `/api/ragtime/search/theme/{theme}` | Recherche par thème |
| `GET` | `/api/ragtime/search/genre/{genre}` | Recherche par genre |
| `GET` | `/api/ragtime/search/author/{author}` | Recherche par auteur |

### **Livres**

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/ragtime/books` | Liste des livres |
| `GET` | `/api/ragtime/books/{id}` | Détails d'un livre |
| `GET` | `/api/ragtime/books/{id}/summary` | Résumé d'un livre |

### **IA et système**

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/ragtime/ai/status` | Statut de l'IA |
| `POST` | `/api/ragtime/ai/configure` | Configuration IA |
| `GET` | `/api/ragtime/statistics` | Statistiques |
| `GET` | `/api/ragtime/health` | Vérification de santé |

## 💻 **Exemples d'utilisation**

### **Recherche simple (sans IA)**

```java
@Autowired
private RagTimeClient ragTimeClient;

// Recherche RAG pure
RagTimeSearchResponse response = ragTimeClient.searchBooks(
    "livres sur l'Ukraine", 
    null, 
    10, 
    false, 
    "user123"
);

System.out.println("Livres trouvés: " + response.getBooks().size());
System.out.println("Temps RAG: " + response.getRagTime() + "s");
```

### **Recherche avec IA**

```java
// Recherche avec IA rapide
RagTimeSearchResponse response = ragTimeClient.searchBooks(
    "livres sur l'Ukraine", 
    null, 
    10, 
    true, 
    "user123"
);

if (response.isAiUsed()) {
    System.out.println("Réponse IA: " + response.getAiResponse());
    System.out.println("Modèle utilisé: " + response.getAiModel());
}
```

### **Configuration IA**

```java
// Mode rapide (Phi-2)
ragTimeClient.configureAI("fast");

// Mode qualité (Mistral)
ragTimeClient.configureAI("quality");

// Vérifier le statut
AIStatus status = ragTimeClient.getAIStatus();
System.out.println("IA disponible: " + status.isEnabled());
System.out.println("Modèles: " + status.getAvailableModels());
```

### **Résumés de livres**

```java
// Résumé standard
String summary = ragTimeClient.getBookSummary(1, "standard");

// Résumé détaillé
String detailedSummary = ragTimeClient.getBookSummary(1, "detailed");
```

## 🔧 **Configuration**

### **Variables d'environnement**

```bash
# Port de l'API RagTime
RAGTIME_API_PORT=5000

# URL de l'API RagTime
RAGTIME_API_URL=http://localhost:5000

# URL d'Ollama
OLLAMA_URL=http://localhost:11434
```

### **Configuration Spring Boot**

```yaml
# application.yml
ragtime:
  api:
    base-url: http://localhost:5000
    timeout: 30s
  ai:
    enabled: true
    default-mode: fast
```

## 📊 **Performance**

### **Temps de réponse typiques**

| Mode | Temps RAG | Temps IA | Total |
|------|-----------|----------|-------|
| RAG pur | 50-100ms | - | 50-100ms |
| IA rapide (Phi-2) | 50-100ms | 1-3s | 1-3s |
| IA qualité (Mistral) | 50-100ms | 3-8s | 3-8s |

### **Ressources requises**

| Composant | RAM | CPU | Disque |
|-----------|-----|-----|--------|
| API RagTime | 2GB | 2 cores | 1GB |
| Phi-2 2.7B | 4GB | 4 cores | 2GB |
| Mistral 7B | 8GB | 6 cores | 4GB |

## 🛠️ **Dépannage**

### **L'API RagTime ne démarre pas**

```bash
# Vérifier les logs
tail -f ragtime_api.log

# Vérifier les dépendances
python3 -c "import flask, sentence_transformers"

# Vérifier le port
netstat -tlnp | grep 5000
```

### **L'IA ne fonctionne pas**

```bash
# Vérifier Ollama
ollama list

# Démarrer Ollama
ollama serve

# Télécharger les modèles
ollama pull phi:2.7b
ollama pull mistral:7b-instruct
```

### **Erreurs de connexion Java**

```java
// Vérifier la santé de l'API
boolean isHealthy = ragTimeClient.isHealthy();
if (!isHealthy) {
    System.err.println("API RagTime non disponible");
}
```

## 🔄 **Workflow de développement**

### **1. Développement local**

```bash
# Terminal 1: API RagTime
cd RagTime/LumieresUkraine
./start_ragtime_api.sh

# Terminal 2: Backend Java
cd backend
./mvnw spring-boot:run
```

### **2. Tests**

```bash
# Test de l'API RagTime
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "livres sur l'Ukraine", "useAI": false}'

# Test du backend Java
curl -X POST http://localhost:8080/api/ragtime/search \
  -H "Content-Type: application/json" \
  -d '{"query": "livres sur l'Ukraine", "useAI": false}'
```

### **3. Production**

```bash
# Démarrage en production
nohup ./start_ragtime_api.sh 5000 > ragtime.log 2>&1 &

# Configuration Java pour production
export RAGTIME_API_URL=http://production-server:5000
```

## 📈 **Monitoring**

### **Métriques importantes**

- Temps de réponse RAG
- Temps de réponse IA
- Taux d'utilisation de l'IA
- Erreurs de connexion
- Utilisation mémoire/CPU

### **Logs**

```bash
# Logs API RagTime
tail -f ragtime_api.log

# Logs Spring Boot
tail -f backend/logs/application.log
```

## 🎯 **Avantages de cette architecture**

1. **Séparation des responsabilités** : Python pour l'IA, Java pour le business
2. **Flexibilité** : IA optionnelle, modes rapide/qualité
3. **Performance** : RAG toujours rapide, IA en complément
4. **Évolutivité** : API REST standard
5. **Maintenance** : Modules indépendants

## 🚀 **Prochaines étapes**

1. **Intégrer dans le frontend Vue.js**
2. **Ajouter la gestion d'erreurs avancée**
3. **Implémenter le cache Redis**
4. **Ajouter l'authentification**
5. **Optimiser les prompts IA**

---

**🎉 Votre système RagTime est maintenant prêt pour l'intégration !** 