#!/usr/bin/env python3
"""
RagTime with AI - Système RAG avec IA Ollama pour les livres des Lumières d'Ukraine
Intégration d'Ollama avec Mistral 7B pour des fonctionnalités IA avancées
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

class RagTimeWithAI:
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
        self.conversation_history = {}  # Historique des conversations
        
        self.load_data()
        self.extract_themes()
        self.check_ollama_connection()
    
    def check_ollama_connection(self):
        """Vérifie la connexion à Ollama"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                mistral_available = any('mistral' in model['name'].lower() for model in models)
                if mistral_available:
                    print("✅ Ollama connecté - Mistral disponible")
                    self.ai_available = True
                else:
                    print("⚠️ Ollama connecté mais Mistral non trouvé")
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
            'amitié': ['ami', 'amitié', 'solidarité', 'entraide', 'groupe'],
            'aventure': ['aventure', 'voyage', 'découverte', 'exploration', 'quête'],
            'famille': ['famille', 'parent', 'enfant', 'frère', 'sœur', 'mère', 'père'],
            'guerre': ['guerre', 'conflit', 'paix', 'résistance', 'liberté'],
            'nature': ['nature', 'animal', 'forêt', 'mer', 'montagne', 'environnement'],
            'culture': ['culture', 'tradition', 'coutume', 'festival', 'art'],
            'éducation': ['école', 'apprentissage', 'connaissance', 'savoir', 'étude'],
            'amour': ['amour', 'romance', 'sentiment', 'cœur', 'passion'],
            'mystère': ['mystère', 'énigme', 'secret', 'suspense', 'policier'],
            'fantasy': ['magie', 'fantastique', 'créature', 'sort', 'royaume'],
            'histoire': ['historique', 'passé', 'époque', 'événement', 'personnage'],
            'science': ['science', 'technologie', 'découverte', 'invention', 'expérience'],
            'philosophie': ['philosophie', 'réflexion', 'question', 'pensée', 'sagesse'],
            'humour': ['humour', 'comique', 'drôle', 'rire', 'amusement'],
            'émotion': ['émotion', 'sentiment', 'joie', 'tristesse', 'peur', 'espoir']
        }
        
        for i, book in enumerate(self.books_data):
            text = f"{book.get('title', '')} {book.get('description', '')} {book.get('genre', '')}"
            text_lower = text.lower()
            
            book_themes = []
            for theme, keywords in theme_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    book_themes.append(theme)
            
            self.themes_extracted[i] = book_themes
    
    def call_ollama(self, prompt: str, model: str = "mistral:7b", max_tokens: int = 500) -> str:
        """Appelle Ollama avec une requête"""
        if not self.ai_available:
            return "IA non disponible"
        
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": max_tokens
                }
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", 
                                   json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json().get('response', 'Erreur de réponse')
            else:
                return f"Erreur HTTP: {response.status_code}"
                
        except Exception as e:
            return f"Erreur Ollama: {str(e)}"
    
    def search_books_with_ai(self, query: str, user_id: str = None, 
                           conversation_mode: bool = False) -> Dict:
        """Recherche avec assistance IA"""
        
        # Recherche RAG classique
        query_embedding = self.model.encode([query])[0]
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        
        # Tri des résultats
        scores = [(i, sim) for i, sim in enumerate(similarities)]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Top résultats pour l'IA
        top_results = []
        for idx, score in scores[:5]:
            if idx < len(self.books_data):
                book = self.books_data[idx].copy()
                book['score'] = round(score, 3)
                book['themes'] = self.themes_extracted.get(idx, [])
                top_results.append(book)
        
        # Génération de réponse IA
        ai_response = self.generate_ai_response(query, top_results, user_id, conversation_mode)
        
        return {
            'query': query,
            'results': top_results,
            'ai_response': ai_response,
            'total_found': len([s for s in scores if s[1] > 0.3])
        }
    
    def generate_ai_response(self, query: str, results: List[Dict], 
                           user_id: str = None, conversation_mode: bool = False) -> str:
        """Génère une réponse IA basée sur les résultats"""
        
        if not self.ai_available:
            return "Je ne peux pas générer de réponse IA pour le moment."
        
        # Construction du contexte
        context = "Voici les livres trouvés dans notre bibliothèque :\n\n"
        for i, book in enumerate(results[:3]):
            context += f"{i+1}. {book['title']} par {book['author']}\n"
            context += f"   Genre: {book.get('genre', 'N/A')}\n"
            context += f"   Thèmes: {', '.join(book.get('themes', []))}\n"
            if book.get('description'):
                context += f"   Description: {book['description'][:150]}...\n"
            context += f"   Score de pertinence: {book['score']}\n\n"
        
        # Prompt adaptatif
        if conversation_mode:
            prompt = f"""Tu es un assistant bibliothécaire spécialisé dans la littérature ukrainienne et les livres de l'association "Les Lumières d'Ukraine".

Contexte des livres disponibles :
{context}

Question de l'utilisateur : "{query}"

Réponds de manière conversationnelle et naturelle, comme un vrai bibliothécaire qui connaît bien sa collection. 
Suggère des livres spécifiques, explique pourquoi ils correspondent à la demande, et propose des alternatives si nécessaire.
Sois chaleureux et encourageant dans tes recommandations."""
        else:
            prompt = f"""Tu es un assistant de recherche pour la bibliothèque "Les Lumières d'Ukraine".

Livres trouvés pour la requête "{query}" :
{context}

Génère une réponse structurée qui :
1. Résume les résultats trouvés
2. Explique pourquoi ces livres correspondent à la recherche
3. Suggère des alternatives ou des pistes de recherche
4. Donne des conseils de lecture

Réponse en français, maximum 200 mots."""
        
        return self.call_ollama(prompt)
    
    def generate_book_summary(self, book_id: int) -> str:
        """Génère un résumé automatique d'un livre"""
        if book_id >= len(self.books_data):
            return "Livre non trouvé"
        
        book = self.books_data[book_id]
        
        prompt = f"""Génère un résumé captivant et informatif pour ce livre :

Titre : {book.get('title', 'N/A')}
Auteur : {book.get('author', 'N/A')}
Genre : {book.get('genre', 'N/A')}
Description : {book.get('description', 'N/A')}
Thèmes : {', '.join(self.themes_extracted.get(book_id, []))}

Crée un résumé de 3-4 phrases qui :
- Capture l'essence du livre
- Met en avant ses points forts
- Donne envie de le lire
- Mentionne le public cible

Résumé :"""
        
        return self.call_ollama(prompt)
    
    def generate_recommendations_ai(self, user_id: str = None, 
                                  user_preferences: str = None) -> str:
        """Génère des recommandations personnalisées avec IA"""
        
        # Analyse des préférences
        if user_id and user_id in self.user_history:
            # Analyse de l'historique
            preferred_genres = {}
            preferred_themes = {}
            
            for query, books in self.user_history[user_id].items():
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
Préférences détectées :
- Genres préférés : {', '.join([f'{g} ({c})' for g, c in sorted(preferred_genres.items(), key=lambda x: x[1], reverse=True)[:3]])}
- Thèmes préférés : {', '.join([f'{t} ({c})' for t, c in sorted(preferred_themes.items(), key=lambda x: x[1], reverse=True)[:3]])}
"""
        else:
            preferences_text = "Aucune préférence détectée (nouvel utilisateur)"
        
        # Livres recommandés
        recommendations = self.get_recommendations(user_id)
        
        context = "Livres recommandés :\n"
        for i, book in enumerate(recommendations[:5]):
            context += f"{i+1}. {book['title']} par {book['author']}\n"
            context += f"   Genre: {book.get('genre', 'N/A')}\n"
            context += f"   Thèmes: {', '.join(book.get('themes', []))}\n\n"
        
        prompt = f"""Tu es un bibliothécaire expert qui fait des recommandations personnalisées.

{preferences_text}

{context}

Génère une recommandation personnalisée qui :
1. Explique pourquoi ces livres sont recommandés
2. Met en avant les points forts de chaque livre
3. Suggère un ordre de lecture
4. Propose des alternatives si nécessaire

Réponse en français, style conversationnel et chaleureux."""
        
        return self.call_ollama(prompt)
    
    def compare_books_ai(self, book_ids: List[int]) -> str:
        """Compare des livres avec IA"""
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
        
        context = "Livres à comparer :\n\n"
        for i, book in enumerate(books_info):
            context += f"Livre {i+1} : {book['title']} par {book['author']}\n"
            context += f"Genre : {book['genre']}\n"
            context += f"Thèmes : {', '.join(book['themes'])}\n"
            context += f"Description : {book['description'][:100]}...\n\n"
        
        prompt = f"""Tu es un critique littéraire expert. Compare ces livres de manière détaillée :

{context}

Fais une comparaison structurée qui couvre :
1. Les similitudes entre les livres
2. Les différences principales
3. Les points forts de chaque livre
4. Le public cible de chacun
5. Une recommandation finale

Réponse en français, style critique constructif."""
        
        return self.call_ollama(prompt)
    
    def generate_reading_guide(self, theme: str = None, age_group: str = None) -> str:
        """Génère un guide de lecture avec IA"""
        
        # Sélection des livres
        if theme:
            theme_books = []
            for i, book in enumerate(self.books_data):
                if i in self.themes_extracted and theme in self.themes_extracted[i]:
                    theme_books.append(book)
        else:
            theme_books = self.books_data[:10]  # Top 10 pour l'exemple
        
        context = "Livres sélectionnés :\n"
        for i, book in enumerate(theme_books[:8]):
            context += f"{i+1}. {book['title']} par {book['author']}\n"
            context += f"   Genre: {book.get('genre', 'N/A')}\n"
            context += f"   Thèmes: {', '.join(self.themes_extracted.get(i, []))}\n\n"
        
        prompt = f"""Tu es un bibliothécaire qui crée des guides de lecture.

{context}

Crée un guide de lecture structuré qui inclut :
1. Une introduction au thème/genre
2. Les livres recommandés avec explications
3. Un ordre de lecture suggéré
4. Des conseils pour approfondir
5. Des activités complémentaires

Public cible : {age_group or 'Tous publics'}
Thème : {theme or 'Général'}

Guide de lecture :"""
        
        return self.call_ollama(prompt)
    
    def conversational_search(self, user_id: str, message: str) -> Dict:
        """Recherche conversationnelle avec mémoire"""
        
        # Initialisation de l'historique
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Ajout du message à l'historique
        self.conversation_history[user_id].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Recherche RAG
        search_results = self.search_books_with_ai(message, user_id, conversation_mode=True)
        
        # Génération de réponse conversationnelle
        conversation_context = ""
        if len(self.conversation_history[user_id]) > 1:
            # Prend les 3 derniers messages pour le contexte
            recent_messages = self.conversation_history[user_id][-6:]  # 3 échanges
            conversation_context = "Historique de la conversation :\n"
            for msg in recent_messages[:-1]:  # Exclut le message actuel
                conversation_context += f"{msg['role']}: {msg['content']}\n"
        
        # Prompt conversationnel
        prompt = f"""Tu es un bibliothécaire conversationnel de l'association "Les Lumières d'Ukraine".

{conversation_context}

Question actuelle : "{message}"

Livres trouvés :
{search_results['ai_response']}

Réponds de manière naturelle et conversationnelle, comme un vrai bibliothécaire qui aide un lecteur.
Sois chaleureux, pose des questions de suivi si nécessaire, et guide l'utilisateur dans sa découverte."""
        
        ai_response = self.call_ollama(prompt)
        
        # Ajout de la réponse à l'historique
        self.conversation_history[user_id].append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Limite l'historique à 20 messages
        if len(self.conversation_history[user_id]) > 20:
            self.conversation_history[user_id] = self.conversation_history[user_id][-20:]
        
        return {
            'message': message,
            'ai_response': ai_response,
            'books_found': search_results['results'],
            'conversation_id': len(self.conversation_history[user_id])
        }
    
    def get_recommendations(self, user_id: str = None) -> List[Dict]:
        """Recommandations basées sur l'historique (version simplifiée)"""
        # Simulation de recommandations
        recommendations = []
        for i, book in enumerate(self.books_data[:10]):
            book_copy = book.copy()
            book_copy['score'] = 0.8 - (i * 0.05)
            book_copy['themes'] = self.themes_extracted.get(i, [])
            recommendations.append(book_copy)
        
        return recommendations
    
    def get_statistics(self) -> Dict:
        """Statistiques avec analyse IA"""
        stats = {
            'total_books': len(self.books_data),
            'genres': {},
            'languages': {},
            'cities': {},
            'themes': {},
            'ai_available': self.ai_available
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
    """Interface CLI pour RagTime avec IA"""
    ragtime = RagTimeWithAI()
    
    print("🤖 RagTime with AI - Système RAG + IA pour Les Lumières d'Ukraine")
    print("=" * 70)
    print(f"IA disponible : {'✅' if ragtime.ai_available else '❌'}")
    
    while True:
        print("\nOptions disponibles:")
        print("1. Recherche avec IA")
        print("2. Conversation avec IA")
        print("3. Résumé automatique d'un livre")
        print("4. Recommandations personnalisées avec IA")
        print("5. Comparaison de livres avec IA")
        print("6. Guide de lecture avec IA")
        print("7. Statistiques")
        print("8. Quitter")
        
        choice = input("\nVotre choix (1-8): ").strip()
        
        if choice == '1':
            query = input("Votre recherche: ")
            user_id = input("ID utilisateur (optionnel): ").strip() or None
            
            results = ragtime.search_books_with_ai(query, user_id)
            
            print(f"\n🤖 Réponse IA:")
            print(results['ai_response'])
            
            print(f"\n📚 Livres trouvés ({len(results['results'])}):")
            for book in results['results']:
                print(f"\n- {book['title']} par {book['author']}")
                print(f"  Score: {book['score']} | Thèmes: {', '.join(book.get('themes', []))}")
        
        elif choice == '2':
            user_id = input("ID utilisateur: ")
            print("\n💬 Mode conversation (tapez 'quit' pour sortir)")
            
            while True:
                message = input(f"\nVous: ")
                if message.lower() == 'quit':
                    break
                
                response = ragtime.conversational_search(user_id, message)
                print(f"\nBibliothécaire IA: {response['ai_response']}")
        
        elif choice == '3':
            print("Livres disponibles:")
            for i, book in enumerate(ragtime.books_data[:10]):
                print(f"{i+1}. {book['title']} par {book['author']}")
            
            try:
                book_id = int(input("\nChoisissez un livre (numéro): ")) - 1
                summary = ragtime.generate_book_summary(book_id)
                print(f"\n📖 Résumé généré par IA:")
                print(summary)
            except ValueError:
                print("Numéro invalide")
        
        elif choice == '4':
            user_id = input("ID utilisateur (optionnel): ").strip() or None
            preferences = input("Préférences (optionnel): ").strip() or None
            
            recommendations = ragtime.generate_recommendations_ai(user_id, preferences)
            print(f"\n🎯 Recommandations personnalisées:")
            print(recommendations)
        
        elif choice == '5':
            print("Livres disponibles:")
            for i, book in enumerate(ragtime.books_data[:10]):
                print(f"{i+1}. {book['title']} par {book['author']}")
            
            try:
                book_ids = input("\nChoisissez 2-3 livres (numéros séparés par des virgules): ")
                book_ids = [int(x.strip()) - 1 for x in book_ids.split(',')]
                comparison = ragtime.compare_books_ai(book_ids)
                print(f"\n📊 Comparaison IA:")
                print(comparison)
            except ValueError:
                print("Format invalide")
        
        elif choice == '6':
            theme = input("Thème (optionnel): ").strip() or None
            age_group = input("Groupe d'âge (optionnel): ").strip() or None
            
            guide = ragtime.generate_reading_guide(theme, age_group)
            print(f"\n📚 Guide de lecture:")
            print(guide)
        
        elif choice == '7':
            stats = ragtime.get_statistics()
            
            print("\n📊 Statistiques:")
            print(f"Total de livres: {stats['total_books']}")
            print(f"IA disponible: {'Oui' if stats['ai_available'] else 'Non'}")
            
            print("\nGenres populaires:")
            for genre, count in sorted(stats['genres'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {genre}: {count}")
        
        elif choice == '8':
            print("Au revoir ! 👋")
            break
        
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main() 