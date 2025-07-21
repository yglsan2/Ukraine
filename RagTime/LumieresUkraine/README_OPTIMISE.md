# 🚀 RagTime API - Version Optimisée

## ✨ Nouvelles Fonctionnalités

### 🔧 **Singleton Pattern**
- **Une seule instance** : Évite la multiplication des processus
- **Initialisation lazy** : L'API se charge seulement quand nécessaire
- **Thread-safe** : Gestion sécurisée des accès concurrents

### 💾 **Cache Mémoire Intelligent**
- **LRU Cache** : 100 recherches en cache par défaut
- **TTL 24h** : Expiration automatique des résultats
- **Clés uniques** : Query + filtres + mode IA
- **Thread-safe** : Accès concurrent sécurisé

### 🔄 **NumpyEncoder Automatique**
- **Conversion automatique** : Tous les types numpy gérés
- **Robuste** : Gestion d'erreurs et fallbacks
- **Performance** : Pas de conversion manuelle

### 🛠️ **Gestion Automatique**
- **Nettoyage automatique** : Cache vidé à la fermeture
- **Scripts de gestion** : Démarrage/arrêt/redémarrage
- **Monitoring** : Statuts et statistiques en temps réel

## 🚀 Utilisation

### Démarrage Simple
```bash
# Démarrage classique
python3 ragtime_api.py

# Ou avec le gestionnaire
python3 manage_ragtime.py start
```

### Gestion Avancée
```bash
# Voir le statut
python3 manage_ragtime.py status

# Redémarrer
python3 manage_ragtime.py restart

# Tester l'API
python3 manage_ragtime.py test

# Vider le cache
python3 manage_ragtime.py clear-cache
```

## 📊 Endpoints de Monitoring

### Cache
```bash
# Statistiques du cache
GET /api/cache/stats

# Vider le cache
POST /api/cache/clear
```

### Système
```bash
# Statut complet
GET /api/system/status

# Santé de l'API
GET /api/health
```

## 🔧 Configuration

### Cache
```python
# Dans SearchCache.__init__()
max_size=100,      # Nombre max d'entrées
ttl_hours=24       # Durée de vie en heures
```

### Singleton
```python
# Accès automatique
ragtime_api = ragtime_singleton.get_api()
cache = ragtime_singleton.get_cache()
```

## 📈 Avantages

### Performance
- **Cache hit** : Réponses instantanées pour les recherches répétées
- **Mémoire optimisée** : Pas de duplication de données
- **CPU réduit** : Moins de calculs vectoriels

### Fiabilité
- **Pas de processus multiples** : Évite les conflits
- **Gestion d'erreurs** : Fallbacks robustes
- **Nettoyage automatique** : Pas de fuites mémoire

### Maintenabilité
- **Code simplifié** : Moins de conversions manuelles
- **Monitoring intégré** : Statistiques en temps réel
- **Scripts de gestion** : Administration facilitée

## 🎯 Exemples d'Utilisation

### Recherche avec Cache
```python
# Première recherche (cache miss)
result1 = api.search("livres Ukraine")
# → Calcul vectoriel + IA

# Deuxième recherche identique (cache hit)
result2 = api.search("livres Ukraine")
# → Réponse instantanée du cache
```

### Monitoring
```python
# Voir les statistiques
stats = requests.get('/api/cache/stats').json()
print(f"Cache: {stats['size']}/{stats['max_size']} entrées")

# Voir le statut système
status = requests.get('/api/system/status').json()
print(f"Livres: {status['books_count']}")
print(f"IA: {status['ai_status']['enabled']}")
```

## 🔍 Dépannage

### Problème de Port
```bash
# Vérifier les processus
python3 manage_ragtime.py status

# Arrêter proprement
python3 manage_ragtime.py stop

# Redémarrer
python3 manage_ragtime.py restart
```

### Cache Plein
```bash
# Vider le cache
python3 manage_ragtime.py clear-cache

# Ou via API
curl -X POST http://localhost:5000/api/cache/clear
```

### Performance
```bash
# Voir les stats du cache
curl http://localhost:5000/api/cache/stats

# Tester une recherche
python3 manage_ragtime.py test
```

## 🎉 Résultat

**RagTime API est maintenant :**
- ✅ **Plus rapide** : Cache intelligent
- ✅ **Plus fiable** : Singleton + gestion d'erreurs
- ✅ **Plus simple** : NumpyEncoder automatique
- ✅ **Plus maintenable** : Scripts de gestion
- ✅ **Plus économe** : Pas de processus multiples

**L'application est prête pour la production !** 🚀✨ 