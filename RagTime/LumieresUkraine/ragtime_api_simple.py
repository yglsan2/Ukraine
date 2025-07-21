#!/usr/bin/env python3
"""
API RagTime simplifiée et fonctionnelle
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class SimpleRagTime:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.books_data = []
        self.embeddings = []
        self.themes_extracted = {}
        self.book_summaries = {}
        
        self.load_data()
        self.extract_themes()
        self.load_summaries()
        
        logger.info("SimpleRagTime initialisé")
    
    def load_data(self):
        """Charge les données"""
        try:
            if os.path.exists("books_data.json"):
                with open("books_data.json", 'r', encoding='utf-8') as f:
                    self.books_data = json.load(f)
                logger.info(f"📚 {len(self.books_data)} livres chargés")
            
            if os.path.exists("books_index.pkl"):
                with open("books_index.pkl", 'rb') as f:
                    index_data = pickle.load(f)
                    self.embeddings = index_data['embeddings']
                logger.info(f"📊 Index vectoriel chargé")
        except Exception as e:
            logger.error(f"Erreur chargement: {e}")
    
    def load_summaries(self):
        """Charge les résumés"""
        try:
            if os.path.exists("smart_summaries.json"):
                with open("smart_summaries.json", 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.book_summaries = data.get('summaries', {})
                logger.info(f"📝 {len(self.book_summaries)} résumés chargés")
        except Exception as e:
            logger.error(f"Erreur résumés: {e}")
    
    def extract_themes(self):
        """Extrait les thèmes"""
        theme_keywords = {
            'amitié': ['ami', 'amitié', 'solidarité'],
            'aventure': ['aventure', 'voyage', 'découverte'],
            'famille': ['famille', 'parent', 'enfant'],
            'guerre': ['guerre', 'conflit', 'paix'],
            'nature': ['nature', 'animal', 'forêt'],
            'culture': ['culture', 'tradition', 'art'],
            'éducation': ['école', 'apprentissage', 'savoir'],
            'amour': ['amour', 'romance', 'sentiment'],
            'mystère': ['mystère', 'énigme', 'secret'],
            'fantasy': ['magie', 'fantastique', 'créature'],
            'histoire': ['historique', 'passé', 'époque'],
            'science': ['science', 'technologie', 'découverte'],
            'philosophie': ['philosophie', 'réflexion', 'pensée'],
            'humour': ['humour', 'comique', 'drôle'],
            'émotion': ['émotion', 'sentiment', 'joie']
        }
        
        for i, book in enumerate(self.books_data):
            text = f"{book.get('title', '')} {book.get('description', '')} {book.get('genre', '')}"
            text_lower = text.lower()
            
            book_themes = []
            for theme, keywords in theme_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    book_themes.append(theme)
            
            self.themes_extracted[i] = book_themes
    
    def search_books(self, query, max_results=10):
        """Recherche de livres"""
        try:
            if not self.embeddings:
                return []
            
            query_embedding = self.model.encode([query])[0]
            similarities = cosine_similarity([query_embedding], self.embeddings)[0]
            
            scores = [(i, float(sim)) for i, sim in enumerate(similarities)]
            scores.sort(key=lambda x: x[1], reverse=True)
            
            results = []
            for idx, score in scores[:max_results]:
                if idx < len(self.books_data):
                    book = self.books_data[idx].copy()
                    book['score'] = float(score)
                    book['themes'] = self.themes_extracted.get(idx, [])
                    results.append(book)
            
            return results
        except Exception as e:
            logger.error(f"Erreur recherche: {e}")
            return []
    
    def get_book_summary(self, book_id, style="standard"):
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

# Instance globale
ragtime = SimpleRagTime()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de santé"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'service': 'Simple RagTime API'
    })

@app.route('/api/search', methods=['POST'])
def search_books():
    """Recherche de livres"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        max_results = data.get('maxResults', 10)
        use_ai = data.get('useAI', False)
        
        if not query:
            return jsonify({'error': 'Query requise'}), 400
        
        start_time = time.time()
        books_found = ragtime.search_books(query, max_results)
        rag_time = time.time() - start_time
        
        # Formatage de la réponse
        rag_response = ""
        if books_found:
            for i, book in enumerate(books_found):
                rag_response += f"{i+1}. **{book['title']}** par {book['author']}\n"
                rag_response += f"   Genre: {book.get('genre', 'N/A')}\n"
                if book.get('themes'):
                    rag_response += f"   Thèmes: {', '.join(book['themes'])}\n"
                rag_response += f"   Score: {book['score']:.3f}\n"
        else:
            rag_response = "Aucun livre trouvé correspondant à votre recherche."
        
        return jsonify({
            'success': True,
            'query': query,
            'response': rag_response,
            'rag_response': rag_response,
            'ai_response': None,
            'books': books_found,
            'timing': {
                'rag_time': float(rag_time),
                'ai_time': 0.0,
                'total_time': float(rag_time)
            },
            'ai_used': False,
            'ai_model': None
        })
        
    except Exception as e:
        logger.error(f"Erreur recherche: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/books/<int:book_id>/summary', methods=['GET'])
def get_book_summary(book_id):
    """Résumé d'un livre"""
    try:
        style = request.args.get('style', 'standard')
        summary = ragtime.get_book_summary(book_id, style)
        
        return jsonify({
            'book_id': book_id,
            'style': style,
            'summary': summary
        })
        
    except Exception as e:
        logger.error(f"Erreur résumé: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/books', methods=['GET'])
def get_books():
    """Liste des livres"""
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        books = ragtime.books_data[offset:offset+limit]
        return jsonify({
            'books': books,
            'total': len(ragtime.books_data),
            'limit': limit,
            'offset': offset
        })
        
    except Exception as e:
        logger.error(f"Erreur liste livres: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Statistiques"""
    try:
        return jsonify({
            'total_books': len(ragtime.books_data),
            'total_summaries': len(ragtime.book_summaries),
            'ai_enabled': False,
            'ai_models': []
        })
        
    except Exception as e:
        logger.error(f"Erreur statistiques: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Démarrage Simple RagTime API sur le port {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 