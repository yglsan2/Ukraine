#!/usr/bin/env python3
"""
RagTime Enhanced - Système RAG spécialisé pour les livres des Lumières d'Ukraine
Version avancée avec recherche contextuelle, filtres intelligents et recommandations
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

class RagTimeEnhanced:
    def __init__(self, index_path: str = "books_index.pkl", data_path: str = "books_data.json"):
        self.index_path = index_path
        self.data_path = data_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.books_data = []
        self.embeddings = []
        self.concepts = []
        self.user_history = {}  # Historique des utilisateurs
        self.themes_extracted = {}  # Thèmes extraits par livre
        
        self.load_data()
        self.extract_themes()
    
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
    
    def search_books(self, query: str, filters: Dict = None, user_id: str = None, 
                    max_results: int = 10) -> List[Dict]:
        """Recherche avancée avec filtres et contexte utilisateur"""
        
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
        # Détection du type de recherche
        query_lower = query.lower()
        
        # Recherche par âge
        age_patterns = {
            'enfant': ['enfant', 'petit', 'jeune', 'bébé', '3-6 ans', '6-9 ans'],
            'adolescent': ['ado', 'adolescent', 'jeune', '12-15 ans', '15-18 ans'],
            'adulte': ['adulte', 'grand', 'mature']
        }
        
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
    
    def get_recommendations(self, user_id: str = None, filters: Dict = None) -> List[Dict]:
        """Génère des recommandations personnalisées"""
        if not user_id or user_id not in self.user_history:
            # Recommandations générales basées sur la popularité
            return self.get_popular_books(filters)
        
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
    
    def get_popular_books(self, filters: Dict = None) -> List[Dict]:
        """Retourne les livres populaires"""
        # Simulation de popularité basée sur les scores de similarité
        dummy_query = "livre populaire intéressant"
        query_embedding = self.model.encode([dummy_query])[0]
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        
        scores = [(i, sim) for i, sim in enumerate(similarities)]
        filtered_scores = self.apply_filters(scores, filters)
        
        return self.format_results(filtered_scores, 10)
    
    def get_books_by_theme(self, theme: str) -> List[Dict]:
        """Retourne tous les livres d'un thème donné"""
        theme_books = []
        
        for i, book in enumerate(self.books_data):
            if i in self.themes_extracted and theme in self.themes_extracted[i]:
                theme_books.append((i, 1.0))  # Score parfait pour les thèmes exacts
        
        return self.format_results(theme_books, 50)
    
    def get_books_by_genre(self, genre: str) -> List[Dict]:
        """Retourne tous les livres d'un genre donné"""
        genre_books = []
        
        for i, book in enumerate(self.books_data):
            if book.get('genre', '').lower() == genre.lower():
                genre_books.append((i, 1.0))
        
        return self.format_results(genre_books, 50)
    
    def get_books_by_city(self, city: str) -> List[Dict]:
        """Retourne tous les livres disponibles dans une ville"""
        city_books = []
        
        for i, book in enumerate(self.books_data):
            if book.get('city', '').lower() == city.lower():
                city_books.append((i, 1.0))
        
        return self.format_results(city_books, 50)
    
    def get_statistics(self) -> Dict:
        """Retourne des statistiques sur la bibliothèque"""
        stats = {
            'total_books': len(self.books_data),
            'genres': {},
            'languages': {},
            'cities': {},
            'themes': {},
            'status': {}
        }
        
        for book in self.books_data:
            # Genres
            genre = book.get('genre', 'Inconnu')
            stats['genres'][genre] = stats['genres'].get(genre, 0) + 1
            
            # Langues
            language = book.get('language', 'Inconnu')
            stats['languages'][language] = stats['languages'].get(language, 0) + 1
            
            # Villes
            city = book.get('city', 'Inconnu')
            stats['cities'][city] = stats['cities'].get(city, 0) + 1
            
            # Statuts
            status = book.get('status', 'Inconnu')
            stats['status'][status] = stats['status'].get(status, 0) + 1
        
        # Thèmes
        for themes in self.themes_extracted.values():
            for theme in themes:
                stats['themes'][theme] = stats['themes'].get(theme, 0) + 1
        
        return stats

def main():
    """Interface CLI pour RagTime Enhanced"""
    ragtime = RagTimeEnhanced()
    
    print("🌟 RagTime Enhanced - Système RAG pour Les Lumières d'Ukraine")
    print("=" * 60)
    
    while True:
        print("\nOptions disponibles:")
        print("1. Recherche de livres")
        print("2. Recommandations personnalisées")
        print("3. Livres par thème")
        print("4. Livres par genre")
        print("5. Livres par ville")
        print("6. Statistiques")
        print("7. Quitter")
        
        choice = input("\nVotre choix (1-7): ").strip()
        
        if choice == '1':
            query = input("Votre recherche: ")
            user_id = input("ID utilisateur (optionnel): ").strip() or None
            
            # Filtres optionnels
            filters = {}
            apply_filters = input("Appliquer des filtres ? (o/n): ").lower() == 'o'
            
            if apply_filters:
                genre = input("Genre (optionnel): ").strip()
                if genre:
                    filters['genre'] = genre
                
                language = input("Langue (optionnel): ").strip()
                if language:
                    filters['language'] = language
                
                city = input("Ville (optionnel): ").strip()
                if city:
                    filters['city'] = city
                
                status = input("Statut (disponible/emprunté, optionnel): ").strip()
                if status:
                    filters['status'] = status
            
            results = ragtime.search_books(query, filters, user_id)
            
            print(f"\n📚 Résultats ({len(results)} livres trouvés):")
            for book in results:
                print(f"\n{book['rank']}. {book['title']} - {book['author']}")
                print(f"   Genre: {book.get('genre', 'N/A')} | Langue: {book.get('language', 'N/A')}")
                print(f"   Ville: {book.get('city', 'N/A')} | Statut: {book.get('status', 'N/A')}")
                print(f"   Score: {book['score']}")
                if 'themes' in book:
                    print(f"   Thèmes: {', '.join(book['themes'])}")
                if book.get('description'):
                    print(f"   Description: {book['description'][:100]}...")
        
        elif choice == '2':
            user_id = input("ID utilisateur: ")
            results = ragtime.get_recommendations(user_id)
            
            print(f"\n🎯 Recommandations personnalisées ({len(results)} livres):")
            for book in results:
                print(f"\n{book['rank']}. {book['title']} - {book['author']}")
                print(f"   Score: {book['score']}")
        
        elif choice == '3':
            print("Thèmes disponibles:")
            themes = set()
            for book_themes in ragtime.themes_extracted.values():
                themes.update(book_themes)
            
            for theme in sorted(themes):
                print(f"- {theme}")
            
            theme = input("\nChoisissez un thème: ")
            results = ragtime.get_books_by_theme(theme)
            
            print(f"\n📖 Livres sur le thème '{theme}' ({len(results)} livres):")
            for book in results:
                print(f"- {book['title']} - {book['author']}")
        
        elif choice == '4':
            print("Genres disponibles:")
            genres = set(book.get('genre', '') for book in ragtime.books_data if book.get('genre'))
            
            for genre in sorted(genres):
                print(f"- {genre}")
            
            genre = input("\nChoisissez un genre: ")
            results = ragtime.get_books_by_genre(genre)
            
            print(f"\n📚 Livres du genre '{genre}' ({len(results)} livres):")
            for book in results:
                print(f"- {book['title']} - {book['author']}")
        
        elif choice == '5':
            print("Villes disponibles:")
            cities = set(book.get('city', '') for book in ragtime.books_data if book.get('city'))
            
            for city in sorted(cities):
                print(f"- {city}")
            
            city = input("\nChoisissez une ville: ")
            results = ragtime.get_books_by_city(city)
            
            print(f"\n🏙️ Livres disponibles à '{city}' ({len(results)} livres):")
            for book in results:
                print(f"- {book['title']} - {book['author']}")
        
        elif choice == '6':
            stats = ragtime.get_statistics()
            
            print("\n📊 Statistiques de la bibliothèque:")
            print(f"Total de livres: {stats['total_books']}")
            
            print("\nGenres:")
            for genre, count in sorted(stats['genres'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {genre}: {count}")
            
            print("\nLangues:")
            for lang, count in sorted(stats['languages'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {lang}: {count}")
            
            print("\nVilles:")
            for city, count in sorted(stats['cities'].items(), key=lambda x: x[1], reverse=True):
                print(f"  {city}: {count}")
            
            print("\nThèmes populaires:")
            for theme, count in sorted(stats['themes'].items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  {theme}: {count}")
        
        elif choice == '7':
            print("Au revoir ! 👋")
            break
        
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main() 