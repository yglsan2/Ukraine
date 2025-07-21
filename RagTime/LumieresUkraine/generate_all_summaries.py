#!/usr/bin/env python3
"""
Génération de tous les résumés de livres - Script de préparation
Génère tous les résumés une fois pour toutes et les sauvegarde
"""

import json
import pickle
import time
import os
from datetime import datetime
from typing import Dict, List
import requests

class SummaryGenerator:
    def __init__(self, data_path: str = "books_data.json", ollama_url: str = "http://localhost:11434"):
        self.data_path = data_path
        self.ollama_url = ollama_url
        self.books_data = []
        self.summaries = {}
        
        # Modèles disponibles par ordre de rapidité
        self.models = {
            "qwen2": "qwen2.5:0.5b",      # Ultra-rapide
            "phi2": "phi:2.7b",           # Rapide + bon français
            "gemma2": "gemma2:2b",        # Équilibré
            "mistral": "mistral:7b-instruct"  # Qualité max
        }
        
        self.current_model = "qwen2"  # Modèle le plus rapide par défaut
        self.ai_available = False
        
        self.load_data()
        self.check_ai_availability()
    
    def load_data(self):
        """Charge les données des livres"""
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.books_data = json.load(f)
            print(f"📚 {len(self.books_data)} livres chargés")
        else:
            print(f"❌ Fichier {self.data_path} non trouvé")
    
    def check_ai_availability(self):
        """Vérifie la disponibilité des modèles IA"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = []
                
                for model_name, model_id in self.models.items():
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
                            print(f"⚡ Modèle sélectionné: {model}")
                            break
                else:
                    print("⚠️ Aucun modèle IA trouvé")
                    self.ai_available = False
            else:
                print("❌ Ollama non disponible")
                self.ai_available = False
        except Exception as e:
            print(f"❌ Erreur IA: {e}")
            self.ai_available = False
    
    def generate_summary_ai(self, book: Dict, style: str = "standard") -> str:
        """Génère un résumé avec IA"""
        if not self.ai_available:
            return self.generate_summary_fallback(book, style)
        
        # Prompts optimisés par style
        style_prompts = {
            "bref": "Résume en 2 phrases:",
            "standard": "Résume brièvement:",
            "littéraire": "Résume avec style littéraire:",
            "critique": "Fais une analyse rapide:",
            "détaillé": "Résume en détail:"
        }
        
        style_prompt = style_prompts.get(style, style_prompts["standard"])
        
        # Prompt court pour rapidité
        prompt = f"""{style_prompt}

Titre: {book.get('title', 'N/A')}
Auteur: {book.get('author', 'N/A')}
Genre: {book.get('genre', 'N/A')}
Description: {book.get('description', 'N/A')[:200]}

Résumé:"""
        
        try:
            payload = {
                "model": self.models[self.current_model],
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.8,
                    "max_tokens": 150,
                    "num_ctx": 1024,
                    "repeat_penalty": 1.1
                }
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", 
                                   json=payload, timeout=15)
            
            if response.status_code == 200:
                return response.json().get('response', 'Erreur de réponse')
            else:
                return self.generate_summary_fallback(book, style)
                
        except Exception as e:
            return self.generate_summary_fallback(book, style)
    
    def generate_summary_fallback(self, book: Dict, style: str) -> str:
        """Génère un résumé sans IA - Fallback intelligent"""
        title = book.get('title', '')
        author = book.get('author', '')
        genre = book.get('genre', '')
        description = book.get('description', '')
        
        # Extraction intelligente
        summary_parts = []
        
        if title and author:
            summary_parts.append(f"« {title} » par {author}")
        
        if genre:
            summary_parts.append(f"Genre : {genre}")
        
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
    
    def generate_all_summaries(self, style: str = "standard", use_ai: bool = True):
        """Génère tous les résumés pour tous les livres"""
        print(f"\n🚀 Génération de tous les résumés ({style})...")
        print(f"📊 {len(self.books_data)} livres à traiter")
        print(f"🤖 IA utilisée: {'Oui' if use_ai and self.ai_available else 'Non'}")
        
        start_time = time.time()
        successful = 0
        failed = 0
        
        for i, book in enumerate(self.books_data):
            try:
                print(f"\n📖 [{i+1}/{len(self.books_data)}] {book.get('title', 'Sans titre')}")
                
                if use_ai and self.ai_available:
                    summary = self.generate_summary_ai(book, style)
                else:
                    summary = self.generate_summary_fallback(book, style)
                
                # Stockage du résumé
                book_id = book.get('id', i)
                self.summaries[book_id] = {
                    'summary': summary,
                    'style': style,
                    'generated_at': datetime.now().isoformat(),
                    'method': 'ai' if use_ai and self.ai_available else 'fallback'
                }
                
                print(f"   ✅ Résumé généré ({len(summary)} caractères)")
                successful += 1
                
                # Pause pour éviter de surcharger
                if use_ai and self.ai_available:
                    time.sleep(0.5)
                
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
                failed += 1
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 Génération terminée !")
        print(f"   ✅ Succès: {successful}")
        print(f"   ❌ Échecs: {failed}")
        print(f"   ⏱️ Temps total: {total_time:.1f}s")
        print(f"   ⚡ Temps moyen par livre: {total_time/len(self.books_data):.1f}s")
    
    def save_summaries(self, filename: str = "book_summaries.json"):
        """Sauvegarde tous les résumés"""
        summary_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_books': len(self.books_data),
                'total_summaries': len(self.summaries),
                'model_used': self.current_model if self.ai_available else 'fallback'
            },
            'summaries': self.summaries
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Résumés sauvegardés dans {filename}")
        print(f"   📊 {len(self.summaries)} résumés sauvegardés")
    
    def load_summaries(self, filename: str = "book_summaries.json"):
        """Charge les résumés existants"""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.summaries = data.get('summaries', {})
            
            print(f"📚 {len(self.summaries)} résumés chargés depuis {filename}")
            return True
        else:
            print(f"📚 Aucun fichier de résumés trouvé: {filename}")
            return False
    
    def get_summary_stats(self):
        """Affiche les statistiques des résumés"""
        if not self.summaries:
            print("📊 Aucun résumé généré")
            return
        
        total_summaries = len(self.summaries)
        ai_summaries = sum(1 for s in self.summaries.values() if s.get('method') == 'ai')
        fallback_summaries = total_summaries - ai_summaries
        
        avg_length = sum(len(s['summary']) for s in self.summaries.values()) / total_summaries
        
        print(f"\n📊 Statistiques des résumés:")
        print(f"   📚 Total: {total_summaries}")
        print(f"   🤖 IA: {ai_summaries}")
        print(f"   🔄 Fallback: {fallback_summaries}")
        print(f"   📏 Longueur moyenne: {avg_length:.0f} caractères")
        
        # Styles utilisés
        styles = {}
        for summary in self.summaries.values():
            style = summary.get('style', 'unknown')
            styles[style] = styles.get(style, 0) + 1
        
        print(f"   🎨 Styles:")
        for style, count in styles.items():
            print(f"      {style}: {count}")

def main():
    """Interface principale"""
    generator = SummaryGenerator()
    
    print("📚 Générateur de Résumés RagTime")
    print("=" * 50)
    
    while True:
        print("\nOptions disponibles:")
        print("1. Générer tous les résumés (avec IA)")
        print("2. Générer tous les résumés (sans IA)")
        print("3. Charger résumés existants")
        print("4. Afficher statistiques")
        print("5. Changer de modèle IA")
        print("6. Quitter")
        
        choice = input("\nVotre choix (1-6): ").strip()
        
        if choice == '1':
            if not generator.ai_available:
                print("❌ IA non disponible. Utilisez l'option 2.")
                continue
            
            print("\nStyles disponibles:")
            styles = ["bref", "standard", "littéraire", "critique", "détaillé"]
            for i, style in enumerate(styles):
                print(f"{i+1}. {style}")
            
            style_choice = input("\nChoisissez un style (numéro): ").strip()
            style = styles[int(style_choice) - 1] if style_choice.isdigit() and 1 <= int(style_choice) <= len(styles) else "standard"
            
            generator.generate_all_summaries(style, use_ai=True)
            generator.save_summaries()
        
        elif choice == '2':
            print("\nStyles disponibles:")
            styles = ["bref", "standard", "littéraire", "critique", "détaillé"]
            for i, style in enumerate(styles):
                print(f"{i+1}. {style}")
            
            style_choice = input("\nChoisissez un style (numéro): ").strip()
            style = styles[int(style_choice) - 1] if style_choice.isdigit() and 1 <= int(style_choice) <= len(styles) else "standard"
            
            generator.generate_all_summaries(style, use_ai=False)
            generator.save_summaries()
        
        elif choice == '3':
            generator.load_summaries()
        
        elif choice == '4':
            generator.get_summary_stats()
        
        elif choice == '5':
            if not generator.ai_available:
                print("❌ IA non disponible")
                continue
            
            print("Modèles disponibles:")
            for i, model in enumerate(generator.available_models):
                print(f"{i+1}. {model} - {generator.models[model]}")
            
            model_name = input("\nChoisissez un modèle: ").strip()
            if model_name in generator.available_models:
                generator.current_model = model_name
                print(f"✅ Modèle changé vers: {model_name}")
            else:
                print("❌ Modèle invalide")
        
        elif choice == '6':
            print("Au revoir ! 👋")
            break
        
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main() 