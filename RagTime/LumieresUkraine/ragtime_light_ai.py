#!/usr/bin/env python3
"""
RagTime Light AI - Système RAG avec IA légère optimisée
Utilise des modèles Ollama légers spécialement adaptés pour le RAG
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

class RagTimeLightAI:
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
        
        # Modèles IA légers recommandés pour RAG
        self.light_models = {
            "phi2": "microsoft/phi-2:2.7b",  # 2.7B paramètres, excellent pour RAG
            "qwen2": "qwen/qwen2.5:0.5b",     # 0.5B paramètres, très rapide
            "gemma2": "google/gemma2:2b",     # 2B paramètres, optimisé Google
            "llama2": "llama2:7b",            # 7B paramètres, bon équilibre
            "mistral": "mistral:7b"           # 7B paramètres, bonne qualité
        }
        
        self.current_model = "phi2"  # Modèle par défaut (le plus léger)
        
        self.load_data()
        self.extract_themes()
        self.check_ollama_connection()
    
    def check_ollama_connection(self):
        """Vérifie la connexion à Ollama et les modèles disponibles"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = []
                
                for model_name, model_id in self.light_models.items():
                    if any(model_id.split(':')[0] in model['name'] for model in models):
                        available_models.append(model_name)
                
                if available_models:
                    print(f"✅ Ollama connecté - Modèles disponibles: {', '.join(available_models)}")
                    self.ai_available = True
                    self.available_models = available_models
                    
                    # Choisir le modèle le plus léger disponible
                    priority_models = ["qwen2", "phi2", "gemma2", "llama2", "mistral"]
                    for model in priority_models:
                        if model in available_models:
                            self.current_model = model
                            print(f"🎯 Modèle sélectionné: {model} ({self.light_models[model]})")
                            break
                else:
                    print("⚠️ Ollama connecté mais aucun modèle léger trouvé")
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
    
    def call_ollama_light(self, prompt: str, max_tokens: int = 200) -> str:
        """Appelle Ollama avec un modèle léger optimisé pour RAG"""
        if not self.ai_available:
            return "IA non disponible"
        
        try:
            # Prompt optimisé pour les modèles légers
            optimized_prompt = self.optimize_prompt_for_light_model(prompt)
            
            payload = {
                "model": self.light_models[self.current_model],
                "prompt": optimized_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Plus bas pour plus de cohérence
                    "top_p": 0.8,
                    "max_tokens": max_tokens,
                    "num_ctx": 2048,  # Contexte limité pour les modèles légers
                    "repeat_penalty": 1.1
                }
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", 
                                   json=payload, timeout=15)  # Timeout réduit
            
            if response.status_code == 200:
                return response.json().get('response', 'Erreur de réponse')
            else:
                return f"Erreur HTTP: {response.status_code}"
                
        except Exception as e:
            return f"Erreur Ollama: {str(e)}"
    
    def optimize_prompt_for_light_model(self, prompt: str) -> str:
        """Optimise le prompt pour les modèles légers"""
        # Règles d'optimisation pour modèles légers
        optimizations = [
            ("Tu es un", "Tu es"),
            ("assistant bibliothécaire", "bibliothécaire"),
            ("spécialisé dans", "qui connaît"),
            ("littérature ukrainienne", "livres ukrainiens"),
            ("association Les Lumières d'Ukraine", "bibliothèque"),
            ("Réponds de manière", "Réponds"),
            ("conversationnelle et naturelle", "simplement"),
            ("comme un vrai bibliothécaire", "comme un expert"),
            ("qui connaît bien sa collection", "qui aide"),
            ("Suggère des livres spécifiques", "Suggère des livres"),
            ("explique pourquoi ils correspondent", "explique pourquoi"),
            ("propose des alternatives si nécessaire", "propose d'autres choix")
        ]
        
        optimized = prompt
        for old, new in optimizations:
            optimized = optimized.replace(old, new)
        
        # Limite la longueur du prompt
        if len(optimized) > 1000:
            optimized = optimized[:1000] + "..."
        
        return optimized
    
    def search_books_with_light_ai(self, query: str, user_id: str = None) -> Dict:
        """Recherche avec IA légère optimisée"""
        
        # Recherche RAG classique (rapide)
        query_embedding = self.model.encode([query])[0]
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        
        # Tri des résultats
        scores = [(i, sim) for i, sim in enumerate(similarities)]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Top résultats pour l'IA
        top_results = []
        for idx, score in scores[:3]:  # Limité à 3 pour les modèles légers
            if idx < len(self.books_data):
                book = self.books_data[idx].copy()
                book['score'] = round(score, 3)
                book['themes'] = self.themes_extracted.get(idx, [])
                top_results.append(book)
        
        # Génération de réponse IA légère
        ai_response = self.generate_light_ai_response(query, top_results)
        
        return {
            'query': query,
            'results': top_results,
            'ai_response': ai_response,
            'model_used': self.current_model,
            'total_found': len([s for s in scores if s[1] > 0.3])
        }
    
    def generate_light_ai_response(self, query: str, results: List[Dict]) -> str:
        """Génère une réponse IA légère basée sur les résultats"""
        
        if not self.ai_available:
            return "Je ne peux pas générer de réponse IA pour le moment."
        
        # Contexte simplifié pour modèles légers
        context = "Livres trouvés:\n"
        for i, book in enumerate(results):
            context += f"{i+1}. {book['title']} par {book['author']}\n"
            context += f"   Genre: {book.get('genre', 'N/A')}\n"
            if book.get('description'):
                context += f"   {book['description'][:80]}...\n"
        
        # Prompt court et direct pour modèles légers
        prompt = f"""Tu es un bibliothécaire qui aide à trouver des livres.

{context}

Question: "{query}"

Réponds brièvement (2-3 phrases) en suggérant les meilleurs livres et pourquoi ils correspondent."""
        
        return self.call_ollama_light(prompt, max_tokens=150)
    
    def generate_quick_summary(self, book_id: int) -> str:
        """Génère un résumé rapide avec IA légère"""
        if book_id >= len(self.books_data):
            return "Livre non trouvé"
        
        book = self.books_data[book_id]
        
        prompt = f"""Résume ce livre en 2 phrases:

Titre: {book.get('title', 'N/A')}
Auteur: {book.get('author', 'N/A')}
Genre: {book.get('genre', 'N/A')}
Description: {book.get('description', 'N/A')[:200]}

Résumé:"""
        
        return self.call_ollama_light(prompt, max_tokens=100)
    
    def get_light_recommendations(self, user_id: str = None) -> str:
        """Recommandations avec IA légère"""
        
        # Livres populaires
        recommendations = self.get_popular_books()
        
        context = "Livres recommandés:\n"
        for i, book in enumerate(recommendations[:3]):
            context += f"{i+1}. {book['title']} par {book['author']}\n"
            context += f"   Genre: {book.get('genre', 'N/A')}\n"
        
        prompt = f"""Tu es un bibliothécaire qui fait des recommandations.

{context}

Suggère ces livres en 2-3 phrases simples."""
        
        return self.call_ollama_light(prompt, max_tokens=120)
    
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
    
    def switch_model(self, model_name: str) -> bool:
        """Change de modèle IA"""
        if model_name in self.available_models:
            self.current_model = model_name
            print(f"✅ Modèle changé vers: {model_name}")
            return True
        else:
            print(f"❌ Modèle {model_name} non disponible")
            return False
    
    def get_model_info(self) -> Dict:
        """Retourne les informations sur le modèle actuel"""
        return {
            "current_model": self.current_model,
            "model_id": self.light_models[self.current_model],
            "available_models": self.available_models,
            "ai_available": self.ai_available
        }
    
    def get_statistics(self) -> Dict:
        """Statistiques avec info modèle"""
        stats = {
            'total_books': len(self.books_data),
            'genres': {},
            'languages': {},
            'cities': {},
            'themes': {},
            'ai_model': self.current_model,
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
    """Interface CLI pour RagTime Light AI"""
    ragtime = RagTimeLightAI()
    
    print("⚡ RagTime Light AI - Système RAG avec IA légère")
    print("=" * 60)
    print(f"🤖 Modèle IA: {ragtime.current_model}")
    print(f"📚 Livres indexés: {len(ragtime.books_data)}")
    
    while True:
        print("\nOptions disponibles:")
        print("1. Recherche avec IA légère")
        print("2. Résumé rapide d'un livre")
        print("3. Recommandations IA")
        print("4. Changer de modèle IA")
        print("5. Informations modèle")
        print("6. Statistiques")
        print("7. Quitter")
        
        choice = input("\nVotre choix (1-7): ").strip()
        
        if choice == '1':
            query = input("Votre recherche: ")
            results = ragtime.search_books_with_light_ai(query)
            
            print(f"\n🤖 Réponse IA ({results['model_used']}):")
            print(results['ai_response'])
            
            print(f"\n📚 Livres trouvés ({len(results['results'])}):")
            for book in results['results']:
                print(f"\n- {book['title']} par {book['author']}")
                print(f"  Score: {book['score']} | Thèmes: {', '.join(book.get('themes', []))}")
        
        elif choice == '2':
            print("Livres disponibles:")
            for i, book in enumerate(ragtime.books_data[:10]):
                print(f"{i+1}. {book['title']} par {book['author']}")
            
            try:
                book_id = int(input("\nChoisissez un livre (numéro): ")) - 1
                summary = ragtime.generate_quick_summary(book_id)
                print(f"\n📖 Résumé IA:")
                print(summary)
            except ValueError:
                print("Numéro invalide")
        
        elif choice == '3':
            recommendations = ragtime.get_light_recommendations()
            print(f"\n🎯 Recommandations IA:")
            print(recommendations)
        
        elif choice == '4':
            print("Modèles disponibles:")
            for i, model in enumerate(ragtime.available_models):
                print(f"{i+1}. {model} - {ragtime.light_models[model]}")
            
            model_name = input("\nChoisissez un modèle: ").strip()
            ragtime.switch_model(model_name)
        
        elif choice == '5':
            info = ragtime.get_model_info()
            print(f"\n🤖 Informations modèle:")
            print(f"   Modèle actuel: {info['current_model']}")
            print(f"   ID modèle: {info['model_id']}")
            print(f"   IA disponible: {'Oui' if info['ai_available'] else 'Non'}")
            print(f"   Modèles disponibles: {', '.join(info['available_models'])}")
        
        elif choice == '6':
            stats = ragtime.get_statistics()
            
            print("\n📊 Statistiques:")
            print(f"Total de livres: {stats['total_books']}")
            print(f"Modèle IA: {stats['ai_model']}")
            print(f"IA disponible: {'Oui' if stats['ai_available'] else 'Non'}")
            
            print("\nGenres populaires:")
            for genre, count in sorted(stats['genres'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {genre}: {count}")
        
        elif choice == '7':
            print("Au revoir ! 👋")
            break
        
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main() 