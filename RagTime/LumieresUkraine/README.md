# 🌻 RagTime - Spécialiste des livres des Lumières d'Ukraine

RagTime est un système RAG (Retrieval-Augmented Generation) intelligent spécialement conçu pour la recherche et la recommandation de livres dans le cadre de l'association Les Lumières d'Ukraine. Il s'enrichit automatiquement du contenu de chaque nouveau livre ajouté au site.

## 🚀 À quoi sert RagTime ?

- **Recherche intelligente** dans la base de livres de l'association
- **Recommandations personnalisées** basées sur les préférences utilisateur
- **Mise à jour automatique** quand de nouveaux livres sont ajoutés
- **Recherche multilingue** (français, anglais, ukrainien, etc.)
- **Filtrage avancé** par genre, langue, âge, localisation
- **Performance optimisée** avec des temps de réponse < 1 seconde

## 🏗️ Architecture du projet

### Structure des fichiers

```
RagTime/LumieresUkraine/
├── RagTime.py                    # Interface CLI principale
├── init_books_rag.py             # Script d'indexation des livres
├── update_books_from_db.py       # Mise à jour depuis la base de données
├── watch_books.py                # Surveillance automatique
├── requirements.txt              # Dépendances Python
├── books_data.json               # Données des livres (généré)
├── books_index.pkl               # Index vectoriel (généré)
├── last_update.txt               # Timestamp de dernière mise à jour
└── README.md                     # Ce fichier
```

### Composants principaux

#### 1. `RagTime.py` - Interface utilisateur
**Fonction :** Interface en ligne de commande pour interroger le RAG
**Utilisation :** `python RagTime.py`
**Caractéristiques :**
- Interface interactive avec prompt `RagTime >`
- Recherche en temps réel
- Affichage des résultats avec scores
- Gestion des erreurs
- Commande `exit` pour quitter

#### 2. `init_books_rag.py` - Moteur d'indexation
**Fonction :** Crée l'index vectoriel à partir des données des livres
**Utilisation :** `python init_books_rag.py`
**Caractéristiques :**
- Charge les données depuis `books_data.json`
- Génère les embeddings avec `sentence-transformers`
- Crée l'index pickle optimisé
- Enrichit avec métadonnées (concepts, thèmes)

#### 3. `update_books_from_db.py` - Synchronisation
**Fonction :** Met à jour les livres depuis la base de données
**Utilisation :** `python update_books_from_db.py`
**Caractéristiques :**
- Se connecte à l'API backend
- Récupère les nouveaux livres
- Met à jour l'index automatiquement
- Gestion des erreurs de connexion

#### 4. `watch_books.py` - Surveillance automatique
**Fonction :** Surveille en continu les nouveaux livres
**Utilisation :** `python watch_books.py`
**Caractéristiques :**
- Vérification périodique (5 min par défaut)
- Mise à jour automatique
- Service systemd et cron
- Logs détaillés

## 🧠 Comment fonctionne RagTime ?

### Pipeline RAG pour les livres

```
Question utilisateur
    ↓
Extraction de concepts (genre, langue, âge, etc.)
    ↓
Recherche vectorielle dans books_index.pkl
    ↓
Scoring hybride (sémantique + concepts + disponibilité)
    ↓
Sélection des livres les plus pertinents
    ↓
Affichage des résultats avec informations complètes
```

### Processus détaillé

#### 1. **Extraction de concepts** (`extract_book_concepts`)
- Détecte les concepts liés aux livres (genre, langue, âge, etc.)
- Utilise un dictionnaire de synonymes spécialisé
- Extrait les verbes d'action (emprunter, chercher, recommander)

#### 2. **Recherche vectorielle** (`search_books`)
- Charge l'index pickle (ultra-rapide)
- Génère l'embedding de la question
- Calcule la similarité cosinus avec tous les livres
- Applique un scoring hybride

#### 3. **Scoring hybride** (combinaison de scores)
- **Score sémantique** (50%) : Similarité vectorielle
- **Score conceptuel** (20%) : Correspondance des concepts
- **Score titre/auteur** (20%) : Mots-clés dans le titre ou l'auteur
- **Score disponibilité** (10%) : Livres disponibles prioritaires

#### 4. **Sélection et affichage**
- Trie les résultats par score décroissant
- Affiche les 5 meilleurs livres
- Montre toutes les informations pertinentes

## 🔧 Technologies utilisées

### Dépendances principales
- **sentence-transformers** : Modèle `all-MiniLM-L6-v2` pour les embeddings
- **numpy** : Calculs vectoriels et algèbre linéaire
- **requests** : Requêtes HTTP vers l'API backend
- **pickle** : Sérialisation optimisée de l'index

### Modèle d'embedding
- **all-MiniLM-L6-v2** : Modèle léger (384 dimensions)
- **Avantages :** Rapide, précis, multilingue
- **Taille :** ~90MB

## 🚀 Installation et utilisation

### Prérequis
```bash
# Python 3.8+
python --version

# Environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Initialisation
```bash
# Créer l'index initial avec des données d'exemple
python init_books_rag.py

# Ou mettre à jour depuis la base de données
python update_books_from_db.py
```

### Utilisation
```bash
# Interface interactive
python RagTime.py

# Mise à jour manuelle
python update_books_from_db.py

# Surveillance automatique
python watch_books.py
```

## 📚 Exemples d'utilisation

### Recherches simples
```
RagTime > romans en français
RagTime > livres pour enfants
RagTime > science-fiction disponible
RagTime > livres à Nancy
```

### Recherches avancées
```
RagTime > romans policiers en anglais pour adultes
RagTime > poésie ukrainienne
RagTime > livres de fantasy en excellent état
RagTime > biographies disponibles à Strasbourg
```

### Recommandations
```
RagTime > recommander des livres comme Harry Potter
RagTime > suggérer des romans pour adolescents
RagTime > livres populaires empruntés plus de 10 fois
```

## 🔄 Mise à jour automatique

### Mode surveillance continue
```bash
# Démarrer la surveillance (vérification toutes les 5 minutes)
python watch_books.py

# Avec intervalle personnalisé (2 minutes)
python watch_books.py --interval 120
```

### Service systemd
```bash
# Créer le service
python watch_books.py --create-service

# Installer le service (remplacer YOUR_USERNAME)
sudo cp ragtime-watcher.service /etc/systemd/system/
sudo systemctl enable ragtime-watcher
sudo systemctl start ragtime-watcher
```

### Tâche cron
```bash
# Créer la tâche cron
python watch_books.py --create-cron

# Installer la tâche (remplacer YOUR_USERNAME)
crontab ragtime-cron.txt
```

## 📊 Données des livres

### Structure d'un livre
```json
{
  "id": 1,
  "title": "Le Petit Prince",
  "author": "Antoine de Saint-Exupéry",
  "isbn": "9782070612758",
  "publication_year": 1943,
  "genre": "ROMAN",
  "target_age": "ENFANT",
  "language": "FRENCH",
  "condition": "EXCELLENT",
  "description": "Un conte poétique et philosophique...",
  "city": "Nancy",
  "postal_code": "54000",
  "latitude": 48.6921,
  "longitude": 6.1844,
  "status": "AVAILABLE",
  "total_borrows": 15,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-20T14:45:00"
}
```

### Genres supportés
- **ROMAN** : Romans de fiction
- **POESIE** : Poésie et poèmes
- **HISTOIRE** : Livres historiques
- **CULTURE** : Culture et société
- **JEUNESSE** : Livres pour enfants
- **SCIENCE_FICTION** : Science-fiction
- **FANTASY** : Fantasy et fantastique
- **POLICIER** : Romans policiers
- **BIOGRAPHIE** : Biographies et mémoires
- **ESSAI** : Essais et documentaires
- **THEATRE** : Pièces de théâtre
- **AUTRE** : Autres genres

### Langues supportées
- **FRENCH** : Français
- **ENGLISH** : Anglais
- **GERMAN** : Allemand
- **POLISH** : Polonais
- **UKRAINIAN** : Ukrainien
- **RUSSIAN** : Russe
- **SPANISH** : Espagnol
- **ITALIAN** : Italien

## 🛠️ Configuration avancée

### Variables d'environnement
```bash
# URL de l'API backend
export RAGTIME_API_URL=http://localhost:8080/api

# Intervalle de surveillance (secondes)
export RAGTIME_WATCH_INTERVAL=300

# Modèle d'embedding
export RAGTIME_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### Personnalisation des concepts
Modifiez les dictionnaires dans `RagTime.py` :
- `BOOK_CONCEPTS` : Concepts et synonymes
- `BOOK_ACTIONS` : Verbes d'action

### Logs et débogage
```bash
# Activer les logs détaillés
export RAGTIME_DEBUG=1

# Logs dans un fichier
python RagTime.py > ragtime.log 2>&1
```

## 🔍 Dépannage

### Problèmes courants

#### Index non trouvé
```
❌ Index des livres non trouvé. Lancez d'abord: python init_books_rag.py
```
**Solution :** Exécuter `python init_books_rag.py`

#### API backend inaccessible
```
❌ L'API backend n'est pas accessible
```
**Solution :** Démarrer le backend avec `./mvnw spring-boot:run`

#### Erreur d'embedding
```
⚠️ Erreur embedding pour le livre...
```
**Solution :** Vérifier la connexion internet pour télécharger le modèle

#### Mémoire insuffisante
```
❌ Erreur: Out of memory
```
**Solution :** Réduire le nombre de livres ou augmenter la RAM

### Logs et diagnostics
```bash
# Vérifier l'état de l'index
python -c "import pickle; data=pickle.load(open('books_index.pkl','rb')); print(f'{len(data)} livres indexés')"

# Vérifier la connectivité API
curl http://localhost:8080/api/health

# Vérifier les dépendances
pip list | grep -E "(sentence-transformers|numpy|requests)"
```

## 🤝 Contribution

### Ajout de nouveaux concepts
1. Modifiez `BOOK_CONCEPTS` dans `RagTime.py`
2. Ajoutez les nouveaux synonymes
3. Testez avec `python RagTime.py`

### Amélioration du scoring
1. Modifiez la fonction `search_books` dans `RagTime.py`
2. Ajustez les poids des scores
3. Testez avec différentes requêtes

### Nouveaux endpoints API
1. Modifiez `update_books_from_db.py`
2. Ajoutez les nouveaux endpoints
3. Testez la synchronisation

## 📄 Licence

Ce projet fait partie de l'association Les Lumières d'Ukraine.
Développé pour faciliter l'accès à la culture et à la littérature.

## 🌻 Support

Pour toute question ou problème :
- Consultez ce README
- Vérifiez les logs d'erreur
- Contactez l'équipe technique

---

**RagTime** - Spécialiste des livres des Lumières d'Ukraine 🌻
*Rendre la littérature accessible à tous*
