#!/usr/bin/env python3
"""
Script de surveillance automatique des livres
Met à jour RagTime en continu quand de nouveaux livres sont ajoutés
"""

import os
import sys
import time
import signal
import threading
from datetime import datetime, timedelta
from typing import Optional

# Importer le script de mise à jour
try:
    from update_books_from_db import main as update_books
except ImportError:
    print("❌ Erreur: update_books_from_db.py non trouvé")
    sys.exit(1)

class BookWatcher:
    """Surveillant automatique des livres"""
    
    def __init__(self, check_interval: int = 300):  # 5 minutes par défaut
        self.check_interval = check_interval
        self.running = False
        self.last_check = None
        self.update_count = 0
        
    def start(self):
        """Démarre la surveillance"""
        self.running = True
        print("🌻 Démarrage de la surveillance automatique des livres")
        print(f"⏰ Vérification toutes les {self.check_interval} secondes")
        print("🛑 Appuyez sur Ctrl+C pour arrêter")
        print("=" * 60)
        
        # Gestionnaire de signal pour arrêt propre
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            while self.running:
                self.check_for_updates()
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Arrête la surveillance"""
        self.running = False
        print("\n🛑 Arrêt de la surveillance")
        print(f"📊 Total des mises à jour: {self.update_count}")
    
    def signal_handler(self, signum, frame):
        """Gestionnaire de signal pour arrêt propre"""
        print(f"\n📡 Signal {signum} reçu")
        self.stop()
    
    def check_for_updates(self):
        """Vérifie s'il y a des mises à jour"""
        now = datetime.now()
        self.last_check = now
        
        print(f"\n🔍 Vérification à {now.strftime('%H:%M:%S')}...")
        
        try:
            # Lancer la mise à jour
            success = update_books()
            
            if success:
                self.update_count += 1
                print(f"✅ Vérification terminée (mise à jour #{self.update_count})")
            else:
                print("⚠️ Vérification terminée avec des avertissements")
                
        except Exception as e:
            print(f"❌ Erreur lors de la vérification: {e}")
            print("🔄 Nouvelle tentative dans 60 secondes...")
            time.sleep(60)

def create_systemd_service():
    """Crée un service systemd pour la surveillance automatique"""
    service_content = """[Unit]
Description=RagTime Book Watcher - Surveillance automatique des livres
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/Desktop/Ukraine3/RagTime/LumieresUkraine
ExecStart=/usr/bin/python3 /home/YOUR_USERNAME/Desktop/Ukraine3/RagTime/LumieresUkraine/watch_books.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    service_file = "ragtime-watcher.service"
    with open(service_file, 'w') as f:
        f.write(service_content)
    
    print(f"📄 Service systemd créé: {service_file}")
    print("💡 Instructions d'installation:")
    print("   1. Remplacez YOUR_USERNAME par votre nom d'utilisateur")
    print("   2. Copiez le fichier: sudo cp ragtime-watcher.service /etc/systemd/system/")
    print("   3. Activez le service: sudo systemctl enable ragtime-watcher")
    print("   4. Démarrez le service: sudo systemctl start ragtime-watcher")

def create_cron_job():
    """Crée une tâche cron pour la surveillance"""
    cron_content = """# Surveillance automatique des livres RagTime
# Vérification toutes les 5 minutes
*/5 * * * * cd /home/YOUR_USERNAME/Desktop/Ukraine3/RagTime/LumieresUkraine && python3 update_books_from_db.py >> /tmp/ragtime-update.log 2>&1

# Nettoyage des logs (garder 7 jours)
0 2 * * 0 find /tmp/ragtime-update.log -mtime +7 -delete
"""
    
    cron_file = "ragtime-cron.txt"
    with open(cron_file, 'w') as f:
        f.write(cron_content)
    
    print(f"📄 Tâche cron créée: {cron_file}")
    print("💡 Instructions d'installation:")
    print("   1. Remplacez YOUR_USERNAME par votre nom d'utilisateur")
    print("   2. Ajoutez à votre crontab: crontab ragtime-cron.txt")
    print("   3. Vérifiez: crontab -l")

def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Surveillance automatique des livres")
    parser.add_argument("--interval", type=int, default=300, 
                       help="Intervalle de vérification en secondes (défaut: 300)")
    parser.add_argument("--create-service", action="store_true",
                       help="Créer un service systemd")
    parser.add_argument("--create-cron", action="store_true",
                       help="Créer une tâche cron")
    parser.add_argument("--once", action="store_true",
                       help="Exécuter une seule fois et quitter")
    
    args = parser.parse_args()
    
    if args.create_service:
        create_systemd_service()
        return
    
    if args.create_cron:
        create_cron_job()
        return
    
    if args.once:
        print("🌻 Exécution unique de la mise à jour")
        success = update_books()
        sys.exit(0 if success else 1)
    
    # Mode surveillance continue
    watcher = BookWatcher(args.interval)
    watcher.start()

if __name__ == "__main__":
    main() 