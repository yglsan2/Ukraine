#!/usr/bin/env python3
"""
Script de gestion complet pour RagTime API
Permet de démarrer, arrêter, redémarrer et surveiller l'API
"""

import os
import sys
import psutil
import time
import requests
import json
import argparse
from pathlib import Path

def find_ragtime_processes():
    """Trouve tous les processus RagTime"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and any('ragtime_api.py' in cmd for cmd in proc.info['cmdline']):
                processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

def check_api_health():
    """Vérifie la santé de l'API"""
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_cache_stats():
    """Récupère les statistiques du cache"""
    try:
        response = requests.get('http://localhost:5000/api/cache/stats', timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_system_status():
    """Récupère le statut complet du système"""
    try:
        response = requests.get('http://localhost:5000/api/system/status', timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def start_api():
    """Démarre l'API RagTime"""
    processes = find_ragtime_processes()
    if processes:
        print(f"⚠️  {len(processes)} processus RagTime déjà en cours")
        return False
    
    print("🚀 Démarrage de RagTime API...")
    os.system(f"cd {os.path.dirname(__file__)} && python3 ragtime_api.py &")
    
    # Attendre le démarrage
    for i in range(10):
        time.sleep(1)
        if check_api_health():
            print("✅ RagTime API démarré avec succès")
            return True
    
    print("❌ Échec du démarrage de RagTime API")
    return False

def stop_api():
    """Arrête l'API RagTime"""
    processes = find_ragtime_processes()
    if not processes:
        print("ℹ️  Aucun processus RagTime trouvé")
        return True
    
    print(f"🛑 Arrêt de {len(processes)} processus RagTime...")
    for proc in processes:
        try:
            proc.terminate()
            print(f"   Processus {proc.pid} arrêté")
        except psutil.NoSuchProcess:
            pass
    
    # Attendre la fermeture
    time.sleep(3)
    
    # Forcer l'arrêt si nécessaire
    for proc in processes:
        try:
            if proc.is_running():
                proc.kill()
                print(f"   Processus {proc.pid} forcé à s'arrêter")
        except psutil.NoSuchProcess:
            pass
    
    print("✅ RagTime API arrêté")
    return True

def restart_api():
    """Redémarre l'API RagTime"""
    print("🔄 Redémarrage de RagTime API...")
    stop_api()
    time.sleep(2)
    return start_api()

def status_api():
    """Affiche le statut de l'API"""
    processes = find_ragtime_processes()
    health = check_api_health()
    
    print("=== Statut RagTime API ===")
    print(f"Processus: {len(processes)} en cours")
    
    if health:
        print(f"API: ✅ En ligne")
        print(f"Service: {health.get('service', 'N/A')}")
        print(f"Timestamp: {health.get('timestamp', 'N/A')}")
        
        # Statistiques du cache
        cache_stats = get_cache_stats()
        if cache_stats:
            print(f"\n=== Cache ===")
            print(f"Taille: {cache_stats.get('size', 0)}/{cache_stats.get('max_size', 0)}")
            print(f"TTL: {cache_stats.get('ttl_hours', 0)}h")
        
        # Statut système
        system_status = get_system_status()
        if system_status:
            print(f"\n=== Système ===")
            print(f"Livres: {system_status.get('books_count', 0)}")
            print(f"Embeddings: {'✅' if system_status.get('embeddings_loaded') else '❌'}")
            print(f"IA: {'✅' if system_status.get('ai_status', {}).get('enabled') else '❌'}")
    else:
        print("API: ❌ Hors ligne")

def test_api():
    """Teste l'API avec une recherche"""
    if not check_api_health():
        print("❌ API non disponible")
        return False
    
    print("🧪 Test de recherche...")
    try:
        response = requests.post(
            'http://localhost:5000/api/search',
            json={'query': 'test', 'useAI': False},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Test réussi")
            print(f"Résultats: {len(result.get('books', []))} livres trouvés")
            return True
        else:
            print(f"❌ Test échoué: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de test: {e}")
        return False

def clear_cache():
    """Vide le cache"""
    try:
        response = requests.post('http://localhost:5000/api/cache/clear', timeout=5)
        if response.status_code == 200:
            print("✅ Cache vidé")
            return True
        else:
            print("❌ Échec du vidage du cache")
            return False
    except:
        print("❌ Impossible de vider le cache")
        return False

def main():
    parser = argparse.ArgumentParser(description='Gestionnaire RagTime API')
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'status', 'test', 'clear-cache'],
                       help='Action à effectuer')
    
    args = parser.parse_args()
    
    if args.action == 'start':
        start_api()
    elif args.action == 'stop':
        stop_api()
    elif args.action == 'restart':
        restart_api()
    elif args.action == 'status':
        status_api()
    elif args.action == 'test':
        test_api()
    elif args.action == 'clear-cache':
        clear_cache()

if __name__ == "__main__":
    main() 