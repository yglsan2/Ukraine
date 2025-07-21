#!/usr/bin/env python3
"""
Script de démarrage optimisé pour RagTime API
Gère automatiquement l'initialisation et évite les processus multiples
"""

import os
import sys
import signal
import psutil
import time
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def find_ragtime_processes():
    """Trouve tous les processus RagTime en cours"""
    ragtime_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and any('ragtime_api.py' in cmd for cmd in proc.info['cmdline']):
                ragtime_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return ragtime_processes

def stop_ragtime_processes():
    """Arrête tous les processus RagTime"""
    processes = find_ragtime_processes()
    if processes:
        logger.info(f"Arrêt de {len(processes)} processus RagTime existants...")
        for proc in processes:
            try:
                proc.terminate()
                logger.info(f"Processus {proc.pid} arrêté")
            except psutil.NoSuchProcess:
                pass
        
        # Attendre la fermeture
        time.sleep(3)
        
        # Forcer l'arrêt si nécessaire
        for proc in processes:
            try:
                if proc.is_running():
                    proc.kill()
                    logger.info(f"Processus {proc.pid} forcé à s'arrêter")
            except psutil.NoSuchProcess:
                pass
    else:
        logger.info("Aucun processus RagTime trouvé")

def check_port_available(port=5000):
    """Vérifie si le port est disponible"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def start_ragtime_api():
    """Démarre l'API RagTime"""
    try:
        # Vérifier le port
        if not check_port_available(5000):
            logger.error("Le port 5000 est déjà utilisé")
            return False
        
        # Importer et démarrer l'API
        from ragtime_api import app
        
        logger.info("🚀 Démarrage de RagTime API optimisé...")
        logger.info("📊 Singleton activé - Évite les processus multiples")
        logger.info("💾 Cache mémoire activé - Optimise les performances")
        logger.info("🔧 NumpyEncoder activé - Gestion automatique des types numpy")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
        
    except KeyboardInterrupt:
        logger.info("Arrêt demandé par l'utilisateur")
        return True
    except Exception as e:
        logger.error(f"Erreur lors du démarrage: {e}")
        return False

def main():
    """Fonction principale"""
    logger.info("=== RagTime API - Démarrage Optimisé ===")
    
    # Arrêter les processus existants
    stop_ragtime_processes()
    
    # Démarrer l'API
    success = start_ragtime_api()
    
    if success:
        logger.info("RagTime API arrêté proprement")
    else:
        logger.error("Erreur lors de l'exécution de RagTime API")
        sys.exit(1)

if __name__ == "__main__":
    main() 