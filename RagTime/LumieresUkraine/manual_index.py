#!/usr/bin/env python3
"""
Script manuel pour créer l'index RAG
"""

import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Charger les données
with open('books_data.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

print(f"Chargement de {len(books)} livres")

# Charger le modèle
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("Modèle chargé")

# Traiter les livres
processed_books = []

for i, book in enumerate(books):
    print(f"Traitement livre {i+1}: {book['title']}")
    
    # Texte pour embedding
    text = f"{book['title']} {book['author']} {book['description']}"
    text += f" {book['genre']} {book['language']} {book['target_age']}"
    text += f" {book['condition']} {book['city']}"
    
    # Créer embedding
    embedding = model.encode(text)
    
    # Enrichir le livre
    enriched_book = book.copy()
    enriched_book['embedding'] = embedding
    enriched_book['concepts'] = ['genre', 'langue', 'age']
    enriched_book['themes'] = [book['genre'].lower(), book['language'].lower()]
    
    processed_books.append(enriched_book)

# Sauvegarder
with open('books_index.pkl', 'wb') as f:
    pickle.dump(processed_books, f)

print(f"Index sauvegardé avec {len(processed_books)} livres")
print("Terminé !") 