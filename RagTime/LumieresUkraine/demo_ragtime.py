#!/usr/bin/env python3
"""
Démonstration de RagTime - Spécialiste des livres des Lumières d'Ukraine
"""

import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

def demo_ragtime():
    """Démonstration complète de RagTime"""
    print("🌻 RagTime - Spécialiste des livres des Lumières d'Ukraine")
    print("=" * 60)
    
    # Charger l'index
    print("📚 Chargement de l'index des livres...")
    with open('books_index.pkl', 'rb') as f:
        books = pickle.load(f)
    print(f"✅ {len(books)} livres chargés")
    
    # Charger le modèle
    print("🧠 Chargement du modèle d'embeddings...")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    print("✅ Modèle chargé")
    
    # Démonstrations
    demos = [
        "romans en français",
        "livres pour enfants",
        "science-fiction disponible",
        "livres à Nancy",
        "poésie ukrainienne",
        "fantasy en anglais"
    ]
    
    for query in demos:
        print(f"\n🔍 Recherche: '{query}'")
        print("-" * 40)
        
        # Créer l'embedding de la requête
        query_embedding = model.encode(query)
        
        # Recherche
        results = []
        for book in books:
            # Similarité cosinus
            similarity = np.dot(query_embedding, book['embedding']) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(book['embedding'])
            )
            
            # Score hybride
            score = similarity
            
            # Boost pour les concepts
            if 'français' in query.lower() and book.get('language') == 'FRENCH':
                score += 0.3
            if 'anglais' in query.lower() and book.get('language') == 'ENGLISH':
                score += 0.3
            if 'roman' in query.lower() and book.get('genre') == 'ROMAN':
                score += 0.2
            if 'enfant' in query.lower() and book.get('target_age') == 'ENFANT':
                score += 0.2
            if 'nancy' in query.lower() and book.get('city') == 'Nancy':
                score += 0.3
            if 'disponible' in query.lower() and book.get('status') == 'AVAILABLE':
                score += 0.1
            
            results.append((score, book))
        
        # Trier par score
        results.sort(reverse=True, key=lambda x: x[0])
        
        # Afficher les 3 meilleurs résultats
        for i, (score, book) in enumerate(results[:3], 1):
            print(f"\n📚 Livre {i} (pertinence: {score:.3f})")
            print(f"   Titre: {book['title']}")
            print(f"   Auteur: {book['author']}")
            print(f"   Genre: {book['genre']}")
            print(f"   Langue: {book['language']}")
            print(f"   Public: {book['target_age']}")
            print(f"   Ville: {book['city']}")
            print(f"   Statut: {book['status']}")
            if book.get('isbn'):
                print(f"   ISBN: {book['isbn']}")
    
    print("\n" + "=" * 60)
    print("🎉 Démonstration terminée !")
    print("💡 RagTime est maintenant prêt à l'emploi")
    print("🌻 Pour lancer l'interface interactive: python RagTime.py")

if __name__ == "__main__":
    demo_ragtime() 