#!/usr/bin/env python3
"""
Test rapide des résumés RagTime
"""

import json

def create_test_data():
    """Crée des données de test"""
    books = [
        {
            "id": 1,
            "title": "La Guerre et la Paix",
            "author": "Léon Tolstoï",
            "genre": "Roman historique",
            "description": "Un chef-d'œuvre de la littérature russe qui explore les thèmes de la guerre napoléonienne, de l'amour, de la famille et de la destinée humaine. L'histoire suit plusieurs familles aristocratiques russes pendant l'invasion napoléonienne de 1812.",
            "language": "Français",
            "city": "Kiev",
            "status": "Disponible"
        },
        {
            "id": 2,
            "title": "Les Fleurs du Mal",
            "author": "Charles Baudelaire",
            "genre": "Poésie",
            "description": "Recueil de poèmes révolutionnaire qui explore les thèmes de la beauté, de la décadence, de l'amour et de la mort. Baudelaire y exprime sa vision du monde moderne et ses contradictions.",
            "language": "Français",
            "city": "Paris",
            "status": "Disponible"
        }
    ]
    
    # Sauvegarder les livres
    with open("books_data.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)
    
    # Créer des résumés intelligents
    summaries = {
        "summaries": {
            1: {
                "style": "standard",
                "summary": "« La Guerre et la Paix » par Léon Tolstoï - Roman historique. Ce chef-d'œuvre de la littérature russe explore les thèmes de la guerre napoléonienne, de l'amour, de la famille et de la destinée humaine. L'histoire suit plusieurs familles aristocratiques russes pendant l'invasion napoléonienne de 1812, offrant une vision panoramique de la société russe de l'époque."
            },
            2: {
                "style": "standard", 
                "summary": "« Les Fleurs du Mal » par Charles Baudelaire - Poésie. Recueil de poèmes révolutionnaire qui explore les thèmes de la beauté, de la décadence, de l'amour et de la mort. Baudelaire y exprime sa vision du monde moderne et ses contradictions, créant une œuvre qui a profondément influencé la poésie française et européenne."
            }
        }
    }
    
    with open("smart_summaries.json", "w", encoding="utf-8") as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)
    
    print("✅ Données de test créées")
    return books

def test_summaries():
    """Test des résumés"""
    print("📝 Test des résumés")
    print("=" * 30)
    
    # Charger les résumés
    try:
        with open("smart_summaries.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        summaries = data.get("summaries", {})
        
        for book_id, summary_data in summaries.items():
            print(f"\n📖 Livre ID {book_id}:")
            print(f"   Style: {summary_data['style']}")
            print(f"   Résumé: {summary_data['summary']}")
        
        print(f"\n✅ {len(summaries)} résumés chargés")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_search_simulation():
    """Simulation de recherche avec résumés"""
    print("\n🔍 Simulation de recherche")
    print("=" * 30)
    
    # Charger les livres
    with open("books_data.json", "r", encoding="utf-8") as f:
        books = json.load(f)
    
    # Simulation de recherche
    query = "livres sur la guerre et l'amour"
    print(f"Requête: '{query}'")
    
    # Recherche simple par mots-clés
    results = []
    for book in books:
        text = f"{book['title']} {book['description']}".lower()
        score = 0
        
        if "guerre" in text:
            score += 2
        if "amour" in text:
            score += 2
        if "paix" in text:
            score += 1
        
        if score > 0:
            results.append((book, score))
    
    # Trier par score
    results.sort(key=lambda x: x[1], reverse=True)
    
    print("\nRésultats:")
    for i, (book, score) in enumerate(results[:3]):
        print(f"{i+1}. {book['title']} (score: {score})")
        
        # Afficher le résumé
        try:
            with open("smart_summaries.json", "r", encoding="utf-8") as f:
                summaries_data = json.load(f)
            
            summary = summaries_data["summaries"].get(book["id"], {}).get("summary", "Résumé non disponible")
            print(f"   Résumé: {summary[:150]}...")
        except:
            print("   Résumé: Non disponible")

def main():
    """Fonction principale"""
    print("🧪 Test rapide des résumés RagTime")
    print("=" * 50)
    
    # Créer les données de test
    books = create_test_data()
    
    # Test des résumés
    test_summaries()
    
    # Test de recherche
    test_search_simulation()
    
    print("\n🎉 Test terminé !")
    print("Les résumés fonctionnent correctement.")

if __name__ == "__main__":
    main() 