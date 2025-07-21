#!/usr/bin/env python3
"""
Script d'initialisation du RAG Doki
Crée l'index pickle optimisé avec la documentation Dokos
"""

import os
import sys
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import re
import unicodedata
from pathlib import Path

# Configuration
DOCS_DIR = "dokos-doc/content"
INDEX_FILE = "index.pkl"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def clean_text(text):
    """Nettoie le texte pour la comparaison"""
    text = re.sub(r'(\*\*|__|\*|_)', '', text)
    text = text.lower()
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text

def extract_concepts_from_text(text):
    """Extrait les concepts métiers du texte"""
    concepts = set()
    keywords = [
        ('doctype', ['doctype', 'type de document']),
        ('utilisateur', ['utilisateur', 'user', 'users']),
        ('impression', ['impression', 'print', 'imprimer']),
        ('workflow', ['workflow', 'flux de travail']),
        ('api', ['api', 'endpoint', 'rest']),
        ('personnalisation', ['personnalisation', 'custom', 'personnaliser']),
        ('rapport', ['rapport', 'report']),
        ('module', ['module']),
        ('champ', ['champ', 'field']),
        ('formulaire', ['formulaire', 'form']),
        ('comptabilité', ['comptabilité', 'compta', 'comptable']),
        ('ventes', ['ventes', 'vente', 'commercial']),
        ('stocks', ['stocks', 'stock', 'inventaire']),
        ('production', ['production', 'produire']),
        ('rh', ['rh', 'ressources humaines', 'employé']),
        ('achats', ['achats', 'achat', 'fournisseur']),
        ('projets', ['projets', 'projet']),
        ('actifs', ['actifs', 'actif', 'immobilisation']),
        ('crm', ['crm', 'client', 'prospect']),
        ('lieu', ['lieu', 'site', 'établissement']),
        ('chantiers', ['chantiers', 'chantier', 'travaux']),
        ('e-commerce', ['e-commerce', 'boutique', 'magasin en ligne']),
        ('intégrations', ['intégrations', 'intégration', 'connecteur']),
        ('qualité', ['qualité', 'contrôle qualité']),
        ('support', ['support', 'assistance']),
        ('paramétrage', ['paramétrage', 'paramètre', 'configuration']),
    ]
    norm_text = text.lower()
    for concept, mots in keywords:
        for mot in mots:
            if mot in norm_text:
                concepts.add(concept)
    return list(concepts)

def extract_themes_from_path(file_path):
    """Extrait les thèmes à partir du chemin du fichier"""
    themes = []
    path_parts = file_path.lower().split('/')
    
    # Mapping des dossiers vers thèmes
    theme_mapping = {
        '1.dokos': 'dokos',
        '3.dodock': 'dodock',
        '4.integrations': 'intégrations',
        '5.federation-lieux': 'federation-lieux',
        '6.toobibpro': 'toobibpro',
        'paramétrage': 'paramétrage',
        'comptabilité': 'comptabilité',
        'ventes': 'ventes',
        'stocks': 'stocks',
        'production': 'production',
        'rh': 'rh',
        'achats': 'achats',
        'projets': 'projets',
        'actifs': 'actifs',
        'crm': 'crm',
        'lieu': 'lieu',
        'chantiers': 'chantiers',
        'e-commerce': 'e-commerce',
        'qualité': 'qualité',
        'support': 'support',
        'api': 'api',
        'workflow': 'workflow',
        'doctype': 'doctype',
        'champ': 'champ',
        'formulaire': 'formulaire',
        'rapport': 'rapport',
        'personnalisation': 'personnalisation',
    }
    
    for part in path_parts:
        for key, theme in theme_mapping.items():
            if key in part:
                themes.append(theme)
    
    return list(set(themes))

def parse_markdown_file(file_path):
    """Parse un fichier Markdown et extrait les sections"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Erreur lecture {file_path}: {e}")
        return []
    
    sections = []
    lines = content.split('\n')
    current_section = None
    current_text = []
    
    for line in lines:
        # Détection des titres
        if line.startswith('#'):
            # Sauvegarder la section précédente
            if current_section:
                current_section['text'] = '\n'.join(current_text)
                sections.append(current_section)
            
            # Nouvelle section
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('#').strip()
            current_section = {
                'title': title,
                'level': level,
                'file': str(file_path),
                'text': '',
                'concepts': [],
                'themes': extract_themes_from_path(str(file_path))
            }
            current_text = []
        else:
            if current_section:
                current_text.append(line)
    
    # Ajouter la dernière section
    if current_section:
        current_section['text'] = '\n'.join(current_text)
        sections.append(current_section)
    
    # Extraire les concepts pour chaque section
    for section in sections:
        full_text = f"{section['title']} {section['text']}"
        section['concepts'] = extract_concepts_from_text(full_text)
    
    return sections

def build_index():
    """Construit l'index complet"""
    print("🔍 Initialisation du RAG Doki...")
    
    # Vérifier que le dossier de docs existe
    if not os.path.exists(DOCS_DIR):
        print(f"❌ Dossier {DOCS_DIR} non trouvé")
        return False
    
    # Charger le modèle d'embeddings
    print("📥 Chargement du modèle d'embeddings...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    # Parcourir tous les fichiers Markdown
    print("📚 Parcours de la documentation...")
    all_sections = []
    
    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"  📄 {file_path}")
                sections = parse_markdown_file(file_path)
                all_sections.extend(sections)
    
    print(f"✅ {len(all_sections)} sections trouvées")
    
    # Générer les embeddings
    print("🧠 Génération des embeddings...")
    for i, section in enumerate(all_sections):
        if i % 100 == 0:
            print(f"  📊 {i}/{len(all_sections)} sections traitées")
        
        # Texte pour l'embedding
        text_for_embedding = f"{section['title']} {section['text']}"
        if len(text_for_embedding.strip()) > 0:
            try:
                embedding = model.encode(text_for_embedding)
                section['embedding'] = embedding
            except Exception as e:
                print(f"⚠️ Erreur embedding pour {section['file']}: {e}")
                section['embedding'] = None
        else:
            section['embedding'] = None
    
    # Filtrer les sections sans embedding
    valid_sections = [s for s in all_sections if s['embedding'] is not None]
    print(f"✅ {len(valid_sections)} sections avec embeddings valides")
    
    # Sauvegarder l'index
    print("💾 Sauvegarde de l'index...")
    with open(INDEX_FILE, 'wb') as f:
        pickle.dump(valid_sections, f)
    
    print(f"🎉 Index sauvegardé dans {INDEX_FILE}")
    print(f"📊 Statistiques:")
    print(f"   - Sections totales: {len(valid_sections)}")
    print(f"   - Fichiers traités: {len(set(s['file'] for s in valid_sections))}")
    
    # Statistiques par thème
    theme_counts = {}
    for section in valid_sections:
        for theme in section['themes']:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
    
    print(f"   - Thèmes trouvés: {len(theme_counts)}")
    for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"     • {theme}: {count} sections")
    
    return True

if __name__ == "__main__":
    success = build_index()
    if success:
        print("\n🚀 Le RAG Doki est maintenant prêt !")
        print("Vous pouvez lancer: python search_dokos_docs.py")
    else:
        print("\n❌ Échec de l'initialisation")
        sys.exit(1) 