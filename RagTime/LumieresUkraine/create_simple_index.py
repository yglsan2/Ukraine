#!/usr/bin/env python3
"""
Script très simple pour créer un index basique
"""

import json
import pickle
import numpy as np

# Charger les données
with open('books_data.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

print(f"Chargement de {len(books)} livres")

# Créer des embeddings factices pour tester
processed_books = []

for i, book in enumerate(books):
    print(f"Traitement livre {i+1}: {book['title']}")
    
    # Créer un embedding factice (384 dimensions comme sentence-transformers)
    embedding = np.random.rand(384).astype(np.float32)
    
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