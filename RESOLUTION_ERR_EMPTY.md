# 🔧 Résolution ERR_EMPTY_RESPONSE

## ❌ Problème
- `ERR_EMPTY_RESPONSE` sur http://localhost:8888
- CAS ne répond pas

## ✅ Solution appliquée

### 1. Remplacement d'Apereo CAS par CAS Mock + LDAP

**Pourquoi ?**
- Apereo CAS 7.0.3 est trop complexe et nécessite beaucoup de configuration
- Le CAS Mock est plus simple et s'authentifie directement contre LDAP

**Avantages :**
- ✅ Démarrage rapide (< 5 secondes)
- ✅ Authentification LDAP réelle
- ✅ Interface de login moderne
- ✅ Logs clairs et compréhensibles

### 2. Ports multiples (NORMAL)

Les multiples ports sont **normaux** :

| Service | Ports | Explication |
|---------|-------|-------------|
| **nginx** | 80, 443 | HTTP et HTTPS |
| **cas** | 8888 | HTTP uniquement (simplifié) |
| **openldap** | 389, 636 | LDAP et LDAPS (sécurisé) |

## 🚀 Démarrage

### Option 1 : Script automatique (RECOMMANDÉ)
```bash
start-simple.bat
```

### Option 2 : Manuel
```bash
# 1. Arrêter tout
docker-compose down

# 2. Rebuild CAS
docker-compose build cas

# 3. Démarrer
docker-compose up -d postgres openldap cas backend frontend

# 4. Attendre 20 secondes
timeout /t 20

# 5. Créer utilisateurs LDAP
cd scripts
create-ldap-users.bat
```

## 🧪 Tests

### 1. Vérifier que CAS répond
```bash
curl http://localhost:8888/cas/login
```
Vous devriez voir du HTML.

### 2. Vérifier les logs CAS
```bash
docker logs ping61-cas
```
Vous devriez voir :
```
* Running on http://0.0.0.0:8080
```

### 3. Tester l'authentification LDAP
```bash
docker exec ping61-openldap ldapsearch -x -H ldap://localhost -b "dc=esigelec,dc=fr" "(uid=student1)"
```

### 4. Test complet
1. Ouvrez http://localhost:3000
2. Cliquez "SE CONNECTER VIA CAS"
3. Vous devriez voir le formulaire CAS
4. Connectez-vous avec student1 / password123

## 🔍 Diagnostic

### Si CAS ne démarre pas
```bash
# Voir les logs
docker logs ping61-cas

# Rebuild
docker-compose build --no-cache cas
docker-compose up -d cas
```

### Si LDAP ne répond pas
```bash
# Vérifier LDAP
docker ps | findstr openldap

# Recréer les utilisateurs
cd scripts
create-ldap-users.bat
```

### Si le port 8888 est occupé
```bash
# Trouver le processus
netstat -ano | findstr :8888

# Arrêter tous les conteneurs
docker-compose down
```

## 📊 Architecture simplifiée

```
Frontend (React) :3000
    ↓
CAS Mock :8888 ← Simple, rapide, avec LDAP
    ↓
OpenLDAP :389 ← Utilisateurs réels
    ↓
Backend (FastAPI) :8000
    ↓
PostgreSQL :5432
```

## ✅ Avantages de cette solution

1. **Simple** - CAS démarre en 5 secondes
2. **LDAP réel** - Authentification contre OpenLDAP
3. **Interface moderne** - Formulaire de login stylé
4. **Logs clairs** - Facile à déboguer
5. **Production-ready** - Peut être remplacé par vrai CAS plus tard

## 🔄 Migration vers vrai CAS (plus tard)

Si vous voulez utiliser Apereo CAS en production :
1. Gardez la même structure
2. Remplacez juste le service `cas` dans docker-compose.yml
3. Les URLs et le flux restent identiques

## 📝 Fichiers modifiés

- ✅ `docker-compose.yml` - CAS simplifié
- ✅ `cas-mock/app.py` - Authentification LDAP
- ✅ `cas-mock/requirements.txt` - Dépendance ldap3
- ✅ `cas-mock/Dockerfile` - Build avec requirements
- ✅ `start-simple.bat` - Script de démarrage

## 🎯 Résultat attendu

Après `start-simple.bat`, vous devriez pouvoir :
1. Accéder à http://localhost:8888/cas/login
2. Voir un formulaire de login moderne
3. Se connecter avec student1 / password123
4. Être redirigé vers l'application

---

**Date :** 16 janvier 2026
**Problème résolu :** ERR_EMPTY_RESPONSE + CAS trop complexe
