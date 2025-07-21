#!/usr/bin/env python3
"""
RagTime - Spécialiste des livres des Lumières d'Ukraine
Système RAG intelligent pour la recherche et recommandation de livres
"""

import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import re
import unicodedata
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

# Configuration
INDEX_FILE = 'books_index.pkl'
EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
BOOKS_DATA_FILE = 'books_data.json'

# Concepts et synonymes pour les livres
BOOK_CONCEPTS = {
    "genre": [
        "roman", "poésie", "histoire", "culture", "jeunesse", "science-fiction", 
        "fantasy", "policier", "biographie", "essai", "théâtre", "autre",
        "roman policier", "roman historique", "roman d'amour", "roman d'aventure"
    ],
    "langue": [
        "français", "english", "deutsch", "polski", "українська", "русский", 
        "español", "italiano", "ukrainien", "russe", "allemand", "polonais", "espagnol", "italien"
    ],
    "age": [
        "enfant", "adolescent", "adulte", "senior", "jeune", "tout public", 
        "0-12 ans", "13-17 ans", "18-64 ans", "65+ ans"
    ],
    "condition": [
        "excellent", "très bon", "bon", "moyen", "mauvais", "état", "qualité"
    ],
    "disponibilite": [
        "disponible", "emprunté", "réservé", "indisponible", "libre", "occupé"
    ],
    "localisation": [
        "ville", "code postal", "géolocalisation", "latitude", "longitude", "adresse"
    ],
    "auteur": [
        "écrivain", "écrivaine", "écrivain", "auteur", "autrice"
    ],
    "isbn": [
        "isbn", "numéro", "identifiant", "code"
    ],
    "publication": [
        "année", "date", "édition", "éditeur", "parution"
    ]
}

# Verbes d'action pour les livres
BOOK_ACTIONS = [
    'emprunter', 'réserver', 'chercher', 'trouver', 'rechercher', 'lire',
    'recommander', 'suggérer', 'proposer', 'disponible', 'localiser',
    'filtrer', 'trier', 'par', 'selon', 'pour', 'avec'
]

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

def extract_book_concepts(question):
    """Extrait les concepts liés aux livres de la question"""
    concepts = set()
    norm_q = question.lower()
    
    for concept_type, keywords in BOOK_CONCEPTS.items():
        for keyword in keywords:
            if keyword in norm_q:
                concepts.add(concept_type)
                break
    
    return concepts

def extract_action_and_criteria(question):
    """Extrait l'action et les critères de recherche"""
    q = question.lower()
    action = None
    criteria = []
    
    # Détecter l'action
    for verb in BOOK_ACTIONS:
        if verb in q:
            action = verb
            break
    
    # Détecter les critères
    criteria_patterns = [
        r'par (\w+)',  # par genre, par auteur
        r'en (\w+)',   # en français, en anglais
        r'pour (\w+)', # pour enfants, pour adultes
        r'(\w+) (\w+)', # science fiction, roman policier
    ]
    
    for pattern in criteria_patterns:
        matches = re.findall(pattern, q)
        criteria.extend(matches)
    
    return action, criteria

def has_location_info(text):
    """Détecte si le texte contient des informations de localisation"""
    location_patterns = [
        r'\bville\b', r'\bcity\b', r'\bcode postal\b', r'\bpostal\b',
        r'\blatitude\b', r'\blongitude\b', r'\badresse\b', r'\baddress\b'
    ]
    for pat in location_patterns:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False

def search_books(question, top_k=5):
    """Recherche optimisée dans la base de livres"""
    # Charger l'index et le modèle
    if not os.path.exists(INDEX_FILE):
        print("❌ Index des livres non trouvé. Lancez d'abord: python init_books_rag.py")
        return []
    
    with open(INDEX_FILE, 'rb') as f:
        index = pickle.load(f)
    
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    # Extraire les informations de la question
    q_concepts = extract_book_concepts(question)
    action, criteria = extract_action_and_criteria(question)
    
    print(f"[DEBUG] Concepts détectés: {list(q_concepts)}")
    print(f"[DEBUG] Action: {action}, Critères: {criteria}")
    
    # Générer l'embedding de la question
    query_embedding = model.encode(question)
    
    # Recherche avec scoring hybride
    results = []
    for book in index:
        if book['embedding'] is None:
            continue
            
        # Score sémantique
        emb_score = np.dot(query_embedding, book['embedding']) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(book['embedding'])
        )
        
        # Score conceptuel
        book_concepts = set(book.get('concepts', []))
        concept_match = len(q_concepts & book_concepts)
        
        # Score titre et auteur
        title = clean_text(book.get('title', ''))
        author = clean_text(book.get('author', ''))
        title_contains_concept = any(c in title for c in q_concepts)
        author_contains_concept = any(c in author for c in q_concepts)
        
        # Score disponibilité
        is_available = book.get('status', '') == 'AVAILABLE'
        availability_boost = 0.1 if is_available else 0
        
        # Score localisation
        has_location = has_location_info(str(book))
        location_boost = 0.05 if has_location else 0
        
        # Score final
        score = emb_score
        if title_contains_concept:
            score += 0.3
        if author_contains_concept:
            score += 0.2
        if concept_match > 0:
            score += 0.2 * concept_match
        score += availability_boost
        score += location_boost
        
        results.append((score, book))
    
    # Trier par score
    results.sort(reverse=True, key=lambda x: x[0])
    return results[:top_k]

def format_book_info(book):
    """Formate les informations d'un livre pour l'affichage"""
    info = []
    info.append(f"📚 **{book['title']}**")
    info.append(f"✍️ Auteur: {book['author']}")
    
    if book.get('isbn'):
        info.append(f"🔢 ISBN: {book['isbn']}")
    
    if book.get('publication_year'):
        info.append(f"📅 Année: {book['publication_year']}")
    
    if book.get('genre'):
        info.append(f"📖 Genre: {book['genre']}")
    
    if book.get('language'):
        info.append(f"🌍 Langue: {book['language']}")
    
    if book.get('target_age'):
        info.append(f"👥 Public: {book['target_age']}")
    
    if book.get('condition'):
        info.append(f"⭐ État: {book['condition']}")
    
    if book.get('city'):
        info.append(f"📍 Ville: {book['city']}")
    
    if book.get('status'):
        status_emoji = "✅" if book['status'] == 'AVAILABLE' else "❌"
        info.append(f"{status_emoji} Statut: {book['status']}")
    
    if book.get('description'):
        desc = book['description']
        if len(desc) > 100:
            desc = desc[:100] + "..."
        info.append(f"📝 Description: {desc}")
    
    if book.get('total_borrows'):
        info.append(f"📊 Emprunts: {book['total_borrows']} fois")
    
    return "\n".join(info)

def main():
    """Interface principale"""
    print("🌻 RagTime - Spécialiste des livres des Lumières d'Ukraine")
    print("Tapez 'exit' pour quitter\n")
    
    while True:
        question = input("RagTime > ")
        if question.lower() in ["exit", "quit", "q"]:
            print("Au revoir ! 🌻")
            break
        
        try:
            results = search_books(question)
            
            if not results:
                print("❌ Aucun livre trouvé correspondant à votre recherche.")
                print("💡 Essayez de reformuler votre question ou utilisez des mots-clés comme:")
                print("   - 'romans en français'")
                print("   - 'livres pour enfants'")
                print("   - 'science-fiction disponible'")
                print("   - 'livres à Nancy'")
                continue
            
            print(f"\n📚 {len(results)} livre(s) trouvé(s):")
            for i, (score, book) in enumerate(results, 1):
                print(f"\n--- Livre {i} (pertinence: {score:.3f}) ---")
                print(format_book_info(book))
            
            print("\n" + "="*60 + "\n")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            print("Essayez de reformuler votre question.\n")

if __name__ == "__main__":
    main() 