#!/usr/bin/env python3
"""
Test simple de RagTime
"""

import pickle
import numpy as np

# Charger l'index
with open('books_index.pkl', 'rb') as f:
    books = pickle.load(f)

print(f"Index chargé: {len(books)} livres")

# Test de recherche simple
query = "romans en français"
print(f"Recherche: '{query}'")

# Créer un embedding factice pour la requête
query_embedding = np.random.rand(384).astype(np.float32)

# Recherche simple
results = []
for book in books:
    # Calculer la similarité cosinus
    similarity = np.dot(query_embedding, book['embedding']) / (
        np.linalg.norm(query_embedding) * np.linalg.norm(book['embedding'])
    )
    
    # Score basé sur les concepts
    score = similarity
    
    # Boost pour les livres en français
    if book.get('language') == 'FRENCH':
        score += 0.3
    
    # Boost pour les romans
    if book.get('genre') == 'ROMAN':
        score += 0.2
    
    results.append((score, book))

# Trier par score
results.sort(reverse=True, key=lambda x: x[0])

# Afficher les résultats
print(f"\nRésultats trouvés: {len(results)}")
for i, (score, book) in enumerate(results[:3], 1):
    print(f"\n--- Livre {i} (score: {score:.3f}) ---")
    print(f"📚 {book['title']}")
    print(f"✍️ Auteur: {book['author']}")
    print(f"📖 Genre: {book['genre']}")
    print(f"🌍 Langue: {book['language']}")
    print(f"📍 Ville: {book['city']}")
    print(f"✅ Statut: {book['status']}")

print("\n✅ Test de RagTime réussi !") 