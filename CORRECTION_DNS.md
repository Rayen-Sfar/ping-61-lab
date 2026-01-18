# 🔧 Correction du problème DNS_PROBE_FINISHED_NXDOMAIN

## ❌ Problème

Lorsque vous cliquiez sur "SE CONNECTER VIA CAS", vous étiez redirigé vers :
```
http://cas:8080/cas/login?service=...
```

Le navigateur ne pouvait pas résoudre `cas` car c'est un **nom de conteneur Docker interne**.

## ✅ Solution

J'ai séparé les URLs CAS en deux :

1. **URL interne** (`CAS_SERVER_URL`) : `http://cas:8080`
   - Utilisée par le backend pour valider les tickets
   - Fonctionne dans le réseau Docker

2. **URL publique** (`CAS_SERVER_URL_PUBLIC`) : `http://localhost:8888`
   - Utilisée pour rediriger le navigateur
   - Accessible depuis votre machine

## 📝 Fichiers modifiés

### 1. `.env`
```env
CAS_SERVER_URL=http://cas:8080              # Pour backend (réseau Docker)
CAS_SERVER_URL_PUBLIC=http://localhost:8888  # Pour navigateur
CAS_SERVICE_URL=http://localhost:3000        # URL de callback
```

### 2. `backend/app/core/config.py`
```python
cas_server_url: str = os.getenv("CAS_SERVER_URL", "http://cas:8080")
cas_server_url_public: str = os.getenv("CAS_SERVER_URL_PUBLIC", "http://localhost:8888")
```

### 3. `backend/app/api/auth.py`
```python
@router.get("/login")
async def cas_login():
    # Utilise l'URL publique pour le navigateur
    cas_login_url = f"{settings.cas_server_url_public}/cas/login?service={settings.cas_service_url}"
    return {"redirect_url": cas_login_url}
```

### 4. `docker-compose.yml`
```yaml
backend:
  environment:
    CAS_SERVER_URL: http://cas:8080
    CAS_SERVER_URL_PUBLIC: http://localhost:8888
    CAS_SERVICE_URL: http://localhost:3000
```

## 🚀 Pour appliquer les corrections

### Option 1 : Redémarrer uniquement le backend (RAPIDE)
```bash
restart-backend.bat
```

### Option 2 : Redémarrer tout
```bash
docker-compose down
docker-compose up -d
```

## 🧪 Test

1. Accédez à http://localhost:3000
2. Cliquez sur "SE CONNECTER VIA CAS"
3. Vous devriez être redirigé vers : `http://localhost:8888/cas/login?service=http://localhost:3000`
4. Connectez-vous avec : **student1** / **password123**

## 📊 Flux corrigé

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Utilisateur clique "SE CONNECTER VIA CAS"               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Frontend → GET /api/auth/login                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Backend retourne:                                        │
│    http://localhost:8888/cas/login?service=...              │
│    (URL PUBLIQUE - accessible par le navigateur)            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Navigateur redirige vers CAS                             │
│    ✅ localhost:8888 est accessible                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Utilisateur se connecte sur CAS                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. CAS redirige vers:                                       │
│    http://localhost:3000?ticket=ST-xxxxx                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Frontend → GET /api/auth/callback?ticket=ST-xxxxx        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. Backend valide le ticket auprès de CAS                   │
│    Utilise http://cas:8080/cas/validate                     │
│    (URL INTERNE - réseau Docker)                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 9. Backend génère JWT et retourne au frontend               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 10. Frontend redirige vers le dashboard                     │
└─────────────────────────────────────────────────────────────┘
```

## 🔍 Vérification

### Vérifier que CAS est accessible
```bash
curl http://localhost:8888/cas/login
```

Vous devriez voir du HTML (page de login CAS).

### Vérifier la configuration backend
```bash
docker exec ping61-backend env | findstr CAS
```

Vous devriez voir :
```
CAS_SERVER_URL=http://cas:8080
CAS_SERVER_URL_PUBLIC=http://localhost:8888
CAS_SERVICE_URL=http://localhost:3000
```

## 🐛 Si ça ne marche toujours pas

### 1. Vérifier que CAS est démarré
```bash
docker ps | findstr cas
```

### 2. Voir les logs CAS
```bash
docker logs ping61-cas
```

### 3. Tester l'URL CAS manuellement
Ouvrez dans votre navigateur : http://localhost:8888/cas/login

### 4. Redémarrer tout
```bash
docker-compose down
docker-compose up -d
timeout /t 30
cd scripts
create-ldap-users.bat
```

## ✅ Résultat attendu

Maintenant, quand vous cliquez sur "SE CONNECTER VIA CAS", vous devriez :
1. Être redirigé vers `http://localhost:8888/cas/login`
2. Voir le formulaire de connexion CAS
3. Pouvoir vous connecter avec student1 / password123
4. Être redirigé vers le dashboard

---

**Date :** 16 janvier 2026
**Problème résolu :** DNS_PROBE_FINISHED_NXDOMAIN
