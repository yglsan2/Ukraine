#!/usr/bin/env python3
"""
RagTime API REST - Interface pour intégration avec backend Java
Fournit des endpoints REST pour toutes les fonctionnalités RagTime
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import os
import requests
import time
import logging
import numpy as np
import threading
import atexit
from collections import OrderedDict

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NumpyEncoder robuste pour la sérialisation JSON
class NumpyEncoder(json.JSONEncoder):
    """Encodeur JSON personnalisé pour gérer tous les types numpy automatiquement"""
    
    def default(self, obj):
        """Convertit automatiquement tous les types numpy en types Python natifs"""
        try:
            # Types numpy scalaires
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.bool_):
                return bool(obj)
            elif isinstance(obj, (np.unicode_, np.string_)):
                return str(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.datetime64):
                return obj.item().isoformat()
            elif isinstance(obj, np.timedelta64):
                return obj.item().total_seconds()
            
            # Types numpy avec méthode item()
            elif hasattr(obj, 'item'):
                return obj.item()
            
            # Types numpy avec méthode tolist()
            elif hasattr(obj, 'tolist'):
                return obj.tolist()
            
            # Types numpy avec méthode astype()
            elif hasattr(obj, 'astype'):
                return obj.astype(float).item()
            
            # Fallback pour les autres types numpy
            elif str(type(obj)).startswith("<class 'numpy"):
                return str(obj)
            
            # Appel de la méthode parent pour les types non-numpy
            return super().default(obj)
            
        except Exception as e:
            logger.warning(f"Erreur conversion numpy type {type(obj)}: {e}")
            return str(obj)

# Cache mémoire intelligent pour les recherches
class SearchCache:
    """Cache mémoire pour optimiser les performances de recherche"""
    
    def __init__(self, max_size: int = 100, ttl_hours: int = 24):
        self.max_size = max_size
        self.ttl_hours = ttl_hours
        self.cache = OrderedDict()
        self.lock = threading.Lock()
        
    def _generate_key(self, query: str, filters: Dict = None, use_ai: bool = True) -> str:
        """Génère une clé unique pour la recherche"""
        filter_str = json.dumps(filters, sort_keys=True) if filters else "{}"
        return f"{query.lower().strip()}|{filter_str}|{use_ai}"
    
    def get(self, query: str, filters: Dict = None, use_ai: bool = True) -> Optional[Dict]:
        """Récupère un résultat du cache"""
        with self.lock:
            key = self._generate_key(query, filters, use_ai)
            if key in self.cache:
                result, timestamp = self.cache[key]
                # Vérifier l'expiration
                if datetime.now() - timestamp < timedelta(hours=self.ttl_hours):
                    # Déplacer en fin (LRU)
                    self.cache.move_to_end(key)
                    logger.info(f"Cache hit pour: {query}")
                    return result
                else:
                    # Supprimer l'entrée expirée
                    del self.cache[key]
            return None
    
    def set(self, query: str, result: Dict, filters: Dict = None, use_ai: bool = True):
        """Ajoute un résultat au cache"""
        with self.lock:
            key = self._generate_key(query, filters, use_ai)
            
            # Supprimer l'ancienne entrée si elle existe
            if key in self.cache:
                del self.cache[key]
            
            # Ajouter la nouvelle entrée
            self.cache[key] = (result, datetime.now())
            
            # Gérer la taille maximale (LRU)
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)
            
            logger.info(f"Cache miss pour: {query} (taille cache: {len(self.cache)})")
    
    def clear(self):
        """Vide le cache"""
        with self.lock:
            self.cache.clear()
            logger.info("Cache vidé")
    
    def get_stats(self) -> Dict:
        """Retourne les statistiques du cache"""
        with self.lock:
            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'ttl_hours': self.ttl_hours,
                'keys': list(self.cache.keys())[:10]  # Premiers 10 éléments
            }

# Singleton pour RagTime API
class RagTimeSingleton:
    """Singleton pour éviter la multiplication des instances RagTime"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self.api = None
            self.cache = SearchCache()
            self._init_lock = threading.Lock()
    
    def get_api(self) -> 'RagTimeAPI':
        """Retourne l'instance RagTime API (initialisation lazy)"""
        if self.api is None:
            with self._init_lock:
                if self.api is None:
                    logger.info("Initialisation de RagTime API...")
                    self.api = RagTimeAPI()
                    logger.info("RagTime API initialisée avec succès")
        return self.api
    
    def get_cache(self) -> SearchCache:
        """Retourne le cache de recherche"""
        return self.cache

# Instance globale du singleton
ragtime_singleton = RagTimeSingleton()

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin

# Configuration de l'encodeur JSON personnalisé pour Flask
app.json_encoder = NumpyEncoder

class RagTimeAPI:
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
        
        # Configuration IA
        self.ai_config = {
            "enabled": False,
            "primary_model": None,  # Phi-2 2.7B
            "quality_model": None,  # Mistral 7B
            "available_models": [],
            "mode": "fast"
        }
        
        # Modèles IA
        self.dual_models = {
            "phi2": {
                "id": "phi:2.7b",
                "name": "Phi-2 2.7B",
                "size": "2.7B",
                "ram": "4GB"
            },
            "mistral": {
                "id": "mistral:7b-instruct",
                "name": "Mistral 7B Instruct",
                "size": "7B",
                "ram": "8GB"
            }
        }
        
        self.load_data()
        self.extract_themes()
        self.load_summaries()
        self.check_ai_availability()
        
        logger.info("RagTime API initialisée avec succès")
    
    def load_data(self):
        """Charge les données et l'index"""
        try:
            if os.path.exists(self.data_path):
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    self.books_data = json.load(f)
                logger.info(f"📚 {len(self.books_data)} livres chargés")
            
            if os.path.exists(self.index_path):
                with open(self.index_path, 'rb') as f:
                    index_data = pickle.load(f)
                    self.embeddings = index_data['embeddings']
                    self.concepts = index_data['concepts']
                logger.info(f"📊 Index vectoriel chargé")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données: {e}")
    
    def load_summaries(self):
        """Charge les résumés pré-générés"""
        try:
            if os.path.exists(self.summaries_path):
                with open(self.summaries_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.book_summaries = data.get('summaries', {})
                logger.info(f"📝 {len(self.book_summaries)} résumés chargés")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des résumés: {e}")
    
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
                
                for model_name, model_info in self.dual_models.items():
                    if any(model_info['id'].split(':')[0] in model['name'] for model in models):
                        available_models.append(model_name)
                
                if available_models:
                    self.ai_config["available_models"] = available_models
                    if "phi2" in available_models:
                        self.ai_config["primary_model"] = "phi2"
                    if "mistral" in available_models:
                        self.ai_config["quality_model"] = "mistral"
                    
                    self.ai_config["enabled"] = True
                    logger.info(f"✅ IA disponible - Modèles: {', '.join(available_models)}")
                else:
                    logger.info("⚠️ Aucun modèle IA trouvé")
            else:
                logger.info("❌ Ollama non disponible")
        except Exception as e:
            logger.error(f"Erreur IA: {e}")
    
    def search_books_rag(self, query: str, filters: Dict = None, max_results: int = 10) -> List[Dict]:
        """Recherche RAG pure"""
        try:
            query_embedding = self.model.encode([query])[0]
            similarities = cosine_similarity([query_embedding], self.embeddings)[0]
            
            # Créer les scores (le NumpyEncoder s'occupera de la conversion)
            scores = [(i, sim) for i, sim in enumerate(similarities)]
            scores.sort(key=lambda x: x[1], reverse=True)
            
            # Application des filtres
            if filters:
                scores = self.apply_filters(scores, filters)
            
            results = []
            for idx, score in scores[:max_results]:
                if idx < len(self.books_data):
                    book = self.books_data[idx].copy()
                    book['score'] = score  # Le NumpyEncoder convertira automatiquement
                    book['themes'] = self.themes_extracted.get(idx, [])
                    results.append(book)
            
            return results
        except Exception as e:
            logger.error(f"Erreur recherche RAG: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return []
    
    def apply_filters(self, scores: List[Tuple[int, float]], filters: Dict) -> List[Tuple[int, float]]:
        """Applique les filtres aux résultats"""
        filtered_scores = []
        
        for idx, score in scores:
            if idx >= len(self.books_data):
                continue
            
            book = self.books_data[idx]
            include = True
            
            if 'genre' in filters and book.get('genre') != filters['genre']:
                include = False
            if 'language' in filters and book.get('language') != filters['language']:
                include = False
            if 'city' in filters and book.get('city') != filters['city']:
                include = False
            if 'status' in filters and book.get('status') != filters['status']:
                include = False
            
            if include:
                filtered_scores.append((idx, score))
        
        return filtered_scores
    
    def call_ai_model(self, prompt: str, model_type: str = "primary") -> str:
        """Appelle le modèle IA"""
        if not self.ai_config["enabled"]:
            return "IA non disponible"
        
        try:
            if model_type == "primary" and self.ai_config["primary_model"]:
                model_name = self.ai_config["primary_model"]
            elif model_type == "quality" and self.ai_config["quality_model"]:
                model_name = self.ai_config["quality_model"]
            else:
                model_name = self.ai_config["primary_model"] or self.ai_config["quality_model"]
            
            if not model_name:
                return "Aucun modèle IA disponible"
            
            model_info = self.dual_models[model_name]
            
            payload = {
                "model": model_info["id"],
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.4,
                    "top_p": 0.8,
                    "max_tokens": 250,
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
    
    def generate_dual_response(self, query: str, user_id: str = None, use_ai: bool = True) -> Dict:
        """Génère une réponse dual : RAG + IA optionnelle"""
        try:
            start_time = time.time()
            
            # Recherche RAG (toujours active)
            books_found = self.search_books_rag(query, max_results=5)
            rag_time = time.time() - start_time
            
            # Réponse RAG
            rag_response = self.format_rag_response(books_found)
            
            # Réponse IA (optionnelle)
            ai_response = None
            ai_time = 0
            
            if use_ai and self.ai_config["enabled"]:
                ai_start = time.time()
                ai_response = self.generate_ai_complement(query, books_found)
                ai_time = time.time() - ai_start
            
            # Combinaison
            final_response = self.combine_responses(rag_response, ai_response)
            
            result = {
                'success': True,
                'query': query,
                'response': final_response,
                'rag_response': rag_response,
                'ai_response': ai_response,
                'books': books_found,
                'timing': {
                    'rag_time': rag_time,
                    'ai_time': ai_time,
                    'total_time': rag_time + ai_time
                },
                'ai_used': ai_response is not None,
                'ai_model': self.ai_config["mode"] if ai_response else None
            }
            
            # Le NumpyEncoder s'occupera automatiquement de la conversion
            return result
            
        except Exception as e:
            logger.error(f"Erreur génération réponse: {e}")
            import traceback
            logger.error(f"Traceback complet: {traceback.format_exc()}")
            
            # Retourner une réponse d'erreur sérialisable
            return {
                'success': False,
                'error': str(e),
                'query': query,
                'response': f"Erreur lors de la recherche: {str(e)}",
                'rag_response': None,
                'ai_response': None,
                'books': [],
                'timing': {
                    'rag_time': 0.0,
                    'ai_time': 0.0,
                    'total_time': 0.0
                },
                'ai_used': False,
                'ai_model': None
            }
    
    def format_rag_response(self, books: List[Dict]) -> str:
        """Formate la réponse RAG"""
        if not books:
            return "Aucun livre trouvé correspondant à votre recherche."
        
        response_parts = []
        for i, book in enumerate(books):
            response_parts.append(f"{i+1}. **{book['title']}** par {book['author']}")
            response_parts.append(f"   Genre: {book.get('genre', 'N/A')}")
            if book.get('themes'):
                response_parts.append(f"   Thèmes: {', '.join(book['themes'])}")
            response_parts.append(f"   Score: {book['score']}")
        
        return '\n'.join(response_parts)
    
    def generate_ai_complement(self, query: str, books: List[Dict]) -> str:
        """Génère la réponse IA complémentaire"""
        books_context = ""
        if books:
            books_context = "Livres trouvés:\n"
            for i, book in enumerate(books):
                books_context += f"{i+1}. {book['title']} par {book['author']}\n"
                books_context += f"   Genre: {book.get('genre', 'N/A')}\n"
        
        prompt = f"""Tu es un bibliothécaire expert. Enrichis cette réponse:

Question: "{query}"

{books_context}

Ajoute des explications et suggestions en français:"""
        
        model_type = "primary" if self.ai_config["mode"] == "fast" else "quality"
        return self.call_ai_model(prompt, model_type)
    
    def combine_responses(self, rag_response: str, ai_response: str = None) -> str:
        """Combine les réponses RAG et IA"""
        if not ai_response:
            return rag_response
        
        return f"{rag_response}\n\n🤖 **Enrichissement IA:**\n{ai_response}"
    
    def get_book_summary(self, book_id: int, style: str = "standard") -> str:
        """Récupère le résumé d'un livre"""
        if book_id in self.book_summaries:
            summary_data = self.book_summaries[book_id]
            if summary_data.get('style') == style:
                return summary_data['summary']
        
        # Fallback
        book = self.books_data[book_id] if book_id < len(self.books_data) else {}
        if not book:
            return "Livre non trouvé"
        
        title = book.get('title', '')
        author = book.get('author', '')
        genre = book.get('genre', '')
        description = book.get('description', '')
        
        return f"« {title} » par {author} - {genre}. {description[:100]}..."
    
    def get_statistics(self) -> Dict:
        """Retourne les statistiques"""
        return {
            'total_books': len(self.books_data),
            'total_summaries': len(self.book_summaries),
            'ai_enabled': self.ai_config["enabled"],
            'ai_models': self.ai_config["available_models"],
            'genres': {},
            'themes': {}
        }

# Fonction de nettoyage automatique
def cleanup_on_exit():
    """Nettoyage automatique à la fermeture"""
    try:
        cache = ragtime_singleton.get_cache()
        cache.clear()
        logger.info("Nettoyage automatique effectué")
    except Exception as e:
        logger.error(f"Erreur lors du nettoyage: {e}")

# Enregistrer la fonction de nettoyage
atexit.register(cleanup_on_exit)

# Endpoints REST

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de santé de l'API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'RagTime API'
    })

@app.route('/api/search', methods=['POST'])
def search_books():
    """Recherche de livres avec cache intelligent"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        filters = data.get('filters', {})
        max_results = data.get('maxResults', 10)
        use_ai = data.get('useAI', True)
        user_id = data.get('user_id')
        
        if not query:
            return jsonify({'error': 'Query requise'}), 400
        
        # Récupérer le singleton et le cache
        ragtime_api = ragtime_singleton.get_api()
        cache = ragtime_singleton.get_cache()
        
        # Vérifier le cache d'abord
        cached_result = cache.get(query, filters, use_ai)
        if cached_result:
            logger.info(f"Résultat trouvé en cache pour: {query}")
            return app.response_class(
                response=json.dumps(cached_result, cls=NumpyEncoder),
                status=200,
                mimetype='application/json'
            )
        
        # Si pas en cache, faire la recherche
        logger.info(f"Nouvelle recherche: {query}")
        result = ragtime_api.generate_dual_response(query, user_id, use_ai)
        
        # Mettre en cache le résultat
        cache.set(query, result, filters, use_ai)
        
        # Utilisation explicite du NumpyEncoder
        return app.response_class(
            response=json.dumps(result, cls=NumpyEncoder),
            status=200,
            mimetype='application/json'
        )
        
    except Exception as e:
        logger.error(f"Erreur recherche: {e}")
        import traceback
        logger.error(f"Traceback recherche: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/books', methods=['GET'])
def get_books():
    """Liste des livres"""
    try:
        ragtime_api = ragtime_singleton.get_api()
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        books = ragtime_api.books_data[offset:offset+limit]
        return jsonify({
            'books': books,
            'total': len(ragtime_api.books_data),
            'limit': limit,
            'offset': offset
        })
        
    except Exception as e:
        logger.error(f"Erreur liste livres: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Détails d'un livre"""
    try:
        ragtime_api = ragtime_singleton.get_api()
        if book_id >= len(ragtime_api.books_data):
            return jsonify({'error': 'Livre non trouvé'}), 404
        
        book = ragtime_api.books_data[book_id].copy()
        book['themes'] = ragtime_api.themes_extracted.get(book_id, [])
        book['summary'] = ragtime_api.get_book_summary(book_id)
        
        return jsonify(book)
        
    except Exception as e:
        logger.error(f"Erreur livre: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/summary/<int:book_id>', methods=['GET'])
def get_book_summary(book_id):
    """Résumé d'un livre"""
    try:
        ragtime_api = ragtime_singleton.get_api()
        style = request.args.get('style', 'standard')
        summary = ragtime_api.get_book_summary(book_id, style)
        
        return jsonify({
            'book_id': book_id,
            'style': style,
            'summary': summary
        })
        
    except Exception as e:
        logger.error(f"Erreur résumé: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """Recommandations personnalisées"""
    try:
        ragtime_api = ragtime_singleton.get_api()
        data = request.get_json()
        user_id = data.get('user_id')
        filters = data.get('filters', {})
        max_results = data.get('max_results', 10)
        
        # Simulation de recommandations basées sur l'historique
        recommendations = ragtime_api.search_books_rag("livre recommandé", filters, max_results)
        
        return jsonify({
            'recommendations': recommendations,
            'user_id': user_id
        })
        
    except Exception as e:
        logger.error(f"Erreur recommandations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Statistiques générales"""
    try:
        ragtime_api = ragtime_singleton.get_api()
        stats = ragtime_api.get_statistics()
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Erreur statistiques: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/status', methods=['GET'])
def get_ai_status():
    """Statut de l'IA"""
    try:
        ragtime_api = ragtime_singleton.get_api()
        return jsonify({
            'enabled': ragtime_api.ai_config["enabled"],
            'available_models': ragtime_api.ai_config["available_models"],
            'primary_model': ragtime_api.ai_config["primary_model"],
            'quality_model': ragtime_api.ai_config["quality_model"],
            'mode': ragtime_api.ai_config["mode"]
        })
        
    except Exception as e:
        logger.error(f"Erreur statut IA: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/configure', methods=['POST'])
def configure_ai():
    """Configuration de l'IA"""
    try:
        ragtime_api = ragtime_singleton.get_api()
        data = request.get_json()
        
        if 'mode' in data:
            ragtime_api.ai_config["mode"] = data['mode']
        
        if 'enabled' in data:
            ragtime_api.ai_config["enabled"] = data['enabled']
        
        return jsonify({
            'message': 'Configuration mise à jour',
            'config': ragtime_api.ai_config
        })
        
    except Exception as e:
        logger.error(f"Erreur configuration IA: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache/stats', methods=['GET'])
def get_cache_stats():
    """Statistiques du cache de recherche"""
    try:
        cache = ragtime_singleton.get_cache()
        stats = cache.get_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Erreur stats cache: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Vide le cache de recherche"""
    try:
        cache = ragtime_singleton.get_cache()
        cache.clear()
        return jsonify({'message': 'Cache vidé avec succès'})
    except Exception as e:
        logger.error(f"Erreur vidage cache: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/status', methods=['GET'])
def get_system_status():
    """Statut complet du système RagTime"""
    try:
        ragtime_api = ragtime_singleton.get_api()
        cache = ragtime_singleton.get_cache()
        
        status = {
            'api_status': 'healthy',
            'cache_stats': cache.get_stats(),
            'ai_status': ragtime_api.ai_config,
            'books_count': len(ragtime_api.books_data),
            'embeddings_loaded': len(ragtime_api.embeddings) > 0,
            'summaries_count': len(ragtime_api.book_summaries),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(status)
    except Exception as e:
        logger.error(f"Erreur statut système: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Configuration du serveur
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Démarrage RagTime API sur le port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug) 