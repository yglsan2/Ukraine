#!/usr/bin/env python3
"""
Démo des résumés RagTime
Montre comment RagTime peut générer des résumés de livres
"""

import json
import time

def create_demo_books():
    """Crée des livres de démonstration"""
    books = [
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
        },
        {
            "id": 4,
            "title": "Le Petit Prince",
            "author": "Antoine de Saint-Exupéry",
            "genre": "Conte philosophique",
            "description": "Conte poétique qui raconte l'histoire d'un petit prince venu d'une autre planète. À travers ses rencontres sur Terre, il découvre les valeurs essentielles de la vie : l'amitié, l'amour, la responsabilité et le sens de l'existence.",
            "language": "Français",
            "city": "Paris",
            "status": "Disponible"
        }
    ]
    
    # Sauvegarder les livres
    with open("books_data.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)
    
    return books

def generate_smart_summaries(books):
    """Génère des résumés intelligents pour chaque livre"""
    print("📝 Génération des résumés intelligents...")
    
    summaries = {"summaries": {}}
    
    for book in books:
        # Analyser les thèmes du livre
        text = f"{book['title']} {book['description']} {book['genre']}".lower()
        themes = []
        
        # Détection de thèmes
        theme_keywords = {
            'guerre': ['guerre', 'conflit', 'batailles', 'napoléon'],
            'amour': ['amour', 'romance', 'passion', 'sentiment'],
            'famille': ['famille', 'parent', 'enfant', 'frère', 'sœur'],
            'philosophie': ['philosophie', 'existentiel', 'absurdité', 'sens'],
            'poésie': ['poésie', 'poème', 'vers', 'lyrique'],
            'aventure': ['aventure', 'voyage', 'découverte', 'planète'],
            'mort': ['mort', 'décès', 'fin', 'disparition'],
            'beauté': ['beauté', 'esthétique', 'art', 'création']
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in text for keyword in keywords):
                themes.append(theme)
        
        # Générer le résumé
        summary = f"« {book['title']} » par {book['author']} - {book['genre']}. "
        
        if themes:
            summary += f"Ce livre explore les thèmes de {', '.join(themes)}. "
        
        # Ajouter une description enrichie
        if "guerre" in themes:
            summary += "Une œuvre majeure qui examine les conséquences des conflits sur la société et les individus. "
        elif "amour" in themes:
            summary += "Une exploration profonde des relations humaines et des émotions. "
        elif "philosophie" in themes:
            summary += "Une réflexion sur le sens de l'existence et la condition humaine. "
        elif "poésie" in themes:
            summary += "Une œuvre lyrique qui révolutionne l'expression poétique. "
        elif "aventure" in themes:
            summary += "Un voyage initiatique qui éveille l'imagination et la réflexion. "
        
        summary += f"{book['description'][:100]}..."
        
        summaries["summaries"][book["id"]] = {
            "style": "standard",
            "summary": summary,
            "themes": themes
        }
    
    # Sauvegarder les résumés
    with open("smart_summaries.json", "w", encoding="utf-8") as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(books)} résumés générés")
    return summaries

def demo_search_with_summaries():
    """Démo de recherche avec résumés"""
    print("\n🔍 Démo de recherche avec résumés")
    print("=" * 50)
    
    # Charger les données
    with open("books_data.json", "r", encoding="utf-8") as f:
        books = json.load(f)
    
    with open("smart_summaries.json", "r", encoding="utf-8") as f:
        summaries_data = json.load(f)
    
    # Requêtes de test
    test_queries = [
        "livres sur la guerre et l'amour",
        "poésie française",
        "romans philosophiques",
        "contes pour enfants"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Requête: '{query}'")
        print("-" * 30)
        
        # Recherche simple par mots-clés
        results = []
        for book in books:
            text = f"{book['title']} {book['description']}".lower()
            score = 0
            
            # Score basé sur les mots-clés
            keywords = query.lower().split()
            for keyword in keywords:
                if keyword in text:
                    score += 1
            
            if score > 0:
                results.append((book, score))
        
        # Trier par score
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Afficher les résultats avec résumés
        for i, (book, score) in enumerate(results[:3]):
            print(f"{i+1}. {book['title']} (score: {score})")
            
            # Afficher le résumé
            summary = summaries_data["summaries"].get(book["id"], {}).get("summary", "Résumé non disponible")
            print(f"   📝 {summary}")
            
            # Afficher les thèmes
            themes = summaries_data["summaries"].get(book["id"], {}).get("themes", [])
            if themes:
                print(f"   🏷️ Thèmes: {', '.join(themes)}")
            
            print()

def demo_summary_styles():
    """Démo des différents styles de résumés"""
    print("\n🎨 Démo des styles de résumés")
    print("=" * 40)
    
    with open("smart_summaries.json", "r", encoding="utf-8") as f:
        summaries_data = json.load(f)
    
    for book_id, summary_data in summaries_data["summaries"].items():
        print(f"\n📖 Livre ID {book_id}:")
        print(f"   Style: {summary_data['style']}")
        print(f"   Résumé: {summary_data['summary']}")
        
        if 'themes' in summary_data:
            print(f"   Thèmes détectés: {', '.join(summary_data['themes'])}")

def main():
    """Fonction principale de démo"""
    print("🎭 Démo des résumés RagTime")
    print("=" * 50)
    
    # Créer les livres de démo
    books = create_demo_books()
    print(f"✅ {len(books)} livres de démo créés")
    
    # Générer les résumés
    summaries = generate_smart_summaries(books)
    
    # Démo de recherche
    demo_search_with_summaries()
    
    # Démo des styles
    demo_summary_styles()
    
    print("\n" + "=" * 50)
    print("🎉 Démo terminée !")
    print("\n📋 Ce que RagTime peut faire pour les résumés:")
    print("   ✅ Génération automatique de résumés intelligents")
    print("   ✅ Détection automatique des thèmes")
    print("   ✅ Intégration avec la recherche")
    print("   ✅ Résumés contextuels selon la requête")
    print("   ✅ Support de différents styles")
    print("   ✅ Fallback sans IA (toujours fonctionnel)")

if __name__ == "__main__":
    main() 