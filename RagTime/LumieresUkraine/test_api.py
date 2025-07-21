#!/usr/bin/env python3
"""
Script de test pour l'API RagTime
Teste tous les endpoints principaux
"""

import requests
import json
import time

# Configuration
API_BASE_URL = "http://localhost:5000/api"
TEST_QUERY = "livres sur l'Ukraine"

def test_health():
    """Test de santé de l'API"""
    print("🏥 Test de santé...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API en bonne santé: {data}")
            return True
        else:
            print(f"❌ Erreur santé: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False

def test_search_simple():
    """Test de recherche simple (sans IA)"""
    print("\n🔍 Test recherche simple...")
    try:
        payload = {
            "query": TEST_QUERY,
            "useAI": False,
            "maxResults": 5
        }
        
        response = requests.post(f"{API_BASE_URL}/search", 
                               json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recherche réussie")
            print(f"   Livres trouvés: {len(data.get('books', []))}")
            print(f"   Temps RAG: {data.get('timing', {}).get('rag_time', 0):.3f}s")
            print(f"   IA utilisée: {data.get('ai_used', False)}")
            return True
        else:
            print(f"❌ Erreur recherche: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur recherche: {e}")
        return False

def test_search_with_ai():
    """Test de recherche avec IA"""
    print("\n🤖 Test recherche avec IA...")
    try:
        payload = {
            "query": TEST_QUERY,
            "useAI": True,
            "maxResults": 3
        }
        
        response = requests.post(f"{API_BASE_URL}/search", 
                               json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recherche IA réussie")
            print(f"   Livres trouvés: {len(data.get('books', []))}")
            print(f"   Temps total: {data.get('timing', {}).get('total_time', 0):.3f}s")
            print(f"   IA utilisée: {data.get('ai_used', False)}")
            if data.get('ai_response'):
                print(f"   Réponse IA: {data['ai_response'][:100]}...")
            return True
        else:
            print(f"❌ Erreur recherche IA: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur recherche IA: {e}")
        return False

def test_books_list():
    """Test de la liste des livres"""
    print("\n📚 Test liste des livres...")
    try:
        response = requests.get(f"{API_BASE_URL}/books?limit=5", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Liste des livres récupérée")
            print(f"   Nombre de livres: {len(data.get('books', []))}")
            return True
        else:
            print(f"❌ Erreur liste livres: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur liste livres: {e}")
        return False

def test_book_details():
    """Test des détails d'un livre"""
    print("\n📖 Test détails livre...")
    try:
        response = requests.get(f"{API_BASE_URL}/books/0", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Détails livre récupérés")
            print(f"   Titre: {data.get('title', 'N/A')}")
            print(f"   Auteur: {data.get('author', 'N/A')}")
            return True
        else:
            print(f"❌ Erreur détails livre: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur détails livre: {e}")
        return False

def test_book_summary():
    """Test du résumé d'un livre"""
    print("\n📝 Test résumé livre...")
    try:
        response = requests.get(f"{API_BASE_URL}/books/0/summary", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Résumé récupéré")
            print(f"   Style: {data.get('style', 'N/A')}")
            print(f"   Résumé: {data.get('summary', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Erreur résumé: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur résumé: {e}")
        return False

def test_ai_status():
    """Test du statut de l'IA"""
    print("\n🤖 Test statut IA...")
    try:
        response = requests.get(f"{API_BASE_URL}/ai/status", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Statut IA récupéré")
            print(f"   IA activée: {data.get('enabled', False)}")
            print(f"   Mode: {data.get('mode', 'N/A')}")
            print(f"   Modèles disponibles: {data.get('available_models', [])}")
            return True
        else:
            print(f"❌ Erreur statut IA: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur statut IA: {e}")
        return False

def test_statistics():
    """Test des statistiques"""
    print("\n📊 Test statistiques...")
    try:
        response = requests.get(f"{API_BASE_URL}/statistics", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Statistiques récupérées")
            print(f"   Total livres: {data.get('total_books', 0)}")
            print(f"   Total résumés: {data.get('total_summaries', 0)}")
            print(f"   IA activée: {data.get('ai_enabled', False)}")
            return True
        else:
            print(f"❌ Erreur statistiques: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur statistiques: {e}")
        return False

def test_search_endpoints():
    """Test des endpoints de recherche spécialisés"""
    print("\n🎯 Test endpoints de recherche...")
    
    endpoints = [
        ("/search/simple", "Recherche simple"),
        ("/search/fast", "Recherche rapide"),
        ("/search/quality", "Recherche qualité"),
        ("/search/theme/guerre", "Recherche par thème"),
        ("/search/genre/Roman", "Recherche par genre"),
        ("/search/author/Auteur", "Recherche par auteur")
    ]
    
    success_count = 0
    
    for endpoint, description in endpoints:
        try:
            print(f"   Test {description}...")
            
            if endpoint.startswith("/search/theme") or endpoint.startswith("/search/genre") or endpoint.startswith("/search/author"):
                # GET request
                response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
            else:
                # POST request
                payload = {"query": TEST_QUERY, "maxResults": 3}
                response = requests.post(f"{API_BASE_URL}{endpoint}", json=payload, timeout=15)
            
            if response.status_code == 200:
                print(f"   ✅ {description} OK")
                success_count += 1
            else:
                print(f"   ❌ {description} échoué: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {description} erreur: {e}")
    
    print(f"   📊 {success_count}/{len(endpoints)} endpoints réussis")
    return success_count == len(endpoints)

def main():
    """Fonction principale de test"""
    print("🧪 Tests de l'API RagTime")
    print("=" * 50)
    
    # Attendre que l'API soit prête
    print("⏳ Attente du démarrage de l'API...")
    time.sleep(2)
    
    # Tests
    tests = [
        test_health,
        test_search_simple,
        test_search_with_ai,
        test_books_list,
        test_book_details,
        test_book_summary,
        test_ai_status,
        test_statistics,
        test_search_endpoints
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur dans le test: {e}")
            results.append(False)
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"✅ Tests réussis: {success_count}/{total_count}")
    print(f"📈 Taux de succès: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("🎉 Tous les tests sont passés !")
    else:
        print("⚠️ Certains tests ont échoué")
    
    return success_count == total_count

if __name__ == "__main__":
    main() 