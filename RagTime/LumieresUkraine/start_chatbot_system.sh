#!/bin/bash

# 🚀 Script de démarrage du système Chatbot RagTime
# Pour "Les Lumières d'Ukraine"

echo "🤖 Démarrage du système Chatbot RagTime..."
echo "=========================================="

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages colorés
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier si on est dans le bon répertoire
if [ ! -f "ragtime_api.py" ]; then
    print_error "Ce script doit être exécuté depuis le répertoire RagTime/LumieresUkraine"
    exit 1
fi

# 1. Vérifier les dépendances Python
print_status "Vérification des dépendances Python..."

# Vérifier si Python 3 est installé
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 n'est pas installé"
    exit 1
fi

# Vérifier les packages requis
REQUIRED_PACKAGES=("flask" "sentence_transformers" "scikit-learn" "numpy" "requests")

for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! python3 -c "import $package" 2>/dev/null; then
        print_warning "Package $package manquant, installation..."
        pip3 install $package
    fi
done

print_success "Dépendances Python vérifiées"

# 2. Vérifier les fichiers nécessaires
print_status "Vérification des fichiers..."

REQUIRED_FILES=("books_index.pkl" "books_data.json" "smart_summaries.json")

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Fichier $file manquant"
        exit 1
    fi
done

print_success "Fichiers vérifiés"

# 3. Vérifier Ollama (optionnel)
print_status "Vérification d'Ollama..."

if command -v ollama &> /dev/null; then
    if curl -s http://localhost:11434/api/tags > /dev/null; then
        print_success "Ollama est en cours d'exécution"
        
        # Vérifier les modèles disponibles
        MODELS=$(curl -s http://localhost:11434/api/tags | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    models = [model['name'] for model in data.get('models', [])]
    print('Modèles disponibles:', ', '.join(models))
except:
    print('Aucun modèle trouvé')
")
        print_status "$MODELS"
    else
        print_warning "Ollama installé mais pas en cours d'exécution"
        print_status "Démarrage d'Ollama..."
        ollama serve &
        sleep 5
    fi
else
    print_warning "Ollama non installé - L'IA sera désactivée"
fi

# 4. Arrêter les processus existants
print_status "Arrêt des processus existants..."

pkill -f ragtime_api 2>/dev/null
pkill -f "python3.*http.server.*8080" 2>/dev/null

sleep 2

# 5. Démarrer l'API RagTime
print_status "Démarrage de l'API RagTime..."

python3 ragtime_api.py > ragtime_api.log 2>&1 &
RAGTIME_PID=$!

# Attendre que l'API démarre
sleep 5

# Vérifier que l'API fonctionne
if curl -s http://localhost:5000/api/health > /dev/null; then
    print_success "API RagTime démarrée (PID: $RAGTIME_PID)"
else
    print_error "Échec du démarrage de l'API RagTime"
    print_status "Vérifiez les logs: tail -f ragtime_api.log"
    exit 1
fi

# 6. Démarrer le serveur web pour l'interface
print_status "Démarrage du serveur web..."

python3 -m http.server 8080 > web_server.log 2>&1 &
WEB_PID=$!

sleep 2

if curl -s http://localhost:8080 > /dev/null; then
    print_success "Serveur web démarré (PID: $WEB_PID)"
else
    print_error "Échec du démarrage du serveur web"
    exit 1
fi

# 7. Afficher les informations de connexion
echo ""
echo "🎉 Système Chatbot RagTime démarré avec succès !"
echo "================================================"
echo ""
echo "📡 API RagTime:     http://localhost:5000"
echo "🌐 Interface web:   http://localhost:8080/chatbot_interface.html"
echo "📊 Health check:    http://localhost:5000/api/health"
echo ""
echo "🔧 Commandes utiles:"
echo "   - Voir les logs API:     tail -f ragtime_api.log"
echo "   - Voir les logs web:     tail -f web_server.log"
echo "   - Tester l'API:          curl http://localhost:5000/api/health"
echo "   - Arrêter le système:    ./stop_chatbot_system.sh"
echo ""

# 8. Test rapide de l'API
print_status "Test rapide de l'API..."

TEST_RESPONSE=$(curl -s -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "useAI": false}' 2>/dev/null)

if echo "$TEST_RESPONSE" | grep -q "success"; then
    print_success "Test API réussi"
else
    print_warning "Test API échoué - vérifiez les logs"
fi

# 9. Sauvegarder les PIDs pour l'arrêt
echo "$RAGTIME_PID" > ragtime_api.pid
echo "$WEB_PID" > web_server.pid

echo ""
print_success "Système prêt ! Ouvrez http://localhost:8080/chatbot_interface.html dans votre navigateur"
echo ""

# Attendre les signaux d'arrêt
trap 'echo ""; print_status "Arrêt du système..."; pkill -f ragtime_api; pkill -f "python3.*http.server.*8080"; rm -f *.pid; exit 0' INT TERM

# Garder le script en vie
while true; do
    sleep 10
    
    # Vérifier que les processus sont toujours en vie
    if ! kill -0 $RAGTIME_PID 2>/dev/null; then
        print_error "L'API RagTime s'est arrêtée"
        break
    fi
    
    if ! kill -0 $WEB_PID 2>/dev/null; then
        print_error "Le serveur web s'est arrêté"
        break
    fi
done 