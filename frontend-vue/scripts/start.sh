#!/bin/bash

# Script de démarrage automatique pour Lumières d'Ukraine
# Ce script nettoie et lance l'application proprement

echo "🚀 Démarrage de Lumières d'Ukraine..."

# Aller dans le bon répertoire
cd "$(dirname "$0")/.."

# Nettoyer avant de démarrer
echo "🧹 Nettoyage préalable..."
./scripts/cleanup.sh

# Attendre un peu pour s'assurer que tout est propre
sleep 2

# Démarrer l'application selon le mode demandé
if [ "$1" = "preview" ]; then
    echo "📱 Démarrage en mode preview..."
    npm run preview
elif [ "$1" = "serve" ]; then
    echo "🌐 Démarrage du serveur HTTP..."
    npm run serve
elif [ "$1" = "clean" ]; then
    echo "🧽 Démarrage avec nettoyage complet..."
    npm run dev:clean
else
    echo "⚡ Démarrage en mode développement..."
    npm run dev
fi

# Nettoyer à la fermeture
trap 'echo "🛑 Arrêt de l'application..."; ./scripts/cleanup.sh; exit' INT TERM 