# 🚀 Guide de Démarrage Rapide - Lumières d'Ukraine

## 🧹 Nettoyage et Démarrage Automatique

L'application a été configurée pour éviter les conflits de ports et se réinitialiser automatiquement.

### 📋 Commandes Disponibles

#### 🚀 Démarrage Rapide (Recommandé)
```bash
# Démarrage avec nettoyage automatique
./scripts/start.sh

# Ou avec npm
npm run dev
```

#### 🧽 Démarrage avec Nettoyage Complet
```bash
# Nettoyage complet + redémarrage
./scripts/start.sh clean

# Ou avec npm
npm run dev:clean
```

#### 📱 Mode Preview (Production)
```bash
# Preview avec nettoyage automatique
./scripts/start.sh preview

# Ou avec npm
npm run preview
```

#### 🌐 Serveur HTTP Simple
```bash
# Serveur HTTP avec nettoyage automatique
./scripts/start.sh serve

# Ou avec npm
npm run serve
```

### 🛠️ Commandes de Nettoyage Manuel

```bash
# Nettoyer les ports uniquement
npm run clean:ports

# Nettoyage complet (reinstalle les dépendances)
npm run clean:all

# Script de nettoyage manuel
./scripts/cleanup.sh
```

### 🔧 Résolution de Problèmes

#### ❌ Erreur "Address already in use"
```bash
# Solution automatique
npm run clean:ports

# Ou manuellement
pkill -f "vite\|http.server\|python.*http.server"
```

#### ❌ Erreur "Connexion refused"
```bash
# Redémarrer avec nettoyage complet
npm run dev:clean
```

#### ❌ Erreur "ENOENT: no such file or directory"
```bash
# Vérifier le répertoire de travail
pwd
# Doit être dans /home/yglsan/Desktop/Ukraine/frontend-vue

# Si pas dans le bon répertoire
cd /home/yglsan/Desktop/Ukraine/frontend-vue
```

### 🌐 Ports Utilisés

- **5173** : Serveur de développement Vite
- **4173** : Serveur de preview Vite
- **8080** : Serveur HTTP Python (mode production)
- **3001** : Port alternatif (si 8080 occupé)

### 📱 Accès à l'Application

Une fois démarrée, l'application sera accessible sur :
- **Développement** : http://localhost:5173
- **Preview** : http://localhost:4173
- **Production** : http://localhost:8080

### 🎯 Conseils d'Utilisation

1. **Toujours utiliser `./scripts/start.sh`** pour un démarrage propre
2. **En cas de problème**, utiliser `npm run dev:clean` pour un nettoyage complet
3. **Fermer proprement** avec Ctrl+C pour déclencher le nettoyage automatique
4. **Vérifier les ports** avec `lsof -i :5173 -i :4173 -i :8080`

### 🔄 Réinitialisation Automatique

L'application se réinitialise automatiquement :
- ✅ À chaque démarrage
- ✅ À chaque fermeture (Ctrl+C)
- ✅ En cas de conflit de ports
- ✅ En cas d'erreur de connexion

### 🚨 En Cas d'Urgence

Si rien ne fonctionne :
```bash
# Arrêter tous les processus
pkill -f "node\|vite\|python"

# Nettoyer complètement
rm -rf node_modules package-lock.json
npm install

# Redémarrer
./scripts/start.sh
``` 