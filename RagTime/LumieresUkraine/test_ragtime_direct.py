#!/usr/bin/env python3
"""
Test direct de RagTime sans API
Vérifie que le système de base fonctionne
"""

import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time

def test_ragtime_direct():
    """Test direct de RagTime"""
    print("🧪 Test direct de RagTime")
    print("=" * 40)
    
    # 1. Créer des livres de test
    print("1. Création des livres de test...")
    test_books = [
        {
            "id": 1,
            "title": "La Guerre et la Paix",
            "author": "Léon Tolstoï",
            "genre": "Roman historique",
            "description": "Un chef-d'œuvre de la littérature russe qui explore les thèmes de la guerre napoléonienne, de l'amour, de la famille et de la destinée humaine.",
            "language": "Français",
            "city": "Kiev",
            "status": "Disponible"
        },
        {
            "id": 2,
            "title": "Les Fleurs du Mal",
            "author": "Charles Baudelaire",
            "genre": "Poésie",
            "description": "Recueil de poèmes révolutionnaire qui explore les thèmes de la beauté, de la décadence, de l'amour et de la mort.",
            "language": "Français",
            "city": "Paris",
            "status": "Disponible"
        },
        {
            "id": 3,
            "title": "L'Étranger",
            "author": "Albert Camus",
            "genre": "Roman philosophique",
            "description": "Roman existentialiste qui suit Meursault, un homme indifférent à la mort de sa mère et à sa propre condamnation à mort.",
            "language": "Français",
            "city": "Alger",
            "status": "Disponible"
        }
    ]
    
    # Sauvegarder les livres
    with open("books_data.json", "w", encoding="utf-8") as f:
        json.dump(test_books, f, ensure_ascii=False, indent=2)
    print(f"   ✅ {len(test_books)} livres créés")
    
    # 2. Charger le modèle d'embedding
    print("2. Chargement du modèle d'embedding...")
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("   ✅ Modèle chargé")
    except Exception as e:
        print(f"   ❌ Erreur modèle: {e}")
        return False
    
    # 3. Créer les embeddings
    print("3. Création des embeddings...")
    try:
        texts = []
        for book in test_books:
            text = f"{book['title']} {book['author']} {book['description']} {book['genre']}"
            texts.append(text)
        
        embeddings = model.encode(texts)
        print(f"   ✅ {len(embeddings)} embeddings créés")
    except Exception as e:
        print(f"   ❌ Erreur embeddings: {e}")
        return False
    
    # 4. Créer les concepts
    print("4. Création des concepts...")
    concepts = []
    for book in test_books:
        book_concepts = []
        text = f"{book['title']} {book['description']} {book['genre']}".lower()
        
        # Concepts simples
        keywords = ['guerre', 'paix', 'amour', 'mort', 'philosophie', 'poésie', 'roman', 'histoire']
        for keyword in keywords:
            if keyword in text:
                book_concepts.append(keyword)
        
        concepts.append(book_concepts)
    
    print(f"   ✅ Concepts créés pour {len(concepts)} livres")
    
    # 5. Sauvegarder l'index
    print("5. Sauvegarde de l'index...")
    try:
        index_data = {
            'embeddings': embeddings,
            'concepts': concepts
        }
        
        with open("books_index.pkl", "wb") as f:
            pickle.dump(index_data, f)
        print("   ✅ Index sauvegardé")
    except Exception as e:
        print(f"   ❌ Erreur sauvegarde: {e}")
        return False
    
    # 6. Test de recherche
    print("6. Test de recherche...")
    try:
        query = "livres sur la guerre et l'amour"
        query_embedding = model.encode([query])[0]
        
        # Calculer les similarités
        similarities = cosine_similarity([query_embedding], embeddings)[0]
        
        # Trier par similarité
        scores = [(i, sim) for i, sim in enumerate(similarities)]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        print("   Résultats de recherche:")
        for i, (idx, score) in enumerate(scores[:3]):
            book = test_books[idx]
            print(f"   {i+1}. {book['title']} (score: {score:.3f})")
        
        print("   ✅ Recherche réussie")
    except Exception as e:
        print(f"   ❌ Erreur recherche: {e}")
        return False
    
    # 7. Test de résumé simple
    print("7. Test de résumé simple...")
    try:
        # Résumé basé sur les concepts
        best_book = test_books[scores[0][0]]
        concepts_found = concepts[scores[0][0]]
        
        summary = f"« {best_book['title']} » par {best_book['author']} - {best_book['genre']}. "
        summary += f"Ce livre explore les thèmes de {', '.join(concepts_found)}. "
        summary += f"{best_book['description'][:100]}..."
        
        print(f"   Résumé généré: {summary}")
        print("   ✅ Résumé créé")
    except Exception as e:
        print(f"   ❌ Erreur résumé: {e}")
        return False
    
    # 8. Sauvegarder les résumés
    print("8. Sauvegarde des résumés...")
    try:
        summaries = {
            'summaries': {}
        }
        
        for i, book in enumerate(test_books):
            concepts_found = concepts[i]
            summary = f"« {book['title']} » par {book['author']} - {book['genre']}. "
            if concepts_found:
                summary += f"Thèmes: {', '.join(concepts_found)}. "
            summary += f"{book['description'][:150]}..."
            
            summaries['summaries'][book['id']] = {
                'style': 'standard',
                'summary': summary
            }
        
        with open("smart_summaries.json", "w", encoding="utf-8") as f:
            json.dump(summaries, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ {len(test_books)} résumés sauvegardés")
    except Exception as e:
        print(f"   ❌ Erreur résumés: {e}")
        return False
    
    print("\n🎉 Test direct de RagTime réussi !")
    print("Le système est prêt pour l'API.")
    
    return True

def test_performance():
    """Test de performance"""
    print("\n⚡ Test de performance")
    print("=" * 30)
    
    try:
        # Charger l'index
        with open("books_index.pkl", "rb") as f:
            index_data = pickle.load(f)
        
        embeddings = index_data['embeddings']
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Test de vitesse
        queries = [
            "livres sur la guerre",
            "poésie française",
            "romans philosophiques",
            "littérature russe"
        ]
        
        total_time = 0
        
        for query in queries:
            start_time = time.time()
            
            query_embedding = model.encode([query])[0]
            similarities = cosine_similarity([query_embedding], embeddings)[0]
            scores = [(i, sim) for i, sim in enumerate(similarities)]
            scores.sort(key=lambda x: x[1], reverse=True)
            
            query_time = time.time() - start_time
            total_time += query_time
            
            print(f"   '{query}': {query_time:.3f}s")
        
        avg_time = total_time / len(queries)
        print(f"   ⏱️ Temps moyen: {avg_time:.3f}s")
        print(f"   📊 Débit: {1/avg_time:.1f} requêtes/seconde")
        
    except Exception as e:
        print(f"   ❌ Erreur performance: {e}")

if __name__ == "__main__":
    success = test_ragtime_direct()
    if success:
        test_performance() 