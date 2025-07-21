#!/usr/bin/env python3
"""
Résumés Intelligents sans IA - Système de génération automatique
Utilise des algorithmes sophistiqués pour créer des résumés de qualité
"""

import json
import re
import os
from datetime import datetime
from typing import Dict, List, Tuple
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np

class SmartSummaryGenerator:
    def __init__(self, data_path: str = "books_data.json"):
        self.data_path = data_path
        self.books_data = []
        self.summaries = {}
        
        # Mots-clés par thème pour améliorer les résumés
        self.theme_keywords = {
            'amitié': ['ami', 'amitié', 'solidarité', 'entraide', 'groupe', 'camaraderie', 'lien'],
            'aventure': ['aventure', 'voyage', 'découverte', 'exploration', 'quête', 'pérégrination', 'expédition'],
            'famille': ['famille', 'parent', 'enfant', 'frère', 'sœur', 'mère', 'père', 'foyer', 'génération'],
            'guerre': ['guerre', 'conflit', 'paix', 'résistance', 'liberté', 'combat', 'batailles', 'armée'],
            'nature': ['nature', 'animal', 'forêt', 'mer', 'montagne', 'environnement', 'faune', 'flore', 'paysage'],
            'culture': ['culture', 'tradition', 'coutume', 'festival', 'art', 'patrimoine', 'héritage', 'cérémonie'],
            'éducation': ['école', 'apprentissage', 'connaissance', 'savoir', 'étude', 'enseignement', 'formation'],
            'amour': ['amour', 'romance', 'sentiment', 'cœur', 'passion', 'affection', 'tendresse', 'émotion'],
            'mystère': ['mystère', 'énigme', 'secret', 'suspense', 'policier', 'intrigue', 'enquête'],
            'fantasy': ['magie', 'fantastique', 'créature', 'sort', 'royaume', 'enchantement', 'mythologie'],
            'histoire': ['historique', 'passé', 'époque', 'événement', 'personnage', 'chronique', 'mémoire'],
            'science': ['science', 'technologie', 'découverte', 'invention', 'expérience', 'recherche', 'innovation'],
            'philosophie': ['philosophie', 'réflexion', 'question', 'pensée', 'sagesse', 'méditation', 'contemplation'],
            'humour': ['humour', 'comique', 'drôle', 'rire', 'amusement', 'gaieté', 'joie'],
            'émotion': ['émotion', 'sentiment', 'joie', 'tristesse', 'peur', 'espoir', 'mélancolie', 'passion']
        }
        
        # Templates de résumés par style
        self.summary_templates = {
            "bref": [
                "« {title} » par {author} - {genre}. {key_sentence}",
                "{title} de {author} explore {theme}. {key_sentence}",
                "Dans {title}, {author} nous plonge dans {theme}. {key_sentence}"
            ],
            "standard": [
                "« {title} » par {author} est un {genre} qui explore {theme}. {description_summary}",
                "L'œuvre de {author}, {title}, nous transporte dans {theme}. {description_summary}",
                "À travers {title}, {author} aborde {theme} avec {genre}. {description_summary}"
            ],
            "littéraire": [
                "Dans une prose {style_adj}, {author} nous offre {title}, une {genre} qui {action}. {description_summary}",
                "Avec {title}, {author} signe une {genre} {style_adj} où {theme} prend tout son sens. {description_summary}",
                "L'écriture de {author} dans {title} révèle une {genre} {style_adj} où {theme} se déploie. {description_summary}"
            ],
            "critique": [
                "Analyse de {title} par {author} : cette {genre} explore {theme} à travers {key_elements}. {description_summary}",
                "Dans {title}, {author} propose une {genre} qui questionne {theme}. {description_summary}",
                "L'œuvre {title} de {author} offre une {genre} où {theme} est traité avec {approach}. {description_summary}"
            ],
            "détaillé": [
                "« {title} » par {author} est une {genre} majeure qui explore en profondeur {theme}. {description_summary} {additional_info}",
                "L'œuvre de {author}, {title}, constitue une {genre} importante abordant {theme}. {description_summary} {additional_info}",
                "À travers {title}, {author} nous livre une {genre} complète sur {theme}. {description_summary} {additional_info}"
            ]
        }
        
        # Adjectifs de style
        self.style_adjectives = [
            "évocatrice", "poétique", "narrative", "descriptive", "émouvante", 
            "captivante", "intense", "subtile", "puissante", "délicate"
        ]
        
        # Actions littéraires
        self.literary_actions = [
            "nous transporte", "nous émeut", "nous interroge", "nous surprend",
            "nous touche", "nous inspire", "nous bouleverse", "nous émerveille"
        ]
        
        # Approches critiques
        self.critical_approaches = [
            "finesse", "profondeur", "originalité", "sensibilité", "rigueur",
            "créativité", "authenticité", "modernité", "universalité"
        ]
        
        self.load_data()
        self.initialize_nltk()
    
    def initialize_nltk(self):
        """Initialise NLTK pour l'analyse de texte"""
        try:
            # Téléchargement des ressources NLTK si nécessaire
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except Exception as e:
            print(f"⚠️ NLTK non disponible: {e}")
    
    def load_data(self):
        """Charge les données des livres"""
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.books_data = json.load(f)
            print(f"📚 {len(self.books_data)} livres chargés")
        else:
            print(f"❌ Fichier {self.data_path} non trouvé")
    
    def extract_themes(self, text: str) -> List[str]:
        """Extrait les thèmes d'un texte"""
        text_lower = text.lower()
        themes = []
        
        for theme, keywords in self.theme_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                themes.append(theme)
        
        return themes
    
    def extract_key_sentence(self, description: str, max_length: int = 100) -> str:
        """Extrait la phrase la plus importante d'une description"""
        if not description:
            return ""
        
        # Tokenisation des phrases
        try:
            sentences = sent_tokenize(description)
        except:
            # Fallback simple
            sentences = description.split('.')
        
        if not sentences:
            return description[:max_length]
        
        # Score des phrases basé sur la longueur et les mots-clés
        sentence_scores = []
        for sentence in sentences:
            if len(sentence.strip()) < 10:
                continue
            
            score = 0
            sentence_lower = sentence.lower()
            
            # Bonus pour la longueur modérée
            if 20 <= len(sentence) <= 80:
                score += 2
            
            # Bonus pour les mots-clés thématiques
            for keywords in self.theme_keywords.values():
                if any(keyword in sentence_lower for keyword in keywords):
                    score += 1
            
            # Bonus pour les mots importants
            important_words = ['histoire', 'récit', 'roman', 'livre', 'œuvre', 'auteur', 'personnage']
            if any(word in sentence_lower for word in important_words):
                score += 1
            
            sentence_scores.append((sentence.strip(), score))
        
        # Sélection de la meilleure phrase
        if sentence_scores:
            best_sentence = max(sentence_scores, key=lambda x: x[1])[0]
            return best_sentence[:max_length]
        else:
            return sentences[0][:max_length] if sentences else description[:max_length]
    
    def summarize_description(self, description: str, max_length: int = 150) -> str:
        """Résume une description en gardant les éléments essentiels"""
        if not description:
            return ""
        
        if len(description) <= max_length:
            return description
        
        # Extraction des phrases clés
        try:
            sentences = sent_tokenize(description)
        except:
            sentences = description.split('.')
        
        summary_parts = []
        current_length = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if current_length + len(sentence) <= max_length:
                summary_parts.append(sentence)
                current_length += len(sentence)
            else:
                break
        
        if summary_parts:
            return ' '.join(summary_parts)
        else:
            return description[:max_length] + "..."
    
    def get_additional_info(self, book: Dict) -> str:
        """Génère des informations supplémentaires pour les résumés détaillés"""
        info_parts = []
        
        # Informations sur l'auteur
        author = book.get('author', '')
        if author:
            info_parts.append(f"L'auteur {author}")
        
        # Informations sur le genre
        genre = book.get('genre', '')
        if genre:
            info_parts.append(f"ce {genre}")
        
        # Informations sur la langue
        language = book.get('language', '')
        if language and language != 'Français':
            info_parts.append(f"en {language}")
        
        # Informations sur la ville
        city = book.get('city', '')
        if city:
            info_parts.append(f"disponible à {city}")
        
        if info_parts:
            return f" {' '.join(info_parts)}."
        else:
            return ""
    
    def generate_smart_summary(self, book: Dict, style: str = "standard") -> str:
        """Génère un résumé intelligent sans IA"""
        title = book.get('title', 'Sans titre')
        author = book.get('author', 'Auteur inconnu')
        genre = book.get('genre', 'œuvre')
        description = book.get('description', '')
        
        # Extraction des thèmes
        full_text = f"{title} {description} {genre}"
        themes = self.extract_themes(full_text)
        theme = themes[0] if themes else "l'humain"
        
        # Extraction de la phrase clé
        key_sentence = self.extract_key_sentence(description, 80)
        
        # Résumé de la description
        description_summary = self.summarize_description(description, 120)
        
        # Informations supplémentaires
        additional_info = self.get_additional_info(book)
        
        # Sélection du template
        templates = self.summary_templates.get(style, self.summary_templates["standard"])
        template = np.random.choice(templates)
        
        # Remplissage du template
        summary = template.format(
            title=title,
            author=author,
            genre=genre,
            theme=theme,
            key_sentence=key_sentence,
            description_summary=description_summary,
            additional_info=additional_info,
            style_adj=np.random.choice(self.style_adjectives),
            action=np.random.choice(self.literary_actions),
            approach=np.random.choice(self.critical_approaches),
            key_elements="plusieurs éléments narratifs"
        )
        
        return summary.strip()
    
    def generate_all_summaries(self, style: str = "standard"):
        """Génère tous les résumés pour tous les livres"""
        print(f"\n🧠 Génération de tous les résumés intelligents ({style})...")
        print(f"📊 {len(self.books_data)} livres à traiter")
        
        start_time = datetime.now()
        successful = 0
        
        for i, book in enumerate(self.books_data):
            try:
                print(f"\n📖 [{i+1}/{len(self.books_data)}] {book.get('title', 'Sans titre')}")
                
                summary = self.generate_smart_summary(book, style)
                
                # Stockage du résumé
                book_id = book.get('id', i)
                self.summaries[book_id] = {
                    'summary': summary,
                    'style': style,
                    'generated_at': datetime.now().isoformat(),
                    'method': 'smart_algorithm'
                }
                
                print(f"   ✅ Résumé généré ({len(summary)} caractères)")
                print(f"   📝 {summary[:80]}...")
                successful += 1
                
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
        
        total_time = (datetime.now() - start_time).total_seconds()
        
        print(f"\n🎉 Génération terminée !")
        print(f"   ✅ Succès: {successful}")
        print(f"   ⏱️ Temps total: {total_time:.1f}s")
        print(f"   ⚡ Temps moyen par livre: {total_time/len(self.books_data):.3f}s")
    
    def save_summaries(self, filename: str = "smart_summaries.json"):
        """Sauvegarde tous les résumés"""
        summary_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_books': len(self.books_data),
                'total_summaries': len(self.summaries),
                'method': 'smart_algorithm'
            },
            'summaries': self.summaries
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Résumés sauvegardés dans {filename}")
        print(f"   📊 {len(self.summaries)} résumés sauvegardés")
    
    def load_summaries(self, filename: str = "smart_summaries.json"):
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
        avg_length = sum(len(s['summary']) for s in self.summaries.values()) / total_summaries
        
        print(f"\n📊 Statistiques des résumés intelligents:")
        print(f"   📚 Total: {total_summaries}")
        print(f"   📏 Longueur moyenne: {avg_length:.0f} caractères")
        print(f"   🧠 Méthode: Algorithme intelligent")
        
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
    generator = SmartSummaryGenerator()
    
    print("🧠 Générateur de Résumés Intelligents")
    print("=" * 50)
    
    while True:
        print("\nOptions disponibles:")
        print("1. Générer tous les résumés intelligents")
        print("2. Charger résumés existants")
        print("3. Afficher statistiques")
        print("4. Tester un résumé")
        print("5. Quitter")
        
        choice = input("\nVotre choix (1-5): ").strip()
        
        if choice == '1':
            print("\nStyles disponibles:")
            styles = ["bref", "standard", "littéraire", "critique", "détaillé"]
            for i, style in enumerate(styles):
                print(f"{i+1}. {style}")
            
            style_choice = input("\nChoisissez un style (numéro): ").strip()
            style = styles[int(style_choice) - 1] if style_choice.isdigit() and 1 <= int(style_choice) <= len(styles) else "standard"
            
            generator.generate_all_summaries(style)
            generator.save_summaries()
        
        elif choice == '2':
            generator.load_summaries()
        
        elif choice == '3':
            generator.get_summary_stats()
        
        elif choice == '4':
            if not generator.books_data:
                print("❌ Aucun livre chargé")
                continue
            
            print("Livres disponibles:")
            for i, book in enumerate(generator.books_data[:10]):
                print(f"{i+1}. {book['title']} par {book['author']}")
            
            try:
                book_id = int(input("\nChoisissez un livre (numéro): ")) - 1
                if 0 <= book_id < len(generator.books_data):
                    book = generator.books_data[book_id]
                    
                    print("\nStyles disponibles:")
                    styles = ["bref", "standard", "littéraire", "critique", "détaillé"]
                    for i, style in enumerate(styles):
                        print(f"{i+1}. {style}")
                    
                    style_choice = input("\nChoisissez un style (numéro): ").strip()
                    style = styles[int(style_choice) - 1] if style_choice.isdigit() and 1 <= int(style_choice) <= len(styles) else "standard"
                    
                    summary = generator.generate_smart_summary(book, style)
                    print(f"\n📖 Résumé ({style}):")
                    print(summary)
                else:
                    print("❌ Numéro invalide")
            except ValueError:
                print("❌ Choix invalide")
        
        elif choice == '5':
            print("Au revoir ! 👋")
            break
        
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main() 