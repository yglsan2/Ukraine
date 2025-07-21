#!/usr/bin/env python3
"""
Test spécifique pour les résumés RagTime
Teste la génération de résumés avec et sans IA
"""

import requests
import json
import time

# Configuration
API_BASE_URL = "http://localhost:5000/api"

def test_summary_generation():
    """Test de génération de résumés"""
    print("📝 Test de génération de résumés")
    print("=" * 50)
    
    # Créer des livres de test avec des descriptions détaillées
    test_books = [
        {
            "id": 1,
            "title": "La Guerre et la Paix",
            "author": "Léon Tolstoï",
            "genre": "Roman historique",
            "description": "Un chef-d'œuvre de la littérature russe qui explore les thèmes de la guerre napoléonienne, de l'amour, de la famille et de la destinée humaine. L'histoire suit plusieurs familles aristocratiques russes pendant l'invasion napoléonienne de 1812, offrant une vision panoramique de la société russe de l'époque.",
            "language": "Français",
            "city": "Kiev",
            "status": "Disponible"
        },
        {
            "id": 2,
            "title": "Les Fleurs du Mal",
            "author": "Charles Baudelaire",
            "genre": "Poésie",
            "description": "Recueil de poèmes révolutionnaire qui explore les thèmes de la beauté, de la décadence, de l'amour et de la mort. Baudelaire y exprime sa vision du monde moderne et ses contradictions, créant une œuvre qui a profondément influencé la poésie française et européenne.",
            "language": "Français",
            "city": "Paris",
            "status": "Disponible"
        },
        {
            "id": 3,
            "title": "L'Étranger",
            "author": "Albert Camus",
            "genre": "Roman philosophique",
            "description": "Roman existentialiste qui suit Meursault, un homme indifférent à la mort de sa mère et à sa propre condamnation à mort. L'œuvre explore les thèmes de l'absurdité de l'existence, de la justice et de la condition humaine dans un monde sans sens.",
            "language": "Français",
            "city": "Alger",
            "status": "Disponible"
        }
    ]
    
    # Sauvegarder les livres de test
    with open("books_data.json", "w", encoding="utf-8") as f:
        json.dump(test_books, f, ensure_ascii=False, indent=2)
    
    print("✅ Livres de test créés")
    
    # Attendre que l'API soit prête
    print("⏳ Attente de l'API...")
    time.sleep(3)
    
    # Test des résumés pour chaque livre
    for book in test_books:
        print(f"\n📖 Test résumé pour: {book['title']}")
        print("-" * 40)
        
        # Test résumé standard
        try:
            response = requests.get(f"{API_BASE_URL}/books/{book['id']}/summary?style=standard", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Résumé standard:")
                print(f"   {data['summary']}")
            else:
                print(f"❌ Erreur résumé standard: {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur résumé standard: {e}")
        
        # Test résumé détaillé
        try:
            response = requests.get(f"{API_BASE_URL}/books/{book['id']}/summary?style=detailed", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Résumé détaillé:")
                print(f"   {data['summary']}")
            else:
                print(f"❌ Erreur résumé détaillé: {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur résumé détaillé: {e}")
        
        print()

def test_ai_summary_generation():
    """Test de génération de résumés avec IA"""
    print("\n🤖 Test de génération de résumés avec IA")
    print("=" * 50)
    
    # Vérifier le statut de l'IA
    try:
        response = requests.get(f"{API_BASE_URL}/ai/status", timeout=10)
        if response.status_code == 200:
            ai_status = response.json()
            print(f"IA disponible: {ai_status.get('enabled', False)}")
            print(f"Modèles: {ai_status.get('available_models', [])}")
            
            if not ai_status.get('enabled'):
                print("⚠️ IA non disponible - test des résumés sans IA")
                return
        else:
            print("❌ Impossible de vérifier le statut IA")
            return
    except Exception as e:
        print(f"❌ Erreur vérification IA: {e}")
        return
    
    # Test de recherche avec IA pour générer des résumés
    test_queries = [
        "Résume le livre La Guerre et la Paix",
        "Fais un résumé détaillé des Fleurs du Mal",
        "Explique le thème principal de L'Étranger"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Test: {query}")
        print("-" * 30)
        
        try:
            payload = {
                "query": query,
                "useAI": True,
                "maxResults": 1
            }
            
            response = requests.post(f"{API_BASE_URL}/search", json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Recherche réussie")
                print(f"   Temps total: {data.get('timing', {}).get('total_time', 0):.3f}s")
                print(f"   IA utilisée: {data.get('ai_used', False)}")
                
                if data.get('ai_response'):
                    print(f"   Réponse IA: {data['ai_response']}")
                else:
                    print("   Aucune réponse IA générée")
                    
            else:
                print(f"❌ Erreur recherche: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur recherche: {e}")

def test_summary_comparison():
    """Comparaison des résumés avec et sans IA"""
    print("\n⚖️ Comparaison des résumés")
    print("=" * 50)
    
    query = "Résume le livre La Guerre et la Paix de Tolstoï"
    
    # Test sans IA
    print("🔍 Test sans IA:")
    try:
        payload = {
            "query": query,
            "useAI": False,
            "maxResults": 1
        }
        
        start_time = time.time()
        response = requests.post(f"{API_BASE_URL}/search", json=payload, timeout=10)
        rag_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Temps: {rag_time:.3f}s")
            print(f"   Réponse: {data.get('response', 'N/A')[:200]}...")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test avec IA
    print("\n🤖 Test avec IA:")
    try:
        payload = {
            "query": query,
            "useAI": True,
            "maxResults": 1
        }
        
        start_time = time.time()
        response = requests.post(f"{API_BASE_URL}/search", json=payload, timeout=30)
        total_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Temps total: {total_time:.3f}s")
            print(f"   Temps IA: {data.get('timing', {}).get('ai_time', 0):.3f}s")
            print(f"   Réponse: {data.get('response', 'N/A')[:200]}...")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

def main():
    """Fonction principale"""
    print("🧪 Tests des résumés RagTime")
    print("=" * 60)
    
    # Vérifier que l'API est disponible
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ API RagTime non disponible")
            print("   Démarrez l'API avec: ./start_ragtime_api.sh")
            return False
    except Exception as e:
        print("❌ Impossible de se connecter à l'API RagTime")
        print("   Démarrez l'API avec: ./start_ragtime_api.sh")
        return False
    
    print("✅ API RagTime disponible")
    
    # Tests
    test_summary_generation()
    test_ai_summary_generation()
    test_summary_comparison()
    
    print("\n" + "=" * 60)
    print("🎉 Tests des résumés terminés !")
    
    return True

if __name__ == "__main__":
    main() 