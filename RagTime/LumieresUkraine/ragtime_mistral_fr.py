#!/usr/bin/env python3
"""
RagTime Mistral FR - Système RAG optimisé français avec Mistral 7B Instruct
Spécialisé pour résumés de livres et compréhension fine du français
"""

import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import os
import requests
import time

class RagTimeMistralFR:
    def __init__(self, index_path: str = "books_index.pkl", data_path: str = "books_data.json", 
                 ollama_url: str = "http://localhost:11434"):
        self.index_path = index_path
        self.data_path = data_path
        self.ollama_url = ollama_url
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.books_data = []
        self.embeddings = []
        self.concepts = []
        self.user_history = {}
        self.themes_extracted = {}
        self.book_summaries = {}  # Cache des résumés générés
        
        # Modèle Mistral 7B Instruct optimisé français
        self.mistral_model = "mistral:7b-instruct"
        
        self.load_data()
        self.extract_themes()
        self.check_mistral_connection()
    
    def check_mistral_connection(self):
        """Vérifie la connexion à Ollama et Mistral"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                mistral_available = any('mistral' in model['name'].lower() for model in models)
                
                if mistral_available:
                    print("✅ Ollama connecté - Mistral disponible")
                    self.ai_available = True
                    
                    # Test rapide de Mistral
                    test_response = self.call_mistral("Bonjour, test de connexion en français.")
                    if "test" in test_response.lower():
                        print("✅ Mistral 7B Instruct opérationnel")
                    else:
                        print("⚠️ Mistral disponible mais réponse inattendue")
                        self.ai_available = False
                else:
                    print("⚠️ Ollama connecté mais Mistral non trouvé")
                    print("💡 Installez Mistral avec: ollama pull mistral:7b-instruct")
                    self.ai_available = False
            else:
                print("❌ Impossible de se connecter à Ollama")
                self.ai_available = False
        except Exception as e:
            print(f"❌ Erreur de connexion Ollama: {e}")
            self.ai_available = False
    
    def load_data(self):
        """Charge les données et l'index"""
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.books_data = json.load(f)
        
        if os.path.exists(self.index_path):
            with open(self.index_path, 'rb') as f:
                index_data = pickle.load(f)
                self.embeddings = index_data['embeddings']
                self.concepts = index_data['concepts']
    
    def extract_themes(self):
        """Extrait automatiquement les thèmes de chaque livre"""
        theme_keywords = {
            'amitié': ['ami', 'amitié', 'solidarité', 'entraide', 'groupe', 'camaraderie'],
            'aventure': ['aventure', 'voyage', 'découverte', 'exploration', 'quête', 'pérégrination'],
            'famille': ['famille', 'parent', 'enfant', 'frère', 'sœur', 'mère', 'père', 'foyer'],
            'guerre': ['guerre', 'conflit', 'paix', 'résistance', 'liberté', 'combat', 'batailles'],
            'nature': ['nature', 'animal', 'forêt', 'mer', 'montagne', 'environnement', 'faune', 'flore'],
            'culture': ['culture', 'tradition', 'coutume', 'festival', 'art', 'patrimoine', 'héritage'],
            'éducation': ['école', 'apprentissage', 'connaissance', 'savoir', 'étude', 'enseignement'],
            'amour': ['amour', 'romance', 'sentiment', 'cœur', 'passion', 'affection', 'tendresse'],
            'mystère': ['mystère', 'énigme', 'secret', 'suspense', 'policier', 'intrigue'],
            'fantasy': ['magie', 'fantastique', 'créature', 'sort', 'royaume', 'enchantement'],
            'histoire': ['historique', 'passé', 'époque', 'événement', 'personnage', 'chronique'],
            'science': ['science', 'technologie', 'découverte', 'invention', 'expérience', 'recherche'],
            'philosophie': ['philosophie', 'réflexion', 'question', 'pensée', 'sagesse', 'méditation'],
            'humour': ['humour', 'comique', 'drôle', 'rire', 'amusement', 'gaieté'],
            'émotion': ['émotion', 'sentiment', 'joie', 'tristesse', 'peur', 'espoir', 'mélancolie']
        }
        
        for i, book in enumerate(self.books_data):
            text = f"{book.get('title', '')} {book.get('description', '')} {book.get('genre', '')}"
            text_lower = text.lower()
            
            book_themes = []
            for theme, keywords in theme_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    book_themes.append(theme)
            
            self.themes_extracted[i] = book_themes
    
    def call_mistral(self, prompt: str, max_tokens: int = 300) -> str:
        """Appelle Mistral 7B Instruct avec prompt optimisé français"""
        if not self.ai_available:
            return "IA non disponible"
        
        try:
            # Prompt optimisé pour Mistral en français
            formatted_prompt = self.format_prompt_for_mistral(prompt)
            
            payload = {
                "model": self.mistral_model,
                "prompt": formatted_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.4,  # Équilibré pour créativité et cohérence
                    "top_p": 0.85,
                    "max_tokens": max_tokens,
                    "num_ctx": 4096,  # Contexte étendu pour Mistral
                    "repeat_penalty": 1.1,
                    "top_k": 40
                }
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", 
                                   json=payload, timeout=20)
            
            if response.status_code == 200:
                return response.json().get('response', 'Erreur de réponse')
            else:
                return f"Erreur HTTP: {response.status_code}"
                
        except Exception as e:
            return f"Erreur Mistral: {str(e)}"
    
    def format_prompt_for_mistral(self, prompt: str) -> str:
        """Formate le prompt pour Mistral 7B Instruct en français"""
        # Template optimisé pour Mistral Instruct
        mistral_template = f"""<s>[INST] Tu es un bibliothécaire expert de l'association "Les Lumières d'Ukraine", spécialisé dans la littérature ukrainienne et francophone. Tu réponds toujours en français impeccable, avec un style élégant et précis.

{prompt} [/INST]"""
        
        return mistral_template
    
    def search_books_with_mistral(self, query: str, user_id: str = None) -> Dict:
        """Recherche avec Mistral optimisé français"""
        
        # Recherche RAG classique
        query_embedding = self.model.encode([query])[0]
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        
        # Tri des résultats
        scores = [(i, sim) for i, sim in enumerate(similarities)]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Top résultats pour Mistral
        top_results = []
        for idx, score in scores[:5]:
            if idx < len(self.books_data):
                book = self.books_data[idx].copy()
                book['score'] = round(score, 3)
                book['themes'] = self.themes_extracted.get(idx, [])
                top_results.append(book)
        
        # Génération de réponse Mistral
        mistral_response = self.generate_mistral_response(query, top_results)
        
        return {
            'query': query,
            'results': top_results,
            'mistral_response': mistral_response,
            'total_found': len([s for s in scores if s[1] > 0.3])
        }
    
    def generate_mistral_response(self, query: str, results: List[Dict]) -> str:
        """Génère une réponse Mistral en français impeccable"""
        
        if not self.ai_available:
            return "Je ne peux pas générer de réponse IA pour le moment."
        
        # Contexte structuré pour Mistral
        context = "Voici les livres trouvés dans notre collection :\n\n"
        for i, book in enumerate(results):
            context += f"**{i+1}. {book['title']}** par {book['author']}\n"
            context += f"   Genre : {book.get('genre', 'Non spécifié')}\n"
            context += f"   Thèmes : {', '.join(book.get('themes', []))}\n"
            if book.get('description'):
                context += f"   Description : {book['description'][:120]}...\n"
            context += f"   Pertinence : {book['score']}\n\n"
        
        prompt = f"""Un lecteur recherche : "{query}"

{context}

En tant que bibliothécaire expert, réponds en français impeccable et élégant :
1. Présente les livres les plus pertinents avec enthousiasme
2. Explique pourquoi ils correspondent à la recherche
3. Suggère un ordre de lecture
4. Propose des alternatives si nécessaire

Réponse structurée et engageante :"""
        
        return self.call_mistral(prompt, max_tokens=400)
    
    def generate_book_summary_mistral(self, book_id: int, style: str = "standard") -> str:
        """Génère un résumé de livre avec Mistral en français impeccable"""
        if book_id >= len(self.books_data):
            return "Livre non trouvé"
        
        # Vérifier le cache
        cache_key = f"{book_id}_{style}"
        if cache_key in self.book_summaries:
            return self.book_summaries[cache_key]
        
        book = self.books_data[book_id]
        
        # Styles de résumé
        style_prompts = {
            "standard": "Génère un résumé captivant et informatif",
            "littéraire": "Écris un résumé dans un style littéraire élégant",
            "critique": "Fais une analyse critique et détaillée",
            "bref": "Fais un résumé concis en 2-3 phrases",
            "détaillé": "Fais un résumé complet et approfondi"
        }
        
        style_prompt = style_prompts.get(style, style_prompts["standard"])
        
        prompt = f"""{style_prompt} pour ce livre :

**Titre :** {book.get('title', 'N/A')}
**Auteur :** {book.get('author', 'N/A')}
**Genre :** {book.get('genre', 'N/A')}
**Description :** {book.get('description', 'N/A')}
**Thèmes :** {', '.join(self.themes_extracted.get(book_id, []))}

Le résumé doit être en français impeccable, engageant et donner envie de lire le livre."""
        
        summary = self.call_mistral(prompt, max_tokens=300)
        
        # Mise en cache
        self.book_summaries[cache_key] = summary
        
        return summary
    
    def generate_reading_guide_mistral(self, theme: str = None, age_group: str = None) -> str:
        """Génère un guide de lecture avec Mistral"""
        
        # Sélection des livres
        if theme:
            theme_books = []
            for i, book in enumerate(self.books_data):
                if i in self.themes_extracted and theme in self.themes_extracted[i]:
                    theme_books.append(book)
        else:
            theme_books = self.books_data[:8]
        
        context = "**Livres sélectionnés :**\n"
        for i, book in enumerate(theme_books):
            context += f"{i+1}. **{book['title']}** par {book['author']}\n"
            context += f"   Genre : {book.get('genre', 'N/A')}\n"
            context += f"   Thèmes : {', '.join(self.themes_extracted.get(i, []))}\n\n"
        
        prompt = f"""Crée un guide de lecture élégant et structuré en français impeccable.

{context}

**Public cible :** {age_group or 'Tous publics'}
**Thème :** {theme or 'Général'}

Le guide doit inclure :
- Une introduction captivante
- Les livres recommandés avec justifications
- Un parcours de lecture suggéré
- Des conseils pour approfondir
- Une conclusion engageante

Style : Élégant, accessible et enthousiaste."""
        
        return self.call_mistral(prompt, max_tokens=500)
    
    def compare_books_mistral(self, book_ids: List[int]) -> str:
        """Compare des livres avec Mistral"""
        if len(book_ids) < 2:
            return "Il faut au moins 2 livres pour faire une comparaison"
        
        books_info = []
        for book_id in book_ids:
            if book_id < len(self.books_data):
                book = self.books_data[book_id]
                book_info = {
                    'title': book.get('title', 'N/A'),
                    'author': book.get('author', 'N/A'),
                    'genre': book.get('genre', 'N/A'),
                    'description': book.get('description', 'N/A'),
                    'themes': self.themes_extracted.get(book_id, [])
                }
                books_info.append(book_info)
        
        context = "**Livres à comparer :**\n\n"
        for i, book in enumerate(books_info):
            context += f"**Livre {i+1} :** {book['title']} par {book['author']}\n"
            context += f"Genre : {book['genre']}\n"
            context += f"Thèmes : {', '.join(book['themes'])}\n"
            context += f"Description : {book['description'][:100]}...\n\n"
        
        prompt = f"""En tant que critique littéraire expert, fais une comparaison détaillée et érudite de ces livres :

{context}

La comparaison doit être structurée et couvrir :
- Les similitudes et différences stylistiques
- Les thèmes abordés et leur traitement
- Les publics cibles respectifs
- Les points forts de chaque œuvre
- Une recommandation finale argumentée

Style : Critique constructif, érudit et accessible."""
        
        return self.call_mistral(prompt, max_tokens=600)
    
    def get_recommendations_mistral(self, user_id: str = None, preferences: str = None) -> str:
        """Recommandations personnalisées avec Mistral"""
        
        # Analyse des préférences
        if user_id and user_id in self.user_history:
            user_history = self.user_history[user_id]
            preferred_genres = {}
            preferred_themes = {}
            
            for query, books in user_history.items():
                for book_idx in books:
                    if book_idx < len(self.books_data):
                        book = self.books_data[book_idx]
                        genre = book.get('genre', '')
                        if genre:
                            preferred_genres[genre] = preferred_genres.get(genre, 0) + 1
                        
                        if book_idx in self.themes_extracted:
                            for theme in self.themes_extracted[book_idx]:
                                preferred_themes[theme] = preferred_themes.get(theme, 0) + 1
            
            preferences_text = f"""
**Préférences détectées :**
- Genres préférés : {', '.join([f'{g} ({c})' for g, c in sorted(preferred_genres.items(), key=lambda x: x[1], reverse=True)[:3]])}
- Thèmes préférés : {', '.join([f'{t} ({c})' for t, c in sorted(preferred_themes.items(), key=lambda x: x[1], reverse=True)[:3]])}
"""
        else:
            preferences_text = "Nouvel utilisateur - recommandations générales"
        
        # Livres recommandés
        recommendations = self.get_popular_books()
        
        context = "**Livres recommandés :**\n"
        for i, book in enumerate(recommendations[:5]):
            context += f"{i+1}. **{book['title']}** par {book['author']}\n"
            context += f"   Genre : {book.get('genre', 'N/A')}\n"
            context += f"   Thèmes : {', '.join(book.get('themes', []))}\n\n"
        
        prompt = f"""En tant que bibliothécaire expert, fais des recommandations personnalisées et enthousiastes.

{preferences_text}

{context}

Présente ces recommandations de manière engageante :
- Explique pourquoi ces livres sont recommandés
- Met en avant leurs points forts
- Suggère un ordre de découverte
- Propose des alternatives

Style : Chaleureux, expert et enthousiaste."""
        
        return self.call_mistral(prompt, max_tokens=400)
    
    def get_popular_books(self) -> List[Dict]:
        """Retourne les livres populaires"""
        dummy_query = "livre populaire intéressant"
        query_embedding = self.model.encode([dummy_query])[0]
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        
        scores = [(i, sim) for i, sim in enumerate(similarities)]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return self.format_results(scores, 10)
    
    def format_results(self, results: List[Tuple[int, float]], max_results: int) -> List[Dict]:
        """Formate les résultats pour l'affichage"""
        formatted_results = []
        
        for i, (idx, score) in enumerate(results[:max_results]):
            if idx >= len(self.books_data):
                continue
            
            book = self.books_data[idx].copy()
            book['score'] = round(score, 3)
            book['rank'] = i + 1
            
            if idx in self.themes_extracted:
                book['themes'] = self.themes_extracted[idx]
            
            formatted_results.append(book)
        
        return formatted_results
    
    def get_statistics(self) -> Dict:
        """Statistiques avec info Mistral"""
        stats = {
            'total_books': len(self.books_data),
            'genres': {},
            'languages': {},
            'cities': {},
            'themes': {},
            'mistral_available': self.ai_available,
            'cached_summaries': len(self.book_summaries)
        }
        
        for book in self.books_data:
            genre = book.get('genre', 'Inconnu')
            stats['genres'][genre] = stats['genres'].get(genre, 0) + 1
            
            language = book.get('language', 'Inconnu')
            stats['languages'][language] = stats['languages'].get(language, 0) + 1
            
            city = book.get('city', 'Inconnu')
            stats['cities'][city] = stats['cities'].get(city, 0) + 1
        
        for themes in self.themes_extracted.values():
            for theme in themes:
                stats['themes'][theme] = stats['themes'].get(theme, 0) + 1
        
        return stats

def main():
    """Interface CLI pour RagTime Mistral FR"""
    ragtime = RagTimeMistralFR()
    
    print("🇫🇷 RagTime Mistral FR - Système RAG optimisé français")
    print("=" * 60)
    print(f"🤖 Modèle : {ragtime.mistral_model}")
    print(f"📚 Livres indexés : {len(ragtime.books_data)}")
    print(f"✅ Mistral disponible : {'Oui' if ragtime.ai_available else 'Non'}")
    
    while True:
        print("\nOptions disponibles :")
        print("1. Recherche avec Mistral")
        print("2. Résumé de livre (différents styles)")
        print("3. Guide de lecture")
        print("4. Comparaison de livres")
        print("5. Recommandations personnalisées")
        print("6. Statistiques")
        print("7. Quitter")
        
        choice = input("\nVotre choix (1-7) : ").strip()
        
        if choice == '1':
            query = input("Votre recherche : ")
            results = ragtime.search_books_with_mistral(query)
            
            print(f"\n🤖 Réponse Mistral :")
            print(results['mistral_response'])
            
            print(f"\n📚 Livres trouvés ({len(results['results'])}):")
            for book in results['results']:
                print(f"\n- {book['title']} par {book['author']}")
                print(f"  Score : {book['score']} | Thèmes : {', '.join(book.get('themes', []))}")
        
        elif choice == '2':
            print("Livres disponibles :")
            for i, book in enumerate(ragtime.books_data[:10]):
                print(f"{i+1}. {book['title']} par {book['author']}")
            
            try:
                book_id = int(input("\nChoisissez un livre (numéro) : ")) - 1
                print("\nStyles de résumé disponibles :")
                styles = ["standard", "littéraire", "critique", "bref", "détaillé"]
                for i, style in enumerate(styles):
                    print(f"{i+1}. {style}")
                
                style_choice = input("\nChoisissez un style (numéro) : ").strip()
                style = styles[int(style_choice) - 1] if style_choice.isdigit() and 1 <= int(style_choice) <= len(styles) else "standard"
                
                summary = ragtime.generate_book_summary_mistral(book_id, style)
                print(f"\n📖 Résumé ({style}) :")
                print(summary)
            except (ValueError, IndexError):
                print("Choix invalide")
        
        elif choice == '3':
            theme = input("Thème (optionnel) : ").strip() or None
            age_group = input("Groupe d'âge (optionnel) : ").strip() or None
            
            guide = ragtime.generate_reading_guide_mistral(theme, age_group)
            print(f"\n📚 Guide de lecture :")
            print(guide)
        
        elif choice == '4':
            print("Livres disponibles :")
            for i, book in enumerate(ragtime.books_data[:10]):
                print(f"{i+1}. {book['title']} par {book['author']}")
            
            try:
                book_ids = input("\nChoisissez 2-3 livres (numéros séparés par des virgules) : ")
                book_ids = [int(x.strip()) - 1 for x in book_ids.split(',')]
                comparison = ragtime.compare_books_mistral(book_ids)
                print(f"\n📊 Comparaison Mistral :")
                print(comparison)
            except ValueError:
                print("Format invalide")
        
        elif choice == '5':
            user_id = input("ID utilisateur (optionnel) : ").strip() or None
            preferences = input("Préférences (optionnel) : ").strip() or None
            
            recommendations = ragtime.get_recommendations_mistral(user_id, preferences)
            print(f"\n🎯 Recommandations Mistral :")
            print(recommendations)
        
        elif choice == '6':
            stats = ragtime.get_statistics()
            
            print("\n📊 Statistiques :")
            print(f"Total de livres : {stats['total_books']}")
            print(f"Mistral disponible : {'Oui' if stats['mistral_available'] else 'Non'}")
            print(f"Résumés en cache : {stats['cached_summaries']}")
            
            print("\nGenres populaires :")
            for genre, count in sorted(stats['genres'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {genre} : {count}")
        
        elif choice == '7':
            print("Au revoir ! 👋")
            break
        
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main() 