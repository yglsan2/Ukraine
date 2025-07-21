#!/usr/bin/env python3
"""
RagTime Chatbot - Système de chat intelligent avec IA optionnelle
Utilise RagTime de base + IA optionnelle selon la configuration
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

class RagTimeChatbot:
    def __init__(self, index_path: str = "books_index.pkl", data_path: str = "books_data.json", 
                 summaries_path: str = "smart_summaries.json",
                 ollama_url: str = "http://localhost:11434"):
        self.index_path = index_path
        self.data_path = data_path
        self.summaries_path = summaries_path
        self.ollama_url = ollama_url
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.books_data = []
        self.embeddings = []
        self.concepts = []
        self.user_history = {}
        self.themes_extracted = {}
        self.book_summaries = {}
        self.conversation_history = {}
        
        # Configuration IA
        self.ai_config = {
            "enabled": False,
            "model": None,
            "available_models": [],
            "performance_mode": "fast"  # fast, balanced, quality
        }
        
        # Modèles IA légers recommandés
        self.light_models = {
            "qwen2": {
                "id": "qwen2.5:0.5b",
                "size": "0.5B",
                "ram": "2GB",
                "speed": "ultra-fast",
                "french": 3,
                "summaries": 3
            },
            "phi2": {
                "id": "phi:2.7b",
                "size": "2.7B",
                "ram": "4GB",
                "speed": "fast",
                "french": 4,
                "summaries": 4
            },
            "gemma2": {
                "id": "gemma2:2b",
                "size": "2B",
                "ram": "3GB",
                "speed": "fast",
                "french": 4,
                "summaries": 3
            },
            "mistral": {
                "id": "mistral:7b-instruct",
                "size": "7B",
                "ram": "8GB",
                "speed": "medium",
                "french": 5,
                "summaries": 5
            }
        }
        
        self.load_data()
        self.extract_themes()
        self.load_summaries()
        self.check_ai_availability()
    
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
    
    def load_summaries(self):
        """Charge les résumés pré-générés"""
        if os.path.exists(self.summaries_path):
            with open(self.summaries_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.book_summaries = data.get('summaries', {})
            print(f"📚 {len(self.book_summaries)} résumés chargés")
        else:
            print("📚 Aucun résumé pré-généré trouvé")
    
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
    
    def check_ai_availability(self):
        """Vérifie la disponibilité des modèles IA"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = []
                
                for model_name, model_info in self.light_models.items():
                    if any(model_info['id'].split(':')[0] in model['name'] for model in models):
                        available_models.append(model_name)
                
                if available_models:
                    self.ai_config["available_models"] = available_models
                    print(f"✅ IA disponible - Modèles: {', '.join(available_models)}")
                    
                    # Auto-sélection du meilleur modèle
                    self.auto_select_model()
                else:
                    print("⚠️ Aucun modèle IA léger trouvé")
            else:
                print("❌ Ollama non disponible")
        except Exception as e:
            print(f"❌ Erreur IA: {e}")
    
    def auto_select_model(self):
        """Sélectionne automatiquement le meilleur modèle disponible"""
        priority_models = ["phi2", "qwen2", "gemma2", "mistral"]
        
        for model in priority_models:
            if model in self.ai_config["available_models"]:
                self.ai_config["model"] = model
                self.ai_config["enabled"] = True
                print(f"🤖 Modèle auto-sélectionné: {model} ({self.light_models[model]['size']})")
                break
    
    def search_books_fast(self, query: str, max_results: int = 5) -> List[Dict]:
        """Recherche RAG pure - RAPIDE"""
        query_embedding = self.model.encode([query])[0]
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        
        scores = [(i, sim) for i, sim in enumerate(similarities)]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for idx, score in scores[:max_results]:
            if idx < len(self.books_data):
                book = self.books_data[idx].copy()
                book['score'] = round(score, 3)
                book['themes'] = self.themes_extracted.get(idx, [])
                results.append(book)
        
        return results
    
    def get_book_summary(self, book_id: int, style: str = "standard") -> str:
        """Récupère le résumé d'un livre"""
        # Vérifier les résumés pré-générés
        if book_id in self.book_summaries:
            summary_data = self.book_summaries[book_id]
            if summary_data.get('style') == style:
                return summary_data['summary']
        
        # Fallback : résumé basique
        book = self.books_data[book_id] if book_id < len(self.books_data) else {}
        if not book:
            return "Livre non trouvé"
        
        title = book.get('title', '')
        author = book.get('author', '')
        genre = book.get('genre', '')
        description = book.get('description', '')
        
        if style == "bref":
            return f"« {title} » par {author} - {genre}. {description[:80]}..."
        else:
            return f"« {title} » par {author} est un {genre}. {description[:150]}..."
    
    def call_ai_model(self, prompt: str, max_tokens: int = 200) -> str:
        """Appelle le modèle IA configuré"""
        if not self.ai_config["enabled"] or not self.ai_config["model"]:
            return "IA non disponible"
        
        try:
            model_info = self.light_models[self.ai_config["model"]]
            
            # Configuration selon le mode de performance
            if self.ai_config["performance_mode"] == "fast":
                max_tokens = min(max_tokens, 150)
                temperature = 0.3
            elif self.ai_config["performance_mode"] == "balanced":
                max_tokens = min(max_tokens, 200)
                temperature = 0.4
            else:  # quality
                max_tokens = min(max_tokens, 300)
                temperature = 0.5
            
            payload = {
                "model": model_info["id"],
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "top_p": 0.8,
                    "max_tokens": max_tokens,
                    "num_ctx": 2048,
                    "repeat_penalty": 1.1
                }
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", 
                                   json=payload, timeout=15)
            
            if response.status_code == 200:
                return response.json().get('response', 'Erreur de réponse')
            else:
                return f"Erreur HTTP: {response.status_code}"
                
        except Exception as e:
            return f"Erreur IA: {str(e)}"
    
    def generate_chat_response(self, user_message: str, user_id: str = None) -> Dict:
        """Génère une réponse de chat intelligente"""
        
        # Initialisation de l'historique
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Ajout du message à l'historique
        self.conversation_history[user_id].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Recherche de livres
        books_found = self.search_books_fast(user_message, max_results=3)
        
        # Génération de la réponse
        if self.ai_config["enabled"]:
            response = self.generate_ai_response(user_message, books_found, user_id)
        else:
            response = self.generate_fallback_response(user_message, books_found)
        
        # Ajout de la réponse à l'historique
        self.conversation_history[user_id].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Limite l'historique
        if len(self.conversation_history[user_id]) > 20:
            self.conversation_history[user_id] = self.conversation_history[user_id][-20:]
        
        return {
            'message': user_message,
            'response': response,
            'books_found': books_found,
            'ai_used': self.ai_config["enabled"],
            'model_used': self.ai_config["model"] if self.ai_config["enabled"] else None
        }
    
    def generate_ai_response(self, message: str, books: List[Dict], user_id: str) -> str:
        """Génère une réponse avec IA"""
        
        # Contexte de conversation
        conversation_context = ""
        if user_id in self.conversation_history and len(self.conversation_history[user_id]) > 2:
            recent_messages = self.conversation_history[user_id][-6:]  # 3 échanges
            conversation_context = "Historique récent:\n"
            for msg in recent_messages[:-1]:
                conversation_context += f"{msg['role']}: {msg['content']}\n"
        
        # Contexte des livres
        books_context = ""
        if books:
            books_context = "Livres trouvés:\n"
            for i, book in enumerate(books):
                books_context += f"{i+1}. {book['title']} par {book['author']}\n"
                books_context += f"   Genre: {book.get('genre', 'N/A')}\n"
                books_context += f"   Thèmes: {', '.join(book.get('themes', []))}\n"
        
        # Prompt optimisé
        prompt = f"""Tu es un bibliothécaire expert de l'association "Les Lumières d'Ukraine".

{conversation_context}

Question: "{message}"

{books_context}

Réponds de manière naturelle et utile, en français impeccable. Suggère des livres spécifiques et explique pourquoi ils correspondent."""
        
        return self.call_ai_model(prompt, max_tokens=250)
    
    def generate_fallback_response(self, message: str, books: List[Dict]) -> str:
        """Génère une réponse sans IA - Fallback intelligent"""
        
        if not books:
            return "Je n'ai pas trouvé de livres correspondant à votre recherche. Pouvez-vous reformuler ou essayer d'autres mots-clés ?"
        
        # Construction de la réponse
        response_parts = []
        
        if len(books) == 1:
            book = books[0]
            response_parts.append(f"J'ai trouvé un livre qui pourrait vous intéresser :")
            response_parts.append(f"📚 **{book['title']}** par {book['author']}")
            response_parts.append(f"Genre : {book.get('genre', 'N/A')}")
            if book.get('themes'):
                response_parts.append(f"Thèmes : {', '.join(book['themes'])}")
        else:
            response_parts.append(f"J'ai trouvé {len(books)} livres qui pourraient vous intéresser :")
            for i, book in enumerate(books):
                response_parts.append(f"{i+1}. **{book['title']}** par {book['author']} ({book.get('genre', 'N/A')})")
        
        response_parts.append("\nVoulez-vous plus de détails sur l'un de ces livres ?")
        
        return '\n'.join(response_parts)
    
    def get_book_details(self, book_id: int) -> Dict:
        """Récupère les détails complets d'un livre"""
        if book_id >= len(self.books_data):
            return {"error": "Livre non trouvé"}
        
        book = self.books_data[book_id].copy()
        book['themes'] = self.themes_extracted.get(book_id, [])
        
        # Ajout du résumé
        summary = self.get_book_summary(book_id, "standard")
        book['summary'] = summary
        
        return book
    
    def configure_ai(self, enabled: bool = None, model: str = None, performance_mode: str = None):
        """Configure l'IA"""
        if enabled is not None:
            self.ai_config["enabled"] = enabled
        
        if model and model in self.ai_config["available_models"]:
            self.ai_config["model"] = model
        
        if performance_mode in ["fast", "balanced", "quality"]:
            self.ai_config["performance_mode"] = performance_mode
        
        print(f"🤖 Configuration IA mise à jour:")
        print(f"   Activée: {self.ai_config['enabled']}")
        print(f"   Modèle: {self.ai_config['model']}")
        print(f"   Mode: {self.ai_config['performance_mode']}")
    
    def get_ai_info(self) -> Dict:
        """Retourne les informations sur l'IA"""
        return {
            "enabled": self.ai_config["enabled"],
            "model": self.ai_config["model"],
            "available_models": self.ai_config["available_models"],
            "performance_mode": self.ai_config["performance_mode"],
            "model_info": self.light_models.get(self.ai_config["model"], {})
        }
    
    def get_statistics(self) -> Dict:
        """Statistiques du chatbot"""
        stats = {
            'total_books': len(self.books_data),
            'total_summaries': len(self.book_summaries),
            'ai_config': self.ai_config,
            'genres': {},
            'themes': {},
            'conversations': len(self.conversation_history)
        }
        
        for book in self.books_data:
            genre = book.get('genre', 'Inconnu')
            stats['genres'][genre] = stats['genres'].get(genre, 0) + 1
        
        for themes in self.themes_extracted.values():
            for theme in themes:
                stats['themes'][theme] = stats['themes'].get(theme, 0) + 1
        
        return stats

def main():
    """Interface CLI pour le chatbot"""
    chatbot = RagTimeChatbot()
    
    print("🤖 RagTime Chatbot - Assistant Bibliothécaire Intelligent")
    print("=" * 60)
    print(f"📚 Livres indexés: {len(chatbot.books_data)}")
    print(f"📝 Résumés disponibles: {len(chatbot.book_summaries)}")
    print(f"🤖 IA: {'Activée' if chatbot.ai_config['enabled'] else 'Désactivée'}")
    if chatbot.ai_config['enabled']:
        model_info = chatbot.light_models.get(chatbot.ai_config['model'], {})
        print(f"   Modèle: {chatbot.ai_config['model']} ({model_info.get('size', 'N/A')})")
        print(f"   Mode: {chatbot.ai_config['performance_mode']}")
    
    while True:
        print("\nOptions disponibles:")
        print("1. Chat avec l'assistant")
        print("2. Détails d'un livre")
        print("3. Configuration IA")
        print("4. Informations système")
        print("5. Quitter")
        
        choice = input("\nVotre choix (1-5): ").strip()
        
        if choice == '1':
            user_id = input("ID utilisateur (optionnel): ").strip() or "default"
            print("\n💬 Mode chat (tapez 'quit' pour sortir)")
            print("🤖 Assistant: Bonjour ! Je suis votre bibliothécaire virtuel. Comment puis-je vous aider ?")
            
            while True:
                message = input(f"\nVous: ")
                if message.lower() == 'quit':
                    break
                
                start_time = time.time()
                response = chatbot.generate_chat_response(message, user_id)
                response_time = time.time() - start_time
                
                print(f"\n🤖 Assistant ({response_time:.2f}s): {response['response']}")
                if response['ai_used']:
                    print(f"   [IA utilisée: {response['model_used']}]")
        
        elif choice == '2':
            print("Livres disponibles:")
            for i, book in enumerate(chatbot.books_data[:10]):
                print(f"{i+1}. {book['title']} par {book['author']}")
            
            try:
                book_id = int(input("\nChoisissez un livre (numéro): ")) - 1
                details = chatbot.get_book_details(book_id)
                
                if 'error' not in details:
                    print(f"\n📚 Détails du livre:")
                    print(f"Titre: {details['title']}")
                    print(f"Auteur: {details['author']}")
                    print(f"Genre: {details.get('genre', 'N/A')}")
                    print(f"Thèmes: {', '.join(details.get('themes', []))}")
                    print(f"Résumé: {details.get('summary', 'N/A')}")
                else:
                    print(f"❌ {details['error']}")
            except ValueError:
                print("❌ Numéro invalide")
        
        elif choice == '3':
            print("\n🤖 Configuration IA")
            print(f"Actuellement: {'Activée' if chatbot.ai_config['enabled'] else 'Désactivée'}")
            
            if chatbot.ai_config['available_models']:
                print("\nModèles disponibles:")
                for i, model in enumerate(chatbot.ai_config['available_models']):
                    model_info = chatbot.light_models[model]
                    print(f"{i+1}. {model} - {model_info['size']} ({model_info['ram']})")
                
                print("\nModes de performance:")
                print("1. fast - Rapide (réponses courtes)")
                print("2. balanced - Équilibré")
                print("3. quality - Qualité (réponses longues)")
                
                config_choice = input("\nChoisissez une option (1-3): ").strip()
                
                if config_choice == '1':
                    chatbot.configure_ai(enabled=True, performance_mode="fast")
                elif config_choice == '2':
                    chatbot.configure_ai(enabled=True, performance_mode="balanced")
                elif config_choice == '3':
                    chatbot.configure_ai(enabled=True, performance_mode="quality")
                else:
                    print("❌ Option invalide")
            else:
                print("❌ Aucun modèle IA disponible")
        
        elif choice == '4':
            stats = chatbot.get_statistics()
            ai_info = chatbot.get_ai_info()
            
            print("\n📊 Informations système:")
            print(f"Total de livres: {stats['total_books']}")
            print(f"Résumés disponibles: {stats['total_summaries']}")
            print(f"Conversations actives: {stats['conversations']}")
            
            print(f"\n🤖 Configuration IA:")
            print(f"Activée: {ai_info['enabled']}")
            if ai_info['enabled']:
                print(f"Modèle: {ai_info['model']}")
                print(f"Mode: {ai_info['performance_mode']}")
                model_info = ai_info['model_info']
                if model_info:
                    print(f"Taille: {model_info.get('size', 'N/A')}")
                    print(f"RAM: {model_info.get('ram', 'N/A')}")
                    print(f"Vitesse: {model_info.get('speed', 'N/A')}")
            
            print(f"\nGenres populaires:")
            for genre, count in sorted(stats['genres'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {genre}: {count}")
        
        elif choice == '5':
            print("Au revoir ! 👋")
            break
        
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main() 