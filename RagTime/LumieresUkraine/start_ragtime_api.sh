#!/bin/bash

# Script de démarrage pour l'API RagTime
# Usage: ./start_ragtime_api.sh [port]

set -e

# Configuration
DEFAULT_PORT=5000
PORT=${1:-$DEFAULT_PORT}
API_FILE="ragtime_api.py"
LOG_FILE="ragtime_api.log"

echo "🚀 Démarrage de l'API RagTime..."
echo "📁 Répertoire: $(pwd)"
echo "🔌 Port: $PORT"
echo "📝 Log: $LOG_FILE"

# Vérification des dépendances
echo "🔍 Vérification des dépendances..."

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

# Vérifier les modules Python
echo "📦 Vérification des modules Python..."
python3 -c "import flask, sentence_transformers, sklearn, numpy" 2>/dev/null || {
    echo "❌ Modules Python manquants. Installation..."
    pip3 install flask flask-cors sentence-transformers scikit-learn numpy requests
}

# Vérifier Ollama (optionnel)
if command -v ollama &> /dev/null; then
    echo "✅ Ollama détecté"
    # Vérifier si Ollama est en cours d'exécution
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama en cours d'exécution"
    else
        echo "⚠️ Ollama installé mais pas en cours d'exécution"
        echo "   Pour démarrer Ollama: ollama serve"
    fi
else
    echo "⚠️ Ollama non installé - Mode RAG pur uniquement"
fi

# Vérifier les fichiers nécessaires
echo "📂 Vérification des fichiers..."
if [ ! -f "$API_FILE" ]; then
    echo "❌ Fichier $API_FILE non trouvé"
    exit 1
fi

if [ ! -f "books_data.json" ]; then
    echo "⚠️ Fichier books_data.json non trouvé - Création d'un exemple..."
    cat > books_data.json << EOF
[
  {
    "id": 0,
    "title": "Exemple de livre",
    "author": "Auteur exemple",
    "genre": "Roman",
    "description": "Description d'exemple",
    "language": "Français",
    "city": "Paris",
    "status": "Disponible"
  }
]
EOF
fi

# Créer l'index si nécessaire
if [ ! -f "books_index.pkl" ]; then
    echo "🔍 Création de l'index vectoriel..."
    python3 -c "
import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Charger les données
with open('books_data.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

# Modèle d'embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

# Créer les embeddings
texts = [f\"{book['title']} {book['description']} {book['genre']}\" for book in books]
embeddings = model.encode(texts)

# Concepts simples (mots-clés)
concepts = []
for book in books:
    book_concepts = []
    text = f\"{book['title']} {book['description']} {book['genre']}\".lower()
    keywords = ['livre', 'roman', 'histoire', 'aventure', 'amour', 'guerre', 'famille']
    for keyword in keywords:
        if keyword in text:
            book_concepts.append(keyword)
    concepts.append(book_concepts)

# Sauvegarder l'index
index_data = {
    'embeddings': embeddings,
    'concepts': concepts
}

with open('books_index.pkl', 'wb') as f:
    pickle.dump(index_data, f)

print(f'✅ Index créé pour {len(books)} livres')
"
fi

# Créer les résumés si nécessaire
if [ ! -f "smart_summaries.json" ]; then
    echo "📝 Création des résumés intelligents..."
    python3 -c "
import json

# Créer des résumés d'exemple
summaries = {
    'summaries': {
        0: {
            'style': 'standard',
            'summary': 'Un livre d\'exemple pour tester le système RagTime.'
        }
    }
}

with open('smart_summaries.json', 'w', encoding='utf-8') as f:
    json.dump(summaries, f, ensure_ascii=False, indent=2)

print('✅ Résumés créés')
"
fi

# Démarrage de l'API
echo "🚀 Démarrage de l'API RagTime sur le port $PORT..."

# Variables d'environnement
export FLASK_ENV=production
export FLASK_DEBUG=false
export PORT=$PORT

# Démarrer l'API
python3 "$API_FILE" > "$LOG_FILE" 2>&1 &
API_PID=$!

echo "✅ API RagTime démarrée (PID: $API_PID)"
echo "📊 Logs: tail -f $LOG_FILE"
echo "🔗 URL: http://localhost:$PORT"
echo "🏥 Health check: http://localhost:$PORT/api/health"

# Attendre un peu pour vérifier que l'API démarre
sleep 3

# Vérifier que l'API répond
if curl -s http://localhost:$PORT/api/health > /dev/null 2>&1; then
    echo "✅ API RagTime opérationnelle"
    echo ""
    echo "📋 Endpoints disponibles:"
    echo "  GET  /api/health                    - Vérification de santé"
    echo "  POST /api/search                    - Recherche de livres"
    echo "  GET  /api/books                     - Liste des livres"
    echo "  GET  /api/books/{id}                - Détails d'un livre"
    echo "  GET  /api/books/{id}/summary        - Résumé d'un livre"
    echo "  POST /api/recommendations           - Recommandations"
    echo "  GET  /api/statistics                - Statistiques"
    echo "  GET  /api/ai/status                 - Statut IA"
    echo "  POST /api/ai/configure              - Configuration IA"
    echo ""
    echo "🛑 Pour arrêter: kill $API_PID"
else
    echo "❌ Erreur: L'API ne répond pas"
    echo "📝 Vérifiez les logs: cat $LOG_FILE"
    exit 1
fi

# Garder le script en vie
echo "⏳ Appuyez sur Ctrl+C pour arrêter l'API..."
wait $API_PID 