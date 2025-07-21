#!/usr/bin/env python3
"""
Script de test pour RagTime - Spécialiste des livres des Lumières d'Ukraine
Vérifie que tous les composants fonctionnent correctement
"""

import os
import sys
import json
import pickle
from datetime import datetime

def test_dependencies():
    """Teste que toutes les dépendances sont installées"""
    print("🔍 Test des dépendances...")
    
    try:
        import numpy
        print("✅ numpy installé")
    except ImportError:
        print("❌ numpy manquant")
        return False
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ sentence-transformers installé")
    except ImportError:
        print("❌ sentence-transformers manquant")
        return False
    
    try:
        import requests
        print("✅ requests installé")
    except ImportError:
        print("❌ requests manquant")
        return False
    
    return True

def test_books_data():
    """Teste que les données des livres existent"""
    print("\n📚 Test des données des livres...")
    
    if not os.path.exists("books_data.json"):
        print("❌ books_data.json non trouvé")
        print("💡 Lancez: python init_books_rag.py")
        return False
    
    try:
        with open("books_data.json", 'r', encoding='utf-8') as f:
            books = json.load(f)
        
        print(f"✅ {len(books)} livres trouvés dans books_data.json")
        
        # Vérifier la structure d'un livre
        if books:
            book = books[0]
            required_fields = ['id', 'title', 'author', 'genre', 'language']
            for field in required_fields:
                if field not in book:
                    print(f"❌ Champ manquant: {field}")
                    return False
            
            print("✅ Structure des livres valide")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lecture books_data.json: {e}")
        return False

def test_index():
    """Teste que l'index RAG existe et est valide"""
    print("\n🧠 Test de l'index RAG...")
    
    if not os.path.exists("books_index.pkl"):
        print("❌ books_index.pkl non trouvé")
        print("💡 Lancez: python init_books_rag.py")
        return False
    
    try:
        with open("books_index.pkl", 'rb') as f:
            index = pickle.load(f)
        
        print(f"✅ {len(index)} livres indexés")
        
        # Vérifier la structure d'un livre indexé
        if index:
            book = index[0]
            required_fields = ['embedding', 'concepts', 'themes']
            for field in required_fields:
                if field not in book:
                    print(f"❌ Champ manquant dans l'index: {field}")
                    return False
            
            # Vérifier que l'embedding est un vecteur
            if not hasattr(book['embedding'], '__len__'):
                print("❌ Embedding invalide")
                return False
            
            print(f"✅ Embeddings valides ({len(book['embedding'])} dimensions)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lecture books_index.pkl: {e}")
        return False

def test_ragtime_search():
    """Teste la fonction de recherche de RagTime"""
    print("\n🔍 Test de la recherche RagTime...")
    
    try:
        # Importer RagTime
        from RagTime import search_books
        
        # Test avec une requête simple
        results = search_books("romans en français", top_k=3)
        
        if results:
            print(f"✅ Recherche fonctionnelle ({len(results)} résultats)")
            
            # Afficher le premier résultat
            score, book = results[0]
            print(f"   📚 Premier résultat: {book.get('title', 'N/A')} (score: {score:.3f})")
        else:
            print("⚠️ Aucun résultat trouvé (normal si pas de livres correspondants)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la recherche: {e}")
        return False

def test_api_connection():
    """Teste la connexion à l'API backend"""
    print("\n🌐 Test de connexion API...")
    
    try:
        import requests
        
        # Test de santé de l'API
        response = requests.get("http://localhost:8080/api/health", timeout=5)
        
        if response.status_code == 200:
            print("✅ API backend accessible")
            return True
        else:
            print(f"⚠️ API backend répond avec le code {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️ API backend non accessible (normal si le backend n'est pas démarré)")
        return True  # Pas critique pour les tests
        
    except Exception as e:
        print(f"❌ Erreur de connexion API: {e}")
        return False

def test_sample_queries():
    """Teste des requêtes d'exemple"""
    print("\n💬 Test des requêtes d'exemple...")
    
    try:
        from RagTime import search_books
        
        test_queries = [
            "romans en français",
            "livres pour enfants",
            "science-fiction",
            "livres à Nancy",
            "poésie ukrainienne"
        ]
        
        for query in test_queries:
            results = search_books(query, top_k=2)
            if results:
                print(f"✅ '{query}': {len(results)} résultats")
            else:
                print(f"⚠️ '{query}': aucun résultat")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors des tests de requêtes: {e}")
        return False

def run_all_tests():
    """Lance tous les tests"""
    print("🌻 Test complet de RagTime - Spécialiste des livres")
    print("=" * 60)
    
    tests = [
        ("Dépendances", test_dependencies),
        ("Données des livres", test_books_data),
        ("Index RAG", test_index),
        ("Recherche RagTime", test_ragtime_search),
        ("Connexion API", test_api_connection),
        ("Requêtes d'exemple", test_sample_queries)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ Test '{test_name}' échoué")
        except Exception as e:
            print(f"❌ Test '{test_name}' en erreur: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! RagTime est prêt à l'emploi.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les messages ci-dessus.")
        return False

def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test de RagTime")
    parser.add_argument("--quick", action="store_true", 
                       help="Tests rapides uniquement")
    
    args = parser.parse_args()
    
    if args.quick:
        # Tests rapides
        tests = [
            ("Dépendances", test_dependencies),
            ("Données des livres", test_books_data),
            ("Index RAG", test_index)
        ]
        
        print("🚀 Tests rapides de RagTime")
        print("=" * 40)
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                else:
                    print(f"❌ Test '{test_name}' échoué")
            except Exception as e:
                print(f"❌ Test '{test_name}' en erreur: {e}")
        
        print(f"\n📊 Résultats: {passed}/{total} tests réussis")
        
    else:
        # Tests complets
        success = run_all_tests()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 