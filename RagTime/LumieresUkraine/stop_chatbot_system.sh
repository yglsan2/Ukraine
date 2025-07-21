#!/bin/bash

# 🛑 Script d'arrêt du système Chatbot RagTime

echo "🛑 Arrêt du système Chatbot RagTime..."
echo "======================================"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Arrêter l'API RagTime
print_status "Arrêt de l'API RagTime..."

if [ -f "ragtime_api.pid" ]; then
    RAGTIME_PID=$(cat ragtime_api.pid)
    if kill -0 $RAGTIME_PID 2>/dev/null; then
        kill $RAGTIME_PID
        print_success "API RagTime arrêtée (PID: $RAGTIME_PID)"
    else
        print_warning "API RagTime déjà arrêtée"
    fi
    rm -f ragtime_api.pid
else
    # Essayer de tuer par nom de processus
    pkill -f ragtime_api
    print_status "Arrêt forcé de l'API RagTime"
fi

# Arrêter le serveur web
print_status "Arrêt du serveur web..."

if [ -f "web_server.pid" ]; then
    WEB_PID=$(cat web_server.pid)
    if kill -0 $WEB_PID 2>/dev/null; then
        kill $WEB_PID
        print_success "Serveur web arrêté (PID: $WEB_PID)"
    else
        print_warning "Serveur web déjà arrêté"
    fi
    rm -f web_server.pid
else
    # Essayer de tuer par nom de processus
    pkill -f "python3.*http.server.*8080"
    print_status "Arrêt forcé du serveur web"
fi

# Nettoyer les processus restants
print_status "Nettoyage des processus restants..."

pkill -f ragtime_api 2>/dev/null
pkill -f "python3.*http.server.*8080" 2>/dev/null

# Supprimer les fichiers PID
rm -f *.pid

# Vérifier que tout est arrêté
sleep 2

if pgrep -f ragtime_api > /dev/null; then
    print_warning "Certains processus RagTime sont encore en cours d'exécution"
    pgrep -f ragtime_api | xargs ps -p
else
    print_success "Tous les processus RagTime sont arrêtés"
fi

if pgrep -f "python3.*http.server.*8080" > /dev/null; then
    print_warning "Certains processus serveur web sont encore en cours d'exécution"
    pgrep -f "python3.*http.server.*8080" | xargs ps -p
else
    print_success "Tous les processus serveur web sont arrêtés"
fi

echo ""
print_success "Système Chatbot RagTime arrêté avec succès !"
echo "" 