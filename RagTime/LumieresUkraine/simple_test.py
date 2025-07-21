#!/usr/bin/env python3
"""
Test simple pour l'API RagTime
"""

import requests
import json

def test_api():
    """Test simple de l'API"""
    print("🧪 Test simple de l'API RagTime")
    
    # Test de santé
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ API en bonne santé: {response.json()}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return
    
    # Test de recherche simple
    try:
        payload = {
            "query": "livres sur l'Ukraine",
            "useAI": False,
            "maxResults": 3
        }
        
        response = requests.post("http://localhost:5000/api/search", 
                               json=payload, timeout=10)
        
        print(f"Recherche: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recherche réussie")
            print(f"   Livres trouvés: {len(data.get('books', []))}")
            print(f"   Temps: {data.get('timing', {}).get('rag_time', 0):.3f}s")
        else:
            print(f"❌ Erreur recherche: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur recherche: {e}")

if __name__ == "__main__":
    test_api() 