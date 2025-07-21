#!/usr/bin/env python3
"""
RagTime Hybrid Smart - Système RAG optimisé avec IA légère sélective
Utilise RAG pur pour la recherche rapide, IA légère seulement pour les résumés
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

class RagTimeHybridSmart:
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
        self.book_summaries = {}  # Cache des résumés
        
        # Modèles IA légers pour résumés seulement
        self.light_models = {
            "qwen2": "qwen2.5:0.5b",      # Ultra-rapide pour résumés
            "phi2": "phi:2.7b",           # Bon français, rapide
            "gemma2": "gemma2:2b",        # Google, équilibré
            "mistral": "mistral:7b-instruct"  # Qualité max, plus lent
        }
        
        self.current_model = "qwen2"  # Modèle le plus rapide par défaut
        self.ai_available = False
        
        self.load_data()
        self.extract_themes()
        self.check_ai_availability()
    
    def check_ai_availability(self):
        """Vérifie la disponibilité des modèles IA légers"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = []
                
                for model_name, model_id in self.light_models.items():
                    if any(model_id.split(':')[0] in model['name'] for model in models):
                        available_models.append(model_name)
                
                if available_models:
                    print(f"✅ IA disponible - Modèles: {', '.join(available_models)}")
                    self.ai_available = True
                    self.available_models = available_models
                    
                    # Choisir le plus rapide disponible
                    priority_models = ["qwen2", "phi2", "gemma2", "mistral"]
                    for model in priority_models:
                        if model in available_models:
                            self.current_model = model
                            print(f"⚡ Modèle sélectionné: {model} (rapide)")
                            break
                else:
                    print("⚠️ Aucun modèle IA léger trouvé")
                    self.ai_available = False
            else:
                print("❌ Ollama non disponible")
                self.ai_available = False
        except Exception as e:
            print(f"❌ Erreur IA: {e}")
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
    
    def search_books_fast(self, query: str, filters: Dict = None, user_id: str = None, 
                         max_results: int = 10) -> List[Dict]:
        """Recherche RAG pure - RAPIDE (< 100ms)"""
        
        # Prétraitement de la requête
        query_clean = self.preprocess_query(query)
        
        # Génération de l'embedding de la requête
        query_embedding = self.model.encode([query_clean])[0]
        
        # Calcul des similarités
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        
        # Score hybride avec concepts
        hybrid_scores = self.calculate_hybrid_score(query_clean, similarities)
        
        # Application des filtres
        filtered_results = self.apply_filters(hybrid_scores, filters)
        
        # Personnalisation basée sur l'historique utilisateur
        if user_id and user_id in self.user_history:
            filtered_results = self.personalize_results(filtered_results, user_id)
        
        # Tri et formatage des résultats
        results = self.format_results(filtered_results, max_results)
        
        # Mise à jour de l'historique utilisateur
        if user_id:
            self.update_user_history(user_id, query, results[:3])
        
        return results
    
    def preprocess_query(self, query: str) -> str:
        """Prétraitement intelligent de la requête"""
        query_lower = query.lower()
        
        # Recherche par disponibilité
        if 'disponible' in query_lower or 'dispo' in query_lower:
            query += " status:available"
        
        # Recherche par ville
        city_match = re.search(r'à (\w+)', query_lower)
        if city_match:
            city = city_match.group(1)
            query += f" city:{city}"
        
        return query
    
    def calculate_hybrid_score(self, query: str, similarities: np.ndarray) -> List[Tuple[int, float]]:
        """Calcul du score hybride combinant similarité sémantique et concepts"""
        scores = []
        
        for i, similarity in enumerate(similarities):
            # Score de base
            score = similarity
            
            # Bonus pour les concepts
            if i < len(self.concepts):
                concept_bonus = self.calculate_concept_bonus(query, self.concepts[i])
                score += concept_bonus * 0.3
            
            # Bonus pour les thèmes
            if i in self.themes_extracted:
                theme_bonus = self.calculate_theme_bonus(query, self.themes_extracted[i])
                score += theme_bonus * 0.2
            
            scores.append((i, score))
        
        return scores
    
    def calculate_concept_bonus(self, query: str, concepts: List[str]) -> float:
        """Calcule le bonus pour les concepts"""
        query_words = set(query.lower().split())
        concept_words = set()
        
        for concept in concepts:
            concept_words.update(concept.lower().split())
        
        intersection = query_words.intersection(concept_words)
        return len(intersection) / max(len(query_words), 1)
    
    def calculate_theme_bonus(self, query: str, themes: List[str]) -> float:
        """Calcule le bonus pour les thèmes"""
        query_lower = query.lower()
        theme_matches = sum(1 for theme in themes if theme in query_lower)
        return theme_matches / max(len(themes), 1)
    
    def apply_filters(self, scores: List[Tuple[int, float]], filters: Dict = None) -> List[Tuple[int, float]]:
        """Applique les filtres aux résultats"""
        if not filters:
            return scores
        
        filtered_scores = []
        
        for idx, score in scores:
            if idx >= len(self.books_data):
                continue
            
            book = self.books_data[idx]
            include = True
            
            # Filtre par genre
            if 'genre' in filters and book.get('genre') != filters['genre']:
                include = False
            
            # Filtre par langue
            if 'language' in filters and book.get('language') != filters['language']:
                include = False
            
            # Filtre par ville
            if 'city' in filters and book.get('city') != filters['city']:
                include = False
            
            # Filtre par statut
            if 'status' in filters and book.get('status') != filters['status']:
                include = False
            
            # Filtre par thème
            if 'theme' in filters and idx in self.themes_extracted:
                if filters['theme'] not in self.themes_extracted[idx]:
                    include = False
            
            if include:
                filtered_scores.append((idx, score))
        
        return filtered_scores
    
    def personalize_results(self, results: List[Tuple[int, float]], user_id: str) -> List[Tuple[int, float]]:
        """Personnalise les résultats basé sur l'historique utilisateur"""
        user_history = self.user_history[user_id]
        
        # Analyse des préférences
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
        
        # Application des préférences
        personalized_results = []
        for idx, score in results:
            bonus = 0
            
            if idx < len(self.books_data):
                book = self.books_data[idx]
                genre = book.get('genre', '')
                
                # Bonus pour genre préféré
                if genre in preferred_genres:
                    bonus += 0.1 * preferred_genres[genre]
                
                # Bonus pour thèmes préférés
                if idx in self.themes_extracted:
                    for theme in self.themes_extracted[idx]:
                        if theme in preferred_themes:
                            bonus += 0.05 * preferred_themes[theme]
            
            personalized_results.append((idx, score + bonus))
        
        # Retri par score personnalisé
        personalized_results.sort(key=lambda x: x[1], reverse=True)
        return personalized_results
    
    def format_results(self, results: List[Tuple[int, float]], max_results: int) -> List[Dict]:
        """Formate les résultats pour l'affichage"""
        formatted_results = []
        
        for i, (idx, score) in enumerate(results[:max_results]):
            if idx >= len(self.books_data):
                continue
            
            book = self.books_data[idx].copy()
            book['score'] = round(score, 3)
            book['rank'] = i + 1
            
            # Ajout des thèmes
            if idx in self.themes_extracted:
                book['themes'] = self.themes_extracted[idx]
            
            # Ajout des concepts
            if idx < len(self.concepts):
                book['concepts'] = self.concepts[idx][:5]  # Top 5 concepts
            
            formatted_results.append(book)
        
        return formatted_results
    
    def update_user_history(self, user_id: str, query: str, results: List[Dict]):
        """Met à jour l'historique utilisateur"""
        if user_id not in self.user_history:
            self.user_history[user_id] = {}
        
        # Garde seulement les 10 dernières requêtes
        if len(self.user_history[user_id]) >= 10:
            oldest_query = min(self.user_history[user_id].keys())
            del self.user_history[user_id][oldest_query]
        
        # Ajoute les livres consultés
        book_indices = [book.get('id', i) for i, book in enumerate(results)]
        self.user_history[user_id][query] = book_indices
    
    def generate_summary_light(self, book_id: int, style: str = "bref") -> str:
        """Génère un résumé avec IA légère - OPTIMISÉ POUR RAPIDITÉ"""
        if book_id >= len(self.books_data):
            return "Livre non trouvé"
        
        # Vérifier le cache
        cache_key = f"{book_id}_{style}"
        if cache_key in self.book_summaries:
            return self.book_summaries[cache_key]
        
        if not self.ai_available:
            return self.generate_summary_fallback(book_id, style)
        
        book = self.books_data[book_id]
        
        # Prompts optimisés pour modèles légers
        style_prompts = {
            "bref": "Résume en 2 phrases:",
            "standard": "Résume brièvement:",
            "littéraire": "Résume avec style:",
            "critique": "Analyse rapidement:",
            "détaillé": "Résume en détail:"
        }
        
        style_prompt = style_prompts.get(style, style_prompts["bref"])
        
        # Prompt ultra-court pour rapidité
        prompt = f"""{style_prompt}

Titre: {book.get('title', 'N/A')}
Auteur: {book.get('author', 'N/A')}
Genre: {book.get('genre', 'N/A')}
Description: {book.get('description', 'N/A')[:150]}

Résumé:"""
        
        try:
            payload = {
                "model": self.light_models[self.current_model],
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.8,
                    "max_tokens": 150,  # Limité pour rapidité
                    "num_ctx": 1024,    # Contexte réduit
                    "repeat_penalty": 1.1
                }
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", 
                                   json=payload, timeout=10)  # Timeout court
            
            if response.status_code == 200:
                summary = response.json().get('response', 'Erreur de réponse')
                # Mise en cache
                self.book_summaries[cache_key] = summary
                return summary
            else:
                return self.generate_summary_fallback(book_id, style)
                
        except Exception as e:
            return self.generate_summary_fallback(book_id, style)
    
    def generate_summary_fallback(self, book_id: int, style: str) -> str:
        """Génère un résumé sans IA - Fallback intelligent"""
        book = self.books_data[book_id]
        
        # Extraction intelligente de phrases clés
        description = book.get('description', '')
        title = book.get('title', '')
        author = book.get('author', '')
        genre = book.get('genre', '')
        themes = self.themes_extracted.get(book_id, [])
        
        # Construction du résumé
        summary_parts = []
        
        if title and author:
            summary_parts.append(f"« {title} » par {author}")
        
        if genre:
            summary_parts.append(f"Genre : {genre}")
        
        if themes:
            summary_parts.append(f"Thèmes : {', '.join(themes[:3])}")
        
        if description:
            # Prend les premières phrases significatives
            sentences = description.split('.')[:2]
            summary_parts.append(' '.join(sentences) + '.')
        
        if style == "bref":
            return ' | '.join(summary_parts[:2])
        elif style == "standard":
            return ' | '.join(summary_parts)
        elif style == "littéraire":
            return f"Une œuvre captivante : {summary_parts[0] if summary_parts else ''}"
        elif style == "critique":
            return f"Analyse : {summary_parts[0] if summary_parts else ''}"
        else:
            return ' | '.join(summary_parts)
    
    def get_recommendations(self, user_id: str = None) -> List[Dict]:
        """Recommandations basées sur l'historique (RAG pur)"""
        if not user_id or user_id not in self.user_history:
            # Recommandations générales basées sur la popularité
            return self.get_popular_books()
        
        # Recommandations basées sur l'historique
        user_history = self.user_history[user_id]
        
        # Analyse des préférences
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
        
        # Trouve des livres similaires
        recommendations = []
        for i, book in enumerate(self.books_data):
            if i in [idx for books in user_history.values() for idx in books]:
                continue  # Skip déjà consultés
            
            score = 0
            genre = book.get('genre', '')
            
            if genre in preferred_genres:
                score += preferred_genres[genre] * 0.5
            
            if i in self.themes_extracted:
                for theme in self.themes_extracted[i]:
                    if theme in preferred_themes:
                        score += preferred_themes[theme] * 0.3
            
            if score > 0:
                recommendations.append((i, score))
        
        # Tri et formatage
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return self.format_results(recommendations, 10)
    
    def get_popular_books(self) -> List[Dict]:
        """Retourne les livres populaires"""
        dummy_query = "livre populaire intéressant"
        query_embedding = self.model.encode([dummy_query])[0]
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        
        scores = [(i, sim) for i, sim in enumerate(similarities)]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return self.format_results(scores, 10)
    
    def switch_model(self, model_name: str) -> bool:
        """Change de modèle IA"""
        if model_name in self.available_models:
            self.current_model = model_name
            print(f"✅ Modèle changé vers: {model_name}")
            return True
        else:
            print(f"❌ Modèle {model_name} non disponible")
            return False
    
    def get_statistics(self) -> Dict:
        """Statistiques avec info modèle"""
        stats = {
            'total_books': len(self.books_data),
            'genres': {},
            'languages': {},
            'cities': {},
            'themes': {},
            'ai_model': self.current_model,
            'ai_available': self.ai_available,
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
    """Interface CLI pour RagTime Hybrid Smart"""
    ragtime = RagTimeHybridSmart()
    
    print("⚡ RagTime Hybrid Smart - RAG rapide + IA légère sélective")
    print("=" * 60)
    print(f"🤖 Modèle IA: {ragtime.current_model}")
    print(f"📚 Livres indexés: {len(ragtime.books_data)}")
    print(f"✅ IA disponible: {'Oui' if ragtime.ai_available else 'Non'}")
    
    while True:
        print("\nOptions disponibles:")
        print("1. Recherche RAPIDE (RAG pur)")
        print("2. Résumé IA LÉGER (avec fallback)")
        print("3. Recommandations personnalisées")
        print("4. Changer de modèle IA")
        print("5. Statistiques")
        print("6. Quitter")
        
        choice = input("\nVotre choix (1-6): ").strip()
        
        if choice == '1':
            query = input("Votre recherche: ")
            start_time = time.time()
            results = ragtime.search_books_fast(query)
            search_time = time.time() - start_time
            
            print(f"\n⚡ Recherche terminée en {search_time:.3f}s")
            print(f"📚 Livres trouvés ({len(results)}):")
            for book in results:
                print(f"\n- {book['title']} par {book['author']}")
                print(f"  Score: {book['score']} | Thèmes: {', '.join(book.get('themes', []))}")
        
        elif choice == '2':
            print("Livres disponibles:")
            for i, book in enumerate(ragtime.books_data[:10]):
                print(f"{i+1}. {book['title']} par {book['author']}")
            
            try:
                book_id = int(input("\nChoisissez un livre (numéro): ")) - 1
                print("\nStyles de résumé:")
                styles = ["bref", "standard", "littéraire", "critique", "détaillé"]
                for i, style in enumerate(styles):
                    print(f"{i+1}. {style}")
                
                style_choice = input("\nChoisissez un style (numéro): ").strip()
                style = styles[int(style_choice) - 1] if style_choice.isdigit() and 1 <= int(style_choice) <= len(styles) else "bref"
                
                start_time = time.time()
                summary = ragtime.generate_summary_light(book_id, style)
                summary_time = time.time() - start_time
                
                print(f"\n📖 Résumé ({style}) - {summary_time:.2f}s:")
                print(summary)
            except (ValueError, IndexError):
                print("Choix invalide")
        
        elif choice == '3':
            user_id = input("ID utilisateur (optionnel): ").strip() or None
            results = ragtime.get_recommendations(user_id)
            
            print(f"\n🎯 Recommandations ({len(results)} livres):")
            for book in results:
                print(f"\n- {book['title']} par {book['author']}")
                print(f"  Score: {book['score']}")
        
        elif choice == '4':
            print("Modèles disponibles:")
            for i, model in enumerate(ragtime.available_models):
                print(f"{i+1}. {model} - {ragtime.light_models[model]}")
            
            model_name = input("\nChoisissez un modèle: ").strip()
            ragtime.switch_model(model_name)
        
        elif choice == '5':
            stats = ragtime.get_statistics()
            
            print("\n📊 Statistiques:")
            print(f"Total de livres: {stats['total_books']}")
            print(f"Modèle IA: {stats['ai_model']}")
            print(f"IA disponible: {'Oui' if stats['ai_available'] else 'Non'}")
            print(f"Résumés en cache: {stats['cached_summaries']}")
            
            print("\nGenres populaires:")
            for genre, count in sorted(stats['genres'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {genre}: {count}")
        
        elif choice == '6':
            print("Au revoir ! 👋")
            break
        
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main() 