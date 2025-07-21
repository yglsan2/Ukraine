#!/usr/bin/env python3
"""
Script pour corriger les embeddings numpy
"""

import pickle
import numpy as np
import json

def fix_embeddings():
    """Corrige les embeddings numpy"""
    print("🔧 Correction des embeddings numpy...")
    
    try:
        # Charger l'index actuel
        with open("books_index.pkl", "rb") as f:
            index_data = pickle.load(f)
        
        print(f"📊 Index chargé: {len(index_data['embeddings'])} embeddings")
        
        # Convertir les embeddings en listes Python
        embeddings_list = []
        for emb in index_data['embeddings']:
            if isinstance(emb, np.ndarray):
                embeddings_list.append(emb.tolist())
            else:
                embeddings_list.append(emb)
        
        # Créer le nouvel index
        new_index_data = {
            'embeddings': embeddings_list,
            'concepts': index_data['concepts']
        }
        
        # Sauvegarder le nouvel index
        with open("books_index_fixed.pkl", "wb") as f:
            pickle.dump(new_index_data, f)
        
        print("✅ Nouvel index créé: books_index_fixed.pkl")
        
        # Remplacer l'ancien index
        import os
        os.rename("books_index.pkl", "books_index_old.pkl")
        os.rename("books_index_fixed.pkl", "books_index.pkl")
        
        print("✅ Index corrigé et remplacé")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    fix_embeddings() 