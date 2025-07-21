#!/usr/bin/env python3
"""
Script simple pour créer l'index RAG des livres
"""

import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

def create_index():
    """Crée l'index RAG des livres"""
    print("🌻 Création de l'index RAG des livres...")
    
    # Charger les données des livres
    with open('books_data.json', 'r', encoding='utf-8') as f:
        books = json.load(f)
    
    print(f"📚 {len(books)} livres chargés")
    
    # Charger le modèle d'embeddings
    print("📥 Chargement du modèle d'embeddings...")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    # Traiter chaque livre
    print("🧠 Génération des embeddings...")
    processed_books = []
    
    for i, book in enumerate(books):
        print(f"  📊 Traitement du livre {i+1}/{len(books)}: {book['title']}")
        
        # Créer le texte pour l'embedding
        text_for_embedding = f"{book.get('title', '')} {book.get('author', '')} {book.get('description', '')}"
        text_for_embedding += f" {book.get('genre', '')} {book.get('language', '')} {book.get('target_age', '')}"
        text_for_embedding += f" {book.get('condition', '')} {book.get('city', '')}"
        
        # Générer l'embedding
        embedding = model.encode(text_for_embedding)
        
        # Enrichir le livre
        enriched_book = book.copy()
        enriched_book['embedding'] = embedding
        enriched_book['concepts'] = extract_concepts(book)
        enriched_book['themes'] = extract_themes(book)
        
        processed_books.append(enriched_book)
    
    # Sauvegarder l'index
    print("💾 Sauvegarde de l'index...")
    with open('books_index.pkl', 'wb') as f:
        pickle.dump(processed_books, f)
    
    print(f"✅ Index sauvegardé: {len(processed_books)} livres indexés")
    return True

def extract_concepts(book):
    """Extrait les concepts du livre"""
    concepts = set()
    
    # Texte complet
    full_text = f"{book.get('title', '')} {book.get('author', '')} {book.get('description', '')}"
    full_text += f" {book.get('genre', '')} {book.get('language', '')} {book.get('target_age', '')}"
    full_text += f" {book.get('condition', '')} {book.get('city', '')}"
    
    norm_text = full_text.lower()
    
    # Concepts par type
    concept_keywords = {
        'genre': ['roman', 'poésie', 'histoire', 'culture', 'jeunesse', 'science-fiction', 'fantasy', 'policier', 'biographie', 'essai', 'théâtre'],
        'langue': ['français', 'english', 'deutsch', 'polski', 'ukrainien', 'russe', 'allemand', 'polonais', 'espagnol', 'italien'],
        'age': ['enfant', 'adolescent', 'adulte', 'senior', 'jeune'],
        'condition': ['excellent', 'très bon', 'bon', 'moyen', 'mauvais'],
        'disponibilite': ['disponible', 'emprunté', 'réservé', 'indisponible'],
        'localisation': ['ville', 'code postal', 'géolocalisation'],
        'auteur': ['écrivain', 'écrivaine', 'auteur', 'autrice'],
        'isbn': ['isbn', 'numéro', 'identifiant'],
        'publication': ['année', 'date', 'édition', 'éditeur']
    }
    
    for concept_type, keywords in concept_keywords.items():
        for keyword in keywords:
            if keyword in norm_text:
                concepts.add(concept_type)
                break
    
    return list(concepts)

def extract_themes(book):
    """Extrait les thèmes du livre"""
    themes = []
    
    # Thèmes basés sur le genre
    genre_themes = {
        'ROMAN': ['roman', 'fiction'],
        'POESIE': ['poésie', 'poème'],
        'HISTOIRE': ['histoire', 'historique'],
        'CULTURE': ['culture', 'culturel'],
        'JEUNESSE': ['jeunesse', 'enfant'],
        'SCIENCE_FICTION': ['science-fiction', 'sf'],
        'FANTASY': ['fantasy', 'fantastique'],
        'POLICIER': ['policier', 'mystère'],
        'BIOGRAPHIE': ['biographie', 'mémoires'],
        'ESSAI': ['essai', 'documentaire'],
        'THEATRE': ['théâtre', 'pièce'],
        'AUTRE': ['autre', 'divers']
    }
    
    genre = book.get('genre', '')
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
    
    language = book.get('language', '')
    if language in language_themes:
        themes.extend(language_themes[language])
    
    # Thème de disponibilité
    status = book.get('status', '')
    if status == 'AVAILABLE':
        themes.append('disponible')
    else:
        themes.append('indisponible')
    
    return list(set(themes))

if __name__ == "__main__":
    create_index() 