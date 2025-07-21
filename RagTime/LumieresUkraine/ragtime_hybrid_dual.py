#!/usr/bin/env python3
"""
RagTime Hybrid Dual - Système RAG + IA Complémentaire
RAG pur toujours actif + IA optionnelle pour enrichissement
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

class RagTimeHybridDual:
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
        
        # Configuration IA dual
        self.ai_config = {
            "enabled": False,
            "primary_model": None,  # Phi-2 2.7B (rapide)
            "quality_model": None,  # Mistral 7B Instruct (qualité)
            "available_models": [],
            "mode": "fast"  # fast (Phi-2) ou quality (Mistral)
        }
        
        # Modèles IA dual
        self.dual_models = {
            "phi2": {
                "id": "phi:2.7b",
                "name": "Phi-2 2.7B",
                "size": "2.7B",
                "ram": "4GB",
                "speed": "fast",
                "french": 4,
                "summaries": 4,
                "type": "primary"
            },
            "mistral": {
                "id": "mistral:7b-instruct",
                "name": "Mistral 7B Instruct",
                "size": "7B",
                "ram": "8GB",
                "speed": "quality",
                "french": 5,
                "summaries": 5,
                "type": "quality"
            }
        }
        
        self.load_data()
        self.extract_themes()
        self.load_summaries()
        self.check_dual_ai_availability()
    
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
    
    def check_dual_ai_availability(self):
        """Vérifie la disponibilité des modèles IA dual"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = []
                
                for model_name, model_info in self.dual_models.items():
                    if any(model_info['id'].split(':')[0] in model['name'] for model in models):
                        available_models.append(model_name)
                
                if available_models:
                    self.ai_config["available_models"] = available_models
                    print(f"✅ IA Dual disponible - Modèles: {', '.join(available_models)}")
                    
                    # Auto-configuration dual
                    self.auto_configure_dual()
                else:
                    print("⚠️ Aucun modèle IA dual trouvé")
            else:
                print("❌ Ollama non disponible")
        except Exception as e:
            print(f"❌ Erreur IA: {e}")
    
    def auto_configure_dual(self):
        """Configure automatiquement les modèles dual"""
        available = self.ai_config["available_models"]
        
        # Configuration primaire (Phi-2)
        if "phi2" in available:
            self.ai_config["primary_model"] = "phi2"
            print(f"⚡ Modèle primaire: Phi-2 2.7B (rapide)")
        
        # Configuration qualité (Mistral)
        if "mistral" in available:
            self.ai_config["quality_model"] = "mistral"
            print(f"🎯 Modèle qualité: Mistral 7B Instruct")
        
        # Activation si au moins un modèle disponible
        if self.ai_config["primary_model"] or self.ai_config["quality_model"]:
            self.ai_config["enabled"] = True
            self.ai_config["mode"] = "fast" if self.ai_config["primary_model"] else "quality"
    
    def search_books_rag(self, query: str, max_results: int = 5) -> List[Dict]:
        """Recherche RAG pure - TOUJOURS ACTIVE"""
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
        if book_id in self.book_summaries:
            summary_data = self.book_summaries[book_id]
            if summary_data.get('style') == style:
                return summary_data['summary']
        
        # Fallback basique
        book = self.books_data[book_id] if book_id < len(self.books_data) else {}
        if not book:
            return "Livre non trouvé"
        
        title = book.get('title', '')
        author = book.get('author', '')
        genre = book.get('genre', '')
        description = book.get('description', '')
        
        return f"« {title} » par {author} - {genre}. {description[:100]}..."
    
    def call_dual_ai(self, prompt: str, model_type: str = "primary") -> str:
        """Appelle le modèle IA dual configuré"""
        if not self.ai_config["enabled"]:
            return "IA non disponible"
        
        # Sélection du modèle
        if model_type == "primary" and self.ai_config["primary_model"]:
            model_name = self.ai_config["primary_model"]
        elif model_type == "quality" and self.ai_config["quality_model"]:
            model_name = self.ai_config["quality_model"]
        else:
            # Fallback sur le modèle disponible
            model_name = self.ai_config["primary_model"] or self.ai_config["quality_model"]
        
        if not model_name:
            return "Aucun modèle IA disponible"
        
        try:
            model_info = self.dual_models[model_name]
            
            # Configuration selon le type de modèle
            if model_name == "phi2":
                max_tokens = 200
                temperature = 0.4
                timeout = 10
            else:  # mistral
                max_tokens = 300
                temperature = 0.5
                timeout = 20
            
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
                                   json=payload, timeout=timeout)
            
            if response.status_code == 200:
                return response.json().get('response', 'Erreur de réponse')
            else:
                return f"Erreur HTTP: {response.status_code}"
                
        except Exception as e:
            return f"Erreur IA: {str(e)}"
    
    def generate_dual_response(self, user_message: str, user_id: str = None) -> Dict:
        """Génère une réponse dual : RAG + IA optionnelle"""
        
        # Initialisation de l'historique
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = {}
        
        # Ajout du message à l'historique
        if 'messages' not in self.conversation_history[user_id]:
            self.conversation_history[user_id]['messages'] = []
        
        self.conversation_history[user_id]['messages'].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # 1. RECHERCHE RAG (TOUJOURS ACTIVE)
        start_time = time.time()
        books_found = self.search_books_rag(user_message, max_results=3)
        rag_time = time.time() - start_time
        
        # 2. RÉPONSE RAG (TOUJOURS GÉNÉRÉE)
        rag_response = self.generate_rag_response(user_message, books_found)
        
        # 3. RÉPONSE IA (OPTIONNELLE)
        ai_response = None
        ai_time = 0
        ai_model_used = None
        
        if self.ai_config["enabled"]:
            start_time = time.time()
            ai_response = self.generate_ai_complement(user_message, books_found, user_id)
            ai_time = time.time() - start_time
            ai_model_used = self.ai_config["mode"]
        
        # 4. RÉPONSE FINALE
        final_response = self.combine_responses(rag_response, ai_response)
        
        # Ajout de la réponse à l'historique
        self.conversation_history[user_id]['messages'].append({
            'role': 'assistant',
            'content': final_response,
            'rag_response': rag_response,
            'ai_response': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Limite l'historique
        if len(self.conversation_history[user_id]['messages']) > 20:
            self.conversation_history[user_id]['messages'] = self.conversation_history[user_id]['messages'][-20:]
        
        return {
            'message': user_message,
            'final_response': final_response,
            'rag_response': rag_response,
            'ai_response': ai_response,
            'books_found': books_found,
            'timing': {
                'rag_time': rag_time,
                'ai_time': ai_time,
                'total_time': rag_time + ai_time
            },
            'ai_used': ai_response is not None,
            'ai_model': ai_model_used
        }
    
    def generate_rag_response(self, message: str, books: List[Dict]) -> str:
        """Génère la réponse RAG (toujours active)"""
        if not books:
            return "Je n'ai pas trouvé de livres correspondant à votre recherche. Pouvez-vous reformuler ou essayer d'autres mots-clés ?"
        
        response_parts = []
        
        if len(books) == 1:
            book = books[0]
            response_parts.append(f"📚 **{book['title']}** par {book['author']}")
            response_parts.append(f"Genre : {book.get('genre', 'N/A')}")
            if book.get('themes'):
                response_parts.append(f"Thèmes : {', '.join(book['themes'])}")
            response_parts.append(f"Score de pertinence : {book['score']}")
        else:
            response_parts.append(f"J'ai trouvé {len(books)} livres pertinents :")
            for i, book in enumerate(books):
                response_parts.append(f"{i+1}. **{book['title']}** par {book['author']} ({book.get('genre', 'N/A')})")
                if book.get('themes'):
                    response_parts.append(f"   Thèmes : {', '.join(book['themes'])}")
        
        return '\n'.join(response_parts)
    
    def generate_ai_complement(self, message: str, books: List[Dict], user_id: str) -> str:
        """Génère la réponse IA complémentaire"""
        
        # Contexte de conversation
        conversation_context = ""
        if user_id in self.conversation_history and 'messages' in self.conversation_history[user_id]:
            recent_messages = self.conversation_history[user_id]['messages'][-6:]  # 3 échanges
            conversation_context = "Contexte de la conversation:\n"
            for msg in recent_messages[:-1]:
                conversation_context += f"{msg['role']}: {msg['content']}\n"
        
        # Contexte des livres
        books_context = ""
        if books:
            books_context = "Livres trouvés par le système RAG:\n"
            for i, book in enumerate(books):
                books_context += f"{i+1}. {book['title']} par {book['author']}\n"
                books_context += f"   Genre: {book.get('genre', 'N/A')}\n"
                books_context += f"   Thèmes: {', '.join(book.get('themes', []))}\n"
        
        # Prompt pour enrichissement IA
        prompt = f"""Tu es un bibliothécaire expert qui enrichit les réponses du système RAG.

{conversation_context}

Question de l'utilisateur: "{message}"

{books_context}

Enrichis la réponse RAG en ajoutant:
- Des explications sur pourquoi ces livres correspondent
- Des suggestions de lecture complémentaires
- Des conseils personnalisés
- Des éléments culturels ou contextuels

Réponse courte et enrichissante:"""
        
        # Choix du modèle selon le mode
        model_type = "primary" if self.ai_config["mode"] == "fast" else "quality"
        return self.call_dual_ai(prompt, model_type)
    
    def combine_responses(self, rag_response: str, ai_response: str = None) -> str:
        """Combine les réponses RAG et IA"""
        if not ai_response:
            return rag_response
        
        # Combinaison intelligente
        combined = f"{rag_response}\n\n🤖 **Enrichissement IA :**\n{ai_response}"
        return combined
    
    def switch_ai_mode(self, mode: str):
        """Change le mode IA"""
        if mode in ["fast", "quality"]:
            self.ai_config["mode"] = mode
            print(f"🤖 Mode IA changé vers: {mode}")
            if mode == "fast":
                print(f"   Modèle: {self.dual_models.get(self.ai_config.get('primary_model', ''), {}).get('name', 'N/A')}")
            else:
                print(f"   Modèle: {self.dual_models.get(self.ai_config.get('quality_model', ''), {}).get('name', 'N/A')}")
        else:
            print("❌ Mode invalide. Utilisez 'fast' ou 'quality'")
    
    def get_dual_info(self) -> Dict:
        """Retourne les informations sur le système dual"""
        return {
            "enabled": self.ai_config["enabled"],
            "mode": self.ai_config["mode"],
            "primary_model": {
                "name": self.dual_models.get(self.ai_config.get("primary_model", ""), {}).get("name", "Non disponible"),
                "available": self.ai_config["primary_model"] is not None
            },
            "quality_model": {
                "name": self.dual_models.get(self.ai_config.get("quality_model", ""), {}).get("name", "Non disponible"),
                "available": self.ai_config["quality_model"] is not None
            },
            "available_models": self.ai_config["available_models"]
        }
    
    def get_statistics(self) -> Dict:
        """Statistiques du système dual"""
        stats = {
            'total_books': len(self.books_data),
            'total_summaries': len(self.book_summaries),
            'dual_config': self.ai_config,
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
    """Interface CLI pour le système dual"""
    dual_system = RagTimeHybridDual()
    
    print("🤖 RagTime Hybrid Dual - RAG + IA Complémentaire")
    print("=" * 60)
    print(f"📚 Livres indexés: {len(dual_system.books_data)}")
    print(f"📝 Résumés disponibles: {len(dual_system.book_summaries)}")
    
    dual_info = dual_system.get_dual_info()
    print(f"🤖 IA Dual: {'Activée' if dual_info['enabled'] else 'Désactivée'}")
    if dual_info['enabled']:
        print(f"   Mode: {dual_info['mode']}")
        print(f"   Modèle rapide: {dual_info['primary_model']['name']}")
        print(f"   Modèle qualité: {dual_info['quality_model']['name']}")
    
    while True:
        print("\nOptions disponibles:")
        print("1. Chat avec système dual")
        print("2. Changer mode IA")
        print("3. Informations système")
        print("4. Quitter")
        
        choice = input("\nVotre choix (1-4): ").strip()
        
        if choice == '1':
            user_id = input("ID utilisateur (optionnel): ").strip() or "default"
            print("\n💬 Mode chat dual (tapez 'quit' pour sortir)")
            print("🤖 Assistant: Bonjour ! Je suis votre bibliothécaire dual. RAG + IA pour vous servir !")
            
            while True:
                message = input(f"\nVous: ")
                if message.lower() == 'quit':
                    break
                
                start_time = time.time()
                response = dual_system.generate_dual_response(message, user_id)
                total_time = time.time() - start_time
                
                print(f"\n🤖 Assistant ({total_time:.2f}s):")
                print(response['final_response'])
                
                # Affichage des détails
                print(f"\n📊 Détails:")
                print(f"   RAG: {response['timing']['rag_time']:.3f}s")
                if response['ai_used']:
                    print(f"   IA: {response['timing']['ai_time']:.3f}s ({response['ai_model']})")
                else:
                    print(f"   IA: Non utilisée")
        
        elif choice == '2':
            if not dual_info['enabled']:
                print("❌ IA non disponible")
                continue
            
            print("\n🤖 Changement de mode IA")
            print("1. fast - Modèle rapide (Phi-2)")
            print("2. quality - Modèle qualité (Mistral)")
            
            mode_choice = input("\nChoisissez un mode (1-2): ").strip()
            if mode_choice == '1':
                dual_system.switch_ai_mode("fast")
            elif mode_choice == '2':
                dual_system.switch_ai_mode("quality")
            else:
                print("❌ Choix invalide")
        
        elif choice == '3':
            stats = dual_system.get_statistics()
            dual_info = dual_system.get_dual_info()
            
            print("\n📊 Informations système dual:")
            print(f"Total de livres: {stats['total_books']}")
            print(f"Résumés disponibles: {stats['total_summaries']}")
            print(f"Conversations actives: {stats['conversations']}")
            
            print(f"\n🤖 Configuration IA Dual:")
            print(f"Activée: {dual_info['enabled']}")
            if dual_info['enabled']:
                print(f"Mode actuel: {dual_info['mode']}")
                print(f"Modèle rapide: {dual_info['primary_model']['name']} ({'✅' if dual_info['primary_model']['available'] else '❌'})")
                print(f"Modèle qualité: {dual_info['quality_model']['name']} ({'✅' if dual_info['quality_model']['available'] else '❌'})")
            
            print(f"\nGenres populaires:")
            for genre, count in sorted(stats['genres'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {genre}: {count}")
        
        elif choice == '4':
            print("Au revoir ! 👋")
            break
        
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main() 