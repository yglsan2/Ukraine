#!/usr/bin/env python3
"""
Script d'initialisation du RAG pour les livres des Lumières d'Ukraine
Crée l'index pickle optimisé avec les données des livres
"""

import os
import sys
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import re
import unicodedata
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

# Configuration
INDEX_FILE = "books_index.pkl"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
BOOKS_DATA_FILE = "books_data.json"

def clean_text(text):
    """Nettoie le texte pour la comparaison"""
    if not text:
        return ""
    text = re.sub(r'(\*\*|__|\*|_)', '', text)
    text = text.lower()
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text

def extract_book_concepts(book_data):
    """Extrait les concepts métiers du livre"""
    concepts = set()
    
    # Texte complet pour l'analyse
    full_text = f"{book_data.get('title', '')} {book_data.get('author', '')} {book_data.get('description', '')}"
    full_text += f" {book_data.get('genre', '')} {book_data.get('language', '')} {book_data.get('target_age', '')}"
    full_text += f" {book_data.get('condition', '')} {book_data.get('city', '')}"
    
    norm_text = full_text.lower()
    
    # Concepts par type
    concept_keywords = {
        'genre': [
            'roman', 'poésie', 'histoire', 'culture', 'jeunesse', 'science-fiction', 
            'fantasy', 'policier', 'biographie', 'essai', 'théâtre', 'autre'
        ],
        'langue': [
            'français', 'english', 'deutsch', 'polski', 'українська', 'русский', 
            'español', 'italiano', 'ukrainien', 'russe', 'allemand', 'polonais', 'espagnol', 'italien'
        ],
        'age': [
            'enfant', 'adolescent', 'adulte', 'senior', 'jeune', 'tout public'
        ],
        'condition': [
            'excellent', 'très bon', 'bon', 'moyen', 'mauvais', 'état', 'qualité'
        ],
        'disponibilite': [
            'disponible', 'emprunté', 'réservé', 'indisponible', 'libre', 'occupé'
        ],
        'localisation': [
            'ville', 'code postal', 'géolocalisation', 'latitude', 'longitude', 'adresse'
        ],
        'auteur': [
            'écrivain', 'écrivaine', 'auteur', 'autrice'
        ],
        'isbn': [
            'isbn', 'numéro', 'identifiant', 'code'
        ],
        'publication': [
            'année', 'date', 'édition', 'éditeur', 'parution'
        ]
    }
    
    for concept_type, keywords in concept_keywords.items():
        for keyword in keywords:
            if keyword in norm_text:
                concepts.add(concept_type)
                break
    
    return list(concepts)

def extract_themes_from_book(book_data):
    """Extrait les thèmes à partir des données du livre"""
    themes = []
    
    # Thèmes basés sur le genre
    genre_themes = {
        'ROMAN': ['roman', 'fiction'],
        'POESIE': ['poésie', 'poème'],
        'HISTOIRE': ['histoire', 'historique'],
        'CULTURE': ['culture', 'culturel'],
        'JEUNESSE': ['jeunesse', 'enfant'],
        'SCIENCE_FICTION': ['science-fiction', 'sf', 'futuriste'],
        'FANTASY': ['fantasy', 'fantastique'],
        'POLICIER': ['policier', 'mystère', 'thriller'],
        'BIOGRAPHIE': ['biographie', 'mémoires'],
        'ESSAI': ['essai', 'documentaire'],
        'THEATRE': ['théâtre', 'pièce'],
        'AUTRE': ['autre', 'divers']
    }
    
    genre = book_data.get('genre', '')
    if genre in genre_themes:
        themes.extend(genre_themes[genre])
    
    # Thèmes basés sur la langue
    language_themes = {
        'FRENCH': ['français', 'france'],
        'ENGLISH': ['anglais', 'english'],
        'GERMAN': ['allemand', 'deutsch'],
        'POLISH': ['polonais', 'polski'],
        'UKRAINIAN': ['ukrainien', 'ukraine'],
        'RUSSIAN': ['russe', 'russie'],
        'SPANISH': ['espagnol', 'español'],
        'ITALIAN': ['italien', 'italiano']
    }
    
    language = book_data.get('language', '')
    if language in language_themes:
        themes.extend(language_themes[language])
    
    # Thèmes basés sur l'âge cible
    age_themes = {
        'ENFANT': ['enfant', 'jeune'],
        'ADOLESCENT': ['adolescent', 'jeune'],
        'ADULTE': ['adulte', 'mature'],
        'SENIOR': ['senior', 'mature']
    }
    
    target_age = book_data.get('target_age', '')
    if target_age in age_themes:
        themes.extend(age_themes[target_age])
    
    # Thème de localisation
    if book_data.get('city'):
        themes.append('localisation')
    
    # Thème de disponibilité
    status = book_data.get('status', '')
    if status == 'AVAILABLE':
        themes.append('disponible')
    else:
        themes.append('indisponible')
    
    return list(set(themes))

def create_sample_books_data():
    """Crée des données d'exemple pour les livres"""
    sample_books = [
        {
            "id": 1,
            "title": "Le Petit Prince",
            "author": "Antoine de Saint-Exupéry",
            "isbn": "9782070612758",
            "publication_year": 1943,
            "genre": "ROMAN",
            "target_age": "ENFANT",
            "language": "FRENCH",
            "condition": "EXCELLENT",
            "description": "Un conte poétique et philosophique sous l'apparence d'un livre pour enfants. Le narrateur, un aviateur, tombe en panne dans le désert du Sahara et fait la rencontre d'un petit prince venu d'une autre planète.",
            "city": "Nancy",
            "postal_code": "54000",
            "latitude": 48.6921,
            "longitude": 6.1844,
            "status": "AVAILABLE",
            "total_borrows": 15,
            "is_active": True,
            "created_at": "2024-01-15T10:30:00",
            "updated_at": "2024-01-20T14:45:00"
        },
        {
            "id": 2,
            "title": "1984",
            "author": "George Orwell",
            "isbn": "9782070368228",
            "publication_year": 1949,
            "genre": "SCIENCE_FICTION",
            "target_age": "ADULTE",
            "language": "ENGLISH",
            "condition": "BON",
            "description": "Un roman d'anticipation dystopique qui décrit une société totalitaire sous surveillance constante. Winston Smith travaille au ministère de la Vérité et commence à remettre en question le système.",
            "city": "Strasbourg",
            "postal_code": "67000",
            "latitude": 48.5734,
            "longitude": 7.7521,
            "status": "AVAILABLE",
            "total_borrows": 8,
            "is_active": True,
            "created_at": "2024-02-01T09:15:00",
            "updated_at": "2024-02-10T16:20:00"
        },
        {
            "id": 3,
            "title": "Les Fleurs du Mal",
            "author": "Charles Baudelaire",
            "isbn": "9782070413118",
            "publication_year": 1857,
            "genre": "POESIE",
            "target_age": "ADULTE",
            "language": "FRENCH",
            "condition": "TRES_BON",
            "description": "Recueil de poèmes majeur de la littérature française. Baudelaire y explore les thèmes de la beauté, de la mort, de l'amour et de la modernité urbaine.",
            "city": "Lyon",
            "postal_code": "69000",
            "latitude": 45.7578,
            "longitude": 4.8320,
            "status": "BORROWED",
            "total_borrows": 23,
            "is_active": True,
            "created_at": "2024-01-10T11:00:00",
            "updated_at": "2024-02-15T13:30:00"
        },
        {
            "id": 4,
            "title": "Harry Potter à l'école des sorciers",
            "author": "J.K. Rowling",
            "isbn": "9782070541270",
            "publication_year": 1997,
            "genre": "FANTASY",
            "target_age": "ADOLESCENT",
            "language": "FRENCH",
            "condition": "EXCELLENT",
            "description": "Premier tome de la série Harry Potter. Le jeune sorcier découvre qu'il a des pouvoirs magiques et intègre l'école de sorcellerie Poudlard.",
            "city": "Metz",
            "postal_code": "57000",
            "latitude": 49.1193,
            "longitude": 6.1757,
            "status": "AVAILABLE",
            "total_borrows": 31,
            "is_active": True,
            "created_at": "2024-01-05T08:45:00",
            "updated_at": "2024-02-12T10:15:00"
        },
        {
            "id": 5,
            "title": "Le Seigneur des Anneaux",
            "author": "J.R.R. Tolkien",
            "isbn": "9782070612881",
            "publication_year": 1954,
            "genre": "FANTASY",
            "target_age": "ADULTE",
            "language": "ENGLISH",
            "condition": "BON",
            "description": "Épopée fantasy qui suit la quête de Frodon Sacquet pour détruire l'Anneau Unique et sauver la Terre du Milieu du Seigneur des Ténèbres.",
            "city": "Nancy",
            "postal_code": "54000",
            "latitude": 48.6921,
            "longitude": 6.1844,
            "status": "RESERVED",
            "total_borrows": 12,
            "is_active": True,
            "created_at": "2024-01-20T14:20:00",
            "updated_at": "2024-02-18T09:30:00"
        }
    ]
    
    # Sauvegarder les données d'exemple
    with open(BOOKS_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(sample_books, f, ensure_ascii=False, indent=2)
    
    return sample_books

def load_books_data():
    """Charge les données des livres"""
    if os.path.exists(BOOKS_DATA_FILE):
        with open(BOOKS_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"📚 Création de données d'exemple dans {BOOKS_DATA_FILE}")
        return create_sample_books_data()

def build_books_index():
    """Construit l'index complet des livres"""
    print("🌻 Initialisation du RAG des livres des Lumières d'Ukraine...")
    
    # Charger les données des livres
    books_data = load_books_data()
    print(f"📚 {len(books_data)} livres chargés")
    
    # Charger le modèle d'embeddings
    print("📥 Chargement du modèle d'embeddings...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    # Traiter chaque livre
    print("🧠 Génération des embeddings...")
    processed_books = []
    
    for i, book in enumerate(books_data):
        if i % 10 == 0:
            print(f"  📊 {i}/{len(books_data)} livres traités")
        
        # Créer le texte pour l'embedding
        text_for_embedding = f"{book.get('title', '')} {book.get('author', '')} {book.get('description', '')}"
        text_for_embedding += f" {book.get('genre', '')} {book.get('language', '')} {book.get('target_age', '')}"
        text_for_embedding += f" {book.get('condition', '')} {book.get('city', '')}"
        
        if len(text_for_embedding.strip()) > 0:
            try:
                embedding = model.encode(text_for_embedding)
                
                # Enrichir le livre avec les métadonnées
                enriched_book = book.copy()
                enriched_book['embedding'] = embedding
                enriched_book['concepts'] = extract_book_concepts(book)
                enriched_book['themes'] = extract_themes_from_book(book)
                
                processed_books.append(enriched_book)
                
            except Exception as e:
                print(f"⚠️ Erreur embedding pour le livre {book.get('title', 'N/A')}: {e}")
        else:
            print(f"⚠️ Livre {book.get('title', 'N/A')} sans texte pour embedding")
    
    print(f"✅ {len(processed_books)} livres avec embeddings valides")
    
    # Sauvegarder l'index
    print("💾 Sauvegarde de l'index...")
    with open(INDEX_FILE, 'wb') as f:
        pickle.dump(processed_books, f)
    
    print(f"🎉 Index sauvegardé dans {INDEX_FILE}")
    print(f"📊 Statistiques:")
    print(f"   - Livres totales: {len(processed_books)}")
    
    # Statistiques par genre
    genre_counts = {}
    language_counts = {}
    city_counts = {}
    
    for book in processed_books:
        genre = book.get('genre', '')
        language = book.get('language', '')
        city = book.get('city', '')
        
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
        language_counts[language] = language_counts.get(language, 0) + 1
        city_counts[city] = city_counts.get(city, 0) + 1
    
    print(f"   - Genres: {len(genre_counts)}")
    for genre, count in sorted(genre_counts.items()):
        print(f"     • {genre}: {count} livres")
    
    print(f"   - Langues: {len(language_counts)}")
    for lang, count in sorted(language_counts.items()):
        print(f"     • {lang}: {count} livres")
    
    print(f"   - Villes: {len(city_counts)}")
    for city, count in sorted(city_counts.items()):
        print(f"     • {city}: {count} livres")
    
    return True

def update_books_from_database():
    """Met à jour les livres depuis la base de données (à implémenter)"""
    print("🔄 Fonction de mise à jour depuis la base de données")
    print("💡 Cette fonction sera implémentée pour se connecter à la base de données")
    print("💡 Elle permettra de synchroniser automatiquement les nouveaux livres")
    
    # TODO: Implémenter la connexion à la base de données
    # TODO: Récupérer les nouveaux livres
    # TODO: Mettre à jour l'index
    
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialisation du RAG des livres")
    parser.add_argument("--update", action="store_true", help="Mettre à jour depuis la base de données")
    
    args = parser.parse_args()
    
    if args.update:
        success = update_books_from_database()
    else:
        success = build_books_index()
    
    if success:
        print("\n🚀 Le RAG des livres est maintenant prêt !")
        print("Vous pouvez lancer: python RagTime.py")
    else:
        print("\n❌ Échec de l'initialisation")
        sys.exit(1) 