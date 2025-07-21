#!/usr/bin/env python3
"""
Script de mise à jour automatique des livres depuis la base de données
Synchronise l'index RAG avec les nouveaux livres ajoutés
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
import pickle
from typing import List, Dict, Any

# Configuration
BOOKS_DATA_FILE = "books_data.json"
INDEX_FILE = "books_index.pkl"
API_BASE_URL = "http://localhost:8080/api"  # URL de l'API backend

def get_books_from_api():
    """Récupère les livres depuis l'API backend"""
    try:
        # Endpoint pour récupérer tous les livres
        response = requests.get(f"{API_BASE_URL}/books", timeout=10)
        response.raise_for_status()
        
        books = response.json()
        print(f"📚 {len(books)} livres récupérés depuis l'API")
        return books
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération depuis l'API: {e}")
        print("💡 Vérifiez que le backend est démarré sur http://localhost:8080")
        return None

def get_new_books_since_last_update():
    """Récupère seulement les nouveaux livres depuis la dernière mise à jour"""
    try:
        # Lire la date de dernière mise à jour
        last_update_file = "last_update.txt"
        last_update = None
        
        if os.path.exists(last_update_file):
            with open(last_update_file, 'r') as f:
                last_update_str = f.read().strip()
                last_update = datetime.fromisoformat(last_update_str)
        
        # Si pas de dernière mise à jour, récupérer tous les livres
        if not last_update:
            return get_books_from_api()
        
        # Récupérer les livres modifiés depuis la dernière mise à jour
        since_date = last_update.isoformat()
        response = requests.get(
            f"{API_BASE_URL}/books/updated-since", 
            params={"since": since_date},
            timeout=10
        )
        response.raise_for_status()
        
        new_books = response.json()
        print(f"🆕 {len(new_books)} nouveaux livres trouvés depuis {last_update}")
        return new_books
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération des nouveaux livres: {e}")
        return None

def load_existing_books():
    """Charge les livres existants depuis le fichier JSON"""
    if os.path.exists(BOOKS_DATA_FILE):
        with open(BOOKS_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def merge_books(existing_books: List[Dict], new_books: List[Dict]):
    """Fusionne les livres existants avec les nouveaux"""
    # Créer un dictionnaire des livres existants par ID
    existing_by_id = {book['id']: book for book in existing_books}
    
    # Mettre à jour ou ajouter les nouveaux livres
    for new_book in new_books:
        book_id = new_book['id']
        if book_id in existing_by_id:
            # Mettre à jour le livre existant
            existing_by_id[book_id].update(new_book)
            print(f"🔄 Livre mis à jour: {new_book.get('title', 'N/A')}")
        else:
            # Ajouter le nouveau livre
            existing_by_id[book_id] = new_book
            print(f"➕ Nouveau livre ajouté: {new_book.get('title', 'N/A')}")
    
    # Convertir en liste
    merged_books = list(existing_by_id.values())
    
    # Trier par ID
    merged_books.sort(key=lambda x: x['id'])
    
    return merged_books

def save_books_data(books: List[Dict]):
    """Sauvegarde les données des livres"""
    with open(BOOKS_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)
    
    # Sauvegarder la date de mise à jour
    with open("last_update.txt", 'w') as f:
        f.write(datetime.now().isoformat())
    
    print(f"💾 {len(books)} livres sauvegardés dans {BOOKS_DATA_FILE}")

def update_index_from_books():
    """Met à jour l'index RAG à partir des livres"""
    try:
        # Importer le script d'initialisation
        from init_books_rag import build_books_index
        
        print("🔄 Mise à jour de l'index RAG...")
        success = build_books_index()
        
        if success:
            print("✅ Index RAG mis à jour avec succès")
        else:
            print("❌ Échec de la mise à jour de l'index RAG")
        
        return success
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Assurez-vous que init_books_rag.py est dans le même dossier")
        return False

def check_api_health():
    """Vérifie que l'API backend est accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Fonction principale"""
    print("🌻 Mise à jour automatique des livres des Lumières d'Ukraine")
    print("=" * 60)
    
    # Vérifier la santé de l'API
    if not check_api_health():
        print("❌ L'API backend n'est pas accessible")
        print("💡 Démarrez le backend avec: ./mvnw spring-boot:run")
        return False
    
    # Récupérer les nouveaux livres
    new_books = get_new_books_since_last_update()
    if new_books is None:
        return False
    
    if not new_books:
        print("✅ Aucun nouveau livre à traiter")
        return True
    
    # Charger les livres existants
    existing_books = load_existing_books()
    
    # Fusionner les livres
    all_books = merge_books(existing_books, new_books)
    
    # Sauvegarder les données
    save_books_data(all_books)
    
    # Mettre à jour l'index RAG
    success = update_index_from_books()
    
    if success:
        print("\n🎉 Mise à jour terminée avec succès !")
        print("📚 RagTime est maintenant à jour avec les derniers livres")
    else:
        print("\n❌ Échec de la mise à jour")
    
    return success

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Mise à jour des livres depuis la base de données")
    parser.add_argument("--force", action="store_true", help="Forcer la récupération de tous les livres")
    parser.add_argument("--api-url", default=API_BASE_URL, help="URL de l'API backend")
    
    args = parser.parse_args()
    
    if args.api_url:
        API_BASE_URL = args.api_url
    
    if args.force:
        # Supprimer le fichier de dernière mise à jour pour forcer la récupération complète
        if os.path.exists("last_update.txt"):
            os.remove("last_update.txt")
        print("🔄 Mode forcé: récupération de tous les livres")
    
    success = main()
    sys.exit(0 if success else 1) 