#!/bin/bash

# Script de nettoyage automatique pour Lumières d'Ukraine
# Ce script nettoie les processus et ports utilisés par l'application

echo "🧹 Nettoyage des processus et ports..."

# Fonction pour tuer les processus sur les ports spécifiques
kill_port_processes() {
    local ports=("5173" "4173" "8080" "3001" "3000")
    
    for port in "${ports[@]}"; do
        echo "🔍 Vérification du port $port..."
        lsof -ti:$port | xargs -r kill -9
    done
}

# Fonction pour tuer les processus par nom
kill_named_processes() {
    local processes=("vite" "http.server" "python.*http.server" "node.*vite")
    
    for process in "${processes[@]}"; do
        echo "🔍 Recherche de processus: $process"
        pkill -f "$process" || true
    done
}

# Nettoyage principal
echo "🚀 Démarrage du nettoyage..."

# Tuer les processus sur les ports spécifiques
kill_port_processes

# Tuer les processus par nom
kill_named_processes

# Nettoyer les fichiers temporaires
echo "🗑️  Nettoyage des fichiers temporaires..."
rm -rf dist/.vite 2>/dev/null || true
rm -rf node_modules/.vite 2>/dev/null || true

# Vérifier que les ports sont libres
echo "✅ Vérification des ports..."
sleep 2
lsof -i :5173 -i :4173 -i :8080 -i :3001 2>/dev/null || echo "✅ Tous les ports sont libres"

echo "🎉 Nettoyage terminé !"
echo "💡 Utilisez 'npm run dev:clean' pour un nettoyage complet"
echo "💡 Utilisez 'npm run dev' pour un démarrage rapide" 