# 🔧 Résolution Erreur CORS + 401

## ❌ Problèmes identifiés

1. **CORS Error** - "No 'Access-Control-Allow-Origin' header"
2. **401 Unauthorized** - Le backend ne valide pas le ticket
3. **LAM ne s'affiche pas** - Normal, il faut attendre qu'OpenLDAP soit prêt

## ✅ Solutions

### 1. JWT_SECRET_KEY manquant
Ajouté dans `backend/app/core/config.py`

### 2. CORS déjà configuré
Le CORS est déjà dans `main.py`, mais le backend doit redémarrer

### 3. LAM attend OpenLDAP
LAM démarre seulement quand OpenLDAP est "healthy"

## 🚀 Correction rapide

```bash
fix-cors.bat
```

Ou manuellement :
```bash
docker-compose restart backend
```

## 🧪 Test complet

1. **Vérifier que tout tourne :**
```bash
docker ps
```

Vous devriez voir :
- ping61-backend
- ping61-cas
- ping61-openldap
- ping61-lam
- ping61-frontend
- ping61-postgres

2. **Tester CAS :**
```bash
curl http://localhost:8888/cas/login
```

3. **Tester Backend :**
```bash
curl http://localhost:8000/health
```

4. **Tester LAM :**
```bash
curl http://localhost:8081
```

5. **Test complet d'authentification :**
   - Allez sur http://localhost:3000
   - Cliquez "SE CONNECTER VIA CAS"
   - Connectez-vous avec student1 / password123
   - Vous devriez être redirigé vers le dashboard

## 📋 Vérification des logs

### Logs Backend
```bash
docker logs ping61-backend
```

Recherchez :
- ✅ "Application startup complete"
- ✅ "Uvicorn running on http://0.0.0.0:8000"

### Logs CAS
```bash
docker logs ping61-cas
```

Recherchez :
- ✅ "Running on http://0.0.0.0:8080"
- ✅ "Authentification LDAP réussie"

### Logs LDAP
```bash
docker logs ping61-openldap
```

## 🐛 Si ça ne marche toujours pas

### Erreur CORS persiste
```bash
# Rebuild complet
docker-compose down
docker-compose build --no-cache backend
docker-compose up -d
```

### Erreur 401
```bash
# Vérifier les variables d'environnement
docker exec ping61-backend env | findstr CAS
docker exec ping61-backend env | findstr JWT
```

### LAM ne s'affiche pas
```bash
# Vérifier que OpenLDAP est healthy
docker ps | findstr openldap

# Redémarrer LAM
docker-compose restart lam

# Attendre 10 secondes
timeout /t 10

# Tester
curl http://localhost:8081
```

## 📊 Flux d'authentification corrigé

```
1. Frontend → Clic "SE CONNECTER VIA CAS"
   ↓
2. Frontend → GET /api/auth/login
   ↓
3. Backend → Retourne http://localhost:8888/cas/login?service=...
   ↓
4. Navigateur → Redirige vers CAS
   ↓
5. CAS → Affiche formulaire
   ↓
6. Utilisateur → Entre student1 / password123
   ↓
7. CAS → Valide contre LDAP
   ↓
8. CAS → Génère ticket ST-xxxxx
   ↓
9. CAS → Redirige vers http://localhost:3000?ticket=ST-xxxxx
   ↓
10. Frontend → GET /api/auth/callback?ticket=ST-xxxxx
    ↓ (CORS OK maintenant)
11. Backend → Valide ticket auprès de CAS
    ↓
12. CAS → Retourne infos utilisateur
    ↓
13. Backend → Crée utilisateur en DB
    ↓
14. Backend → Génère JWT (avec JWT_SECRET_KEY)
    ↓
15. Frontend → Stocke JWT
    ↓
16. Frontend → Redirige vers /dashboard
```

## ✅ Checklist

- [ ] Backend redémarré
- [ ] JWT_SECRET_KEY configuré
- [ ] CORS activé
- [ ] CAS répond sur :8888
- [ ] Backend répond sur :8000
- [ ] LAM répond sur :8081 (peut prendre 30s)
- [ ] Test d'authentification réussi

---

**Commande rapide :** `fix-cors.bat`
