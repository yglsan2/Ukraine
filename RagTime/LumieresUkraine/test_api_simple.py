#!/usr/bin/env python3
"""
Test simple de l'API RagTime
"""

import requests
import json
import time

def test_api():
    """Test de l'API"""
    print("🧪 Test de l'API RagTime")
    print("=" * 40)
    
    # Test de santé
    try:
        print("🏥 Test de santé...")
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API en bonne santé: {data}")
        else:
            print(f"   ❌ Erreur: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur connexion: {e}")
        return False
    
    # Test de recherche
    try:
        print("\n🔍 Test de recherche...")
        payload = {
            "query": "livres sur l'Ukraine",
            "useAI": False,
            "maxResults": 3
        }
        
        response = requests.post("http://localhost:5000/api/search", 
                               json=payload, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Recherche réussie")
            print(f"   Livres trouvés: {len(data.get('books', []))}")
            print(f"   Temps RAG: {data.get('timing', {}).get('rag_time', 0):.3f}s")
            print(f"   IA utilisée: {data.get('ai_used', False)}")
        else:
            print(f"   ❌ Erreur recherche: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur recherche: {e}")
        return False
    
    # Test des résumés
    try:
        print("\n📝 Test des résumés...")
        response = requests.get("http://localhost:5000/api/books/1/summary", timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Résumé récupéré")
            print(f"   Résumé: {data.get('summary', 'N/A')[:100]}...")
        else:
            print(f"   ❌ Erreur résumé: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erreur résumé: {e}")
    
    print("\n🎉 Test terminé !")
    return True

if __name__ == "__main__":
    test_api() 