#!/usr/bin/env python3
"""
Test de comparaison entre RagTime Pur et RagTime avec IA
Évalue les performances, fonctionnalités et expérience utilisateur
"""

import time
import json
import os
from datetime import datetime

def test_ragtime_pure():
    """Teste RagTime Pur"""
    print("🧪 Test de RagTime Pur...")
    
    try:
        from ragtime_enhanced import RagTimeEnhanced
        
        start_time = time.time()
        ragtime = RagTimeEnhanced()
        init_time = time.time() - start_time
        
        print(f"✅ Initialisation: {init_time:.2f}s")
        
        # Test de recherche
        queries = [
            "romans d'aventure",
            "livres pour enfants",
            "fantasy ukrainienne",
            "livres disponibles à Paris",
            "romans policiers en français"
        ]
        
        search_times = []
        results_count = []
        
        for query in queries:
            start_time = time.time()
            results = ragtime.search_books(query)
            search_time = time.time() - start_time
            
            search_times.append(search_time)
            results_count.append(len(results))
            
            print(f"   Recherche '{query}': {search_time:.3f}s, {len(results)} résultats")
        
        # Test des recommandations
        start_time = time.time()
        recommendations = ragtime.get_recommendations("user123")
        rec_time = time.time() - start_time
        
        print(f"✅ Recommandations: {rec_time:.3f}s, {len(recommendations)} livres")
        
        # Test des statistiques
        start_time = time.time()
        stats = ragtime.get_statistics()
        stats_time = time.time() - start_time
        
        print(f"✅ Statistiques: {stats_time:.3f}s")
        
        return {
            "success": True,
            "init_time": init_time,
            "avg_search_time": sum(search_times) / len(search_times),
            "max_search_time": max(search_times),
            "avg_results": sum(results_count) / len(results_count),
            "recommendations_time": rec_time,
            "stats_time": stats_time,
            "total_books": stats['total_books']
        }
        
    except Exception as e:
        print(f"❌ Erreur RagTime Pur: {e}")
        return {"success": False, "error": str(e)}

def test_ragtime_with_ai():
    """Teste RagTime avec IA"""
    print("\n🤖 Test de RagTime avec IA...")
    
    try:
        from ragtime_with_ai import RagTimeWithAI
        
        start_time = time.time()
        ragtime = RagTimeWithAI()
        init_time = time.time() - start_time
        
        print(f"✅ Initialisation: {init_time:.2f}s")
        print(f"   IA disponible: {'Oui' if ragtime.ai_available else 'Non'}")
        
        if not ragtime.ai_available:
            return {
                "success": False,
                "error": "Ollama non disponible",
                "init_time": init_time
            }
        
        # Test de recherche avec IA
        queries = [
            "romans d'aventure",
            "livres pour enfants",
            "fantasy ukrainienne"
        ]
        
        search_times = []
        ai_response_times = []
        
        for query in queries:
            start_time = time.time()
            results = ragtime.search_books_with_ai(query)
            total_time = time.time() - start_time
            
            search_times.append(total_time)
            
            print(f"   Recherche IA '{query}': {total_time:.3f}s")
            print(f"      Réponse IA: {len(results['ai_response'])} caractères")
        
        # Test de génération de résumé
        if len(ragtime.books_data) > 0:
            start_time = time.time()
            summary = ragtime.generate_book_summary(0)
            summary_time = time.time() - start_time
            
            print(f"✅ Résumé IA: {summary_time:.3f}s, {len(summary)} caractères")
        else:
            summary_time = 0
        
        # Test de recommandations IA
        start_time = time.time()
        ai_rec = ragtime.generate_recommendations_ai("user123")
        ai_rec_time = time.time() - start_time
        
        print(f"✅ Recommandations IA: {ai_rec_time:.3f}s, {len(ai_rec)} caractères")
        
        return {
            "success": True,
            "ai_available": True,
            "init_time": init_time,
            "avg_search_time": sum(search_times) / len(search_times),
            "max_search_time": max(search_times),
            "summary_time": summary_time,
            "recommendations_ai_time": ai_rec_time,
            "total_books": len(ragtime.books_data)
        }
        
    except Exception as e:
        print(f"❌ Erreur RagTime avec IA: {e}")
        return {"success": False, "error": str(e)}

def compare_results(pure_results, ai_results):
    """Compare les résultats des deux approches"""
    print("\n" + "="*60)
    print("📊 COMPARAISON DES RÉSULTATS")
    print("="*60)
    
    if not pure_results["success"]:
        print("❌ RagTime Pur: ÉCHEC")
        print(f"   Erreur: {pure_results.get('error', 'Inconnue')}")
        return
    
    print("✅ RagTime Pur: SUCCÈS")
    print(f"   Initialisation: {pure_results['init_time']:.2f}s")
    print(f"   Recherche moyenne: {pure_results['avg_search_time']:.3f}s")
    print(f"   Recherche max: {pure_results['max_search_time']:.3f}s")
    print(f"   Recommandations: {pure_results['recommendations_time']:.3f}s")
    print(f"   Statistiques: {pure_results['stats_time']:.3f}s")
    print(f"   Livres indexés: {pure_results['total_books']}")
    
    if not ai_results["success"]:
        print("\n❌ RagTime avec IA: ÉCHEC")
        print(f"   Erreur: {ai_results.get('error', 'Inconnue')}")
        return
    
    print("\n✅ RagTime avec IA: SUCCÈS")
    print(f"   Initialisation: {ai_results['init_time']:.2f}s")
    print(f"   IA disponible: {'Oui' if ai_results.get('ai_available', False) else 'Non'}")
    print(f"   Recherche moyenne: {ai_results['avg_search_time']:.3f}s")
    print(f"   Recherche max: {ai_results['max_search_time']:.3f}s")
    print(f"   Résumé IA: {ai_results['summary_time']:.3f}s")
    print(f"   Recommandations IA: {ai_results['recommendations_ai_time']:.3f}s")
    print(f"   Livres indexés: {ai_results['total_books']}")
    
    # Comparaison des performances
    print("\n⚡ ANALYSE DES PERFORMANCES:")
    
    if pure_results["success"] and ai_results["success"]:
        init_ratio = ai_results['init_time'] / pure_results['init_time']
        search_ratio = ai_results['avg_search_time'] / pure_results['avg_search_time']
        
        print(f"   Initialisation: IA {init_ratio:.1f}x plus lente")
        print(f"   Recherche: IA {search_ratio:.1f}x plus lente")
        
        if search_ratio > 3:
            print("   ⚠️ L'IA ralentit significativement la recherche")
        elif search_ratio > 2:
            print("   ⚠️ L'IA ralentit modérément la recherche")
        else:
            print("   ✅ L'IA n'impacte que peu les performances")

def generate_recommendation(pure_results, ai_results):
    """Génère une recommandation basée sur les tests"""
    print("\n" + "="*60)
    print("🎯 RECOMMANDATION FINALE")
    print("="*60)
    
    if not pure_results["success"]:
        print("❌ RagTime Pur ne fonctionne pas - Vérifiez l'installation")
        return
    
    if not ai_results["success"]:
        print("✅ RECOMMANDATION: Utiliser RagTime Pur")
        print("   Raisons:")
        print("   • RagTime Pur fonctionne correctement")
        print("   • RagTime avec IA présente des problèmes")
        print("   • Performance et fiabilité optimales")
        return
    
    # Analyse comparative
    pure_score = 0
    ai_score = 0
    
    # Performance (40% du score)
    if pure_results["avg_search_time"] < ai_results["avg_search_time"]:
        pure_score += 40
    else:
        ai_score += 40
    
    # Fiabilité (30% du score)
    pure_score += 30  # Toujours fiable
    ai_score += 20    # Dépend d'Ollama
    
    # Fonctionnalités (30% du score)
    pure_score += 20  # Fonctionnalités de base
    ai_score += 30    # Fonctionnalités avancées
    
    print(f"📊 Scores: RagTime Pur {pure_score}/100, RagTime IA {ai_score}/100")
    
    if pure_score > ai_score:
        print("\n✅ RECOMMANDATION: RagTime Pur")
        print("   Avantages:")
        print("   • Performance supérieure")
        print("   • Fiabilité maximale")
        print("   • Installation et maintenance simples")
        print("   • Couvre 80% des besoins")
        print("\n   Considération IA:")
        print("   • Évaluer l'ajout d'IA après 2-3 mois d'usage")
        print("   • Si les utilisateurs demandent plus d'intelligence")
    else:
        print("\n🤖 RECOMMANDATION: RagTime avec IA")
        print("   Avantages:")
        print("   • Fonctionnalités avancées")
        print("   • Expérience utilisateur enrichie")
        print("   • Génération de contenu automatique")
        print("\n   Prérequis:")
        print("   • Ressources système suffisantes")
        print("   • Maintenance plus complexe")
        print("   • Formation des utilisateurs")

def main():
    """Test principal"""
    print("🧪 TEST DE COMPARAISON RAGTIME")
    print("="*50)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Tests
    pure_results = test_ragtime_pure()
    ai_results = test_ragtime_with_ai()
    
    # Comparaison
    compare_results(pure_results, ai_results)
    
    # Recommandation
    generate_recommendation(pure_results, ai_results)
    
    # Sauvegarde des résultats
    results = {
        "date": datetime.now().isoformat(),
        "pure_results": pure_results,
        "ai_results": ai_results
    }
    
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Résultats sauvegardés dans test_results.json")

if __name__ == "__main__":
    main() 