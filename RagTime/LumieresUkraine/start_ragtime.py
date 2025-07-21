#!/usr/bin/env python3
"""
Script de démarrage rapide pour RagTime
Configure et lance RagTime en quelques clics
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """Vérifie la version de Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        print(f"   Version actuelle: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} détecté")
    return True

def setup_virtual_environment():
    """Configure l'environnement virtuel"""
    print("\n🐍 Configuration de l'environnement virtuel...")
    
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print("📦 Création de l'environnement virtuel...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("✅ Environnement virtuel créé")
        except subprocess.CalledProcessError:
            print("❌ Erreur lors de la création de l'environnement virtuel")
            return False
    else:
        print("✅ Environnement virtuel existant")
    
    return True

def install_dependencies():
    """Installe les dépendances"""
    print("\n📦 Installation des dépendances...")
    
    # Déterminer le chemin de pip
    if os.name == 'nt':  # Windows
        pip_path = "venv/Scripts/pip"
    else:  # Linux/Mac
        pip_path = "venv/bin/pip"
    
    try:
        # Mettre à jour pip
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        print("✅ pip mis à jour")
        
        # Installer les dépendances
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dépendances installées")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False

def initialize_ragtime():
    """Initialise RagTime avec des données d'exemple"""
    print("\n🌻 Initialisation de RagTime...")
    
    # Déterminer le chemin de python
    if os.name == 'nt':  # Windows
        python_path = "venv/Scripts/python"
    else:  # Linux/Mac
        python_path = "venv/bin/python"
    
    try:
        # Créer l'index initial
        subprocess.run([python_path, "init_books_rag.py"], check=True)
        print("✅ Index RAG créé")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return False

def run_tests():
    """Lance les tests de base"""
    print("\n🧪 Tests de base...")
    
    # Déterminer le chemin de python
    if os.name == 'nt':  # Windows
        python_path = "venv/Scripts/python"
    else:  # Linux/Mac
        python_path = "venv/bin/python"
    
    try:
        # Tests rapides
        result = subprocess.run([python_path, "test_ragtime.py", "--quick"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Tests réussis")
            return True
        else:
            print("⚠️ Certains tests ont échoué")
            print(result.stdout)
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors des tests: {e}")
        return False

def launch_ragtime():
    """Lance RagTime"""
    print("\n🚀 Lancement de RagTime...")
    
    # Déterminer le chemin de python
    if os.name == 'nt':  # Windows
        python_path = "venv/Scripts/python"
    else:  # Linux/Mac
        python_path = "venv/bin/python"
    
    try:
        print("🌻 RagTime - Spécialiste des livres des Lumières d'Ukraine")
        print("💡 Tapez 'exit' pour quitter")
        print("=" * 60)
        
        # Lancer RagTime
        subprocess.run([python_path, "RagTime.py"])
        
    except KeyboardInterrupt:
        print("\n👋 Au revoir !")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

def show_menu():
    """Affiche le menu principal"""
    print("\n🌻 Menu RagTime")
    print("1. Configuration complète (recommandé)")
    print("2. Installation des dépendances uniquement")
    print("3. Initialisation uniquement")
    print("4. Tests uniquement")
    print("5. Lancer RagTime")
    print("6. Quitter")
    
    while True:
        try:
            choice = input("\nVotre choix (1-6): ").strip()
            
            if choice == "1":
                return "full_setup"
            elif choice == "2":
                return "install_only"
            elif choice == "3":
                return "init_only"
            elif choice == "4":
                return "test_only"
            elif choice == "5":
                return "launch_only"
            elif choice == "6":
                return "quit"
            else:
                print("❌ Choix invalide. Entrez un nombre entre 1 et 6.")
                
        except KeyboardInterrupt:
            return "quit"

def main():
    """Fonction principale"""
    print("🌻 RagTime - Spécialiste des livres des Lumières d'Ukraine")
    print("Script de démarrage rapide")
    print("=" * 50)
    
    # Vérifier Python
    if not check_python_version():
        sys.exit(1)
    
    # Afficher le menu
    choice = show_menu()
    
    if choice == "quit":
        print("👋 Au revoir !")
        return
    
    # Configuration complète
    if choice == "full_setup":
        print("\n🔧 Configuration complète...")
        
        if not setup_virtual_environment():
            sys.exit(1)
        
        if not install_dependencies():
            sys.exit(1)
        
        if not initialize_ragtime():
            sys.exit(1)
        
        if not run_tests():
            print("⚠️ Tests échoués, mais RagTime peut fonctionner")
        
        print("\n🎉 Configuration terminée !")
        
        # Demander si on veut lancer RagTime
        launch = input("Voulez-vous lancer RagTime maintenant ? (o/n): ").lower()
        if launch in ['o', 'oui', 'y', 'yes']:
            launch_ragtime()
    
    # Installation uniquement
    elif choice == "install_only":
        if not setup_virtual_environment():
            sys.exit(1)
        if not install_dependencies():
            sys.exit(1)
        print("✅ Installation terminée")
    
    # Initialisation uniquement
    elif choice == "init_only":
        if not initialize_ragtime():
            sys.exit(1)
        print("✅ Initialisation terminée")
    
    # Tests uniquement
    elif choice == "test_only":
        if not run_tests():
            sys.exit(1)
        print("✅ Tests terminés")
    
    # Lancement uniquement
    elif choice == "launch_only":
        launch_ragtime()

if __name__ == "__main__":
    main() 