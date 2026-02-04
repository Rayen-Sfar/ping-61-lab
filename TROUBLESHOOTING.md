# 🆘 Troubleshooting - Problèmes Courants & Solutions

**Si quelque chose ne fonctionne pas, vous êtes au bon endroit**

---

## 🔴 Erreur : "Service Guacamole non disponible"

### Symptôme
```
POST /api/tp/1/guacamole-access
Response: 500 - "Service Guacamole non disponible"
```

### Causes Possibles

#### 1️⃣ Variables d'Environnement Non Configurées

```bash
# Vérifier
docker-compose config | grep GUACAMOLE

# Doit afficher:
# GUACAMOLE_URL: http://guacamole:8080/guacamole
# GUACAMOLE_ADMIN_USERNAME: guacadmin
# GUACAMOLE_ADMIN_PASSWORD: guacadmin
```

**Solution** :
```yaml
# docker-compose.yml - Section backend
environment:
  GUACAMOLE_URL: http://guacamole:8080/guacamole
  GUACAMOLE_ADMIN_USERNAME: guacadmin
  GUACAMOLE_ADMIN_PASSWORD: guacadmin
```

Puis redémarrer : `docker-compose down && docker-compose up -d`

#### 2️⃣ Guacamole n'est pas Accessible

```bash
# Tester depuis le backend
docker exec ping61-backend curl -v http://guacamole:8080/guacamole

# Résultat attendu: HTTP 200
```

**Solution** :
```bash
# Vérifier que Guacamole est running
docker-compose ps | grep guacamole

# Doit montrer "Up"

# Si down, redémarrer
docker-compose up -d guacamole
```

#### 3️⃣ Credentials Guacamole Incorrects

```bash
# Tester les credentials
docker exec ping61-backend curl -X POST http://guacamole:8080/guacamole/api/tokens \
  -d "username=guacadmin&password=guacadmin"

# Résultat attendu: {"authToken": "..."}
# Si erreur 401: password incorrect
```

**Solution** :
```bash
# Vérifier dans guacamole-init.sql ou guacamole_user_roles
# Par défaut: username=guacadmin, password=guacadmin

# Si modifié, mettre à jour docker-compose.yml
GUACAMOLE_ADMIN_PASSWORD: <votre_password>
```

#### 4️⃣ Guacamole n'est pas Démarré

```bash
# Vérifier les logs Guacamole
docker-compose logs guacamole | tail -20

# Chercher des erreurs
```

**Solution** :
```bash
# Redémarrer complètement
docker-compose restart guacamole guacd mysql
docker-compose logs guacamole -f

# Attendre que "Initialization Complete" s'affiche
```

---

## 🔴 Erreur : "401 Unauthorized"

### Symptôme
```
GET /api/tp/1/guacamole-access
Response: 401 - "Token invalide"
```

### Causes

#### 1️⃣ JWT Token Expiré

```bash
# Un token JWT dure 60 minutes par défaut
# Après 60 min, il expire

# Solution: Se reconnecter
curl -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "password"}'

# Récupérer le nouveau token
export TOKEN=$(...)
```

#### 2️⃣ JWT Token Invalide/Mal Formé

```bash
# Vérifier le token
echo $TOKEN

# Doit ressembler à:
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# S'il est vide ou "null", se reconnecter
```

**Solution** :
```bash
# Récupérer un nouveau token
export TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "password"}' \
  | jq -r '.access_token')

# Vérifier
echo $TOKEN
```

#### 3️⃣ JWT_SECRET_KEY Non Configurée

```bash
# Vérifier
docker-compose config | grep JWT_SECRET_KEY

# Doit montrer une clé (pas vide)
```

**Solution** :
```yaml
# docker-compose.yml ou .env
JWT_SECRET_KEY: votre_clé_secrète_très_longue

# Redémarrer
docker-compose restart backend
```

---

## 🔴 Erreur : "TP not found"

### Symptôme
```
GET /api/tp/1/guacamole-access
Response: 404 - "TP not found"
```

### Cause
Le TP avec l'ID 1 n'existe pas en base de données

**Solution** :
```bash
# Vérifier les TPs disponibles
curl -X GET http://localhost:8000/api/tp \
  -H "Authorization: Bearer $TOKEN"

# Créer un TP si nécessaire
curl -X POST http://localhost:8000/api/tp \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test TP",
    "description": "Test",
    "instructions": "Test",
    "difficulty": "Facile",
    "duration": "1h",
    "vm_type": "kali",
    "status": "Published",
    "created_by": "admin"
  }'
```

---

## 🔴 Erreur : "Impossible de créer/vérifier l'utilisateur"

### Symptôme
```
GET /api/tp/1/guacamole-access
Response: 500 - "Impossible de créer/vérifier l'utilisateur Guacamole"
```

### Causes

#### 1️⃣ Guacamole Admin pas authentifié

```bash
# Tester l'authentification admin
curl -X POST http://localhost:8088/guacamole/api/tokens \
  -d "username=guacadmin&password=guacadmin"

# Si erreur 401: credentials incorrects
```

**Solution** : Voir ci-dessus "Credentials Guacamole Incorrects"

#### 2️⃣ Permissions insuffisantes pour Admin Guacamole

```bash
# Vérifier que guacadmin a les bonnes permissions
# dans guacamole_user_permissions
```

**Solution** :
```bash
# Réinitialiser la base Guacamole
docker-compose down
docker volume rm ping61_mysql_data  # ⚠️ Cela efface les données!
docker-compose up -d
```

#### 3️⃣ Erreur de Réseau vers Guacamole

```bash
# Vérifier la connectivité
docker exec ping61-backend ping guacamole

# Doit répondre: "from guacamole"
```

**Solution** :
```bash
# Vérifier le réseau Docker
docker network ls
docker network inspect ping61-network

# Guacamole doit être dans ce réseau
```

---

## 🔴 Erreur : "Utilisateur CAS n'existe pas"

### Symptôme
```
Authentification échoue
Response: "Identifiants invalides"
```

### Cause
L'utilisateur n'existe pas dans LDAP

**Solution** :
```bash
# Vérifier que student1 existe dans LDAP
ldapsearch -x -H ldap://localhost:389 \
  -b "dc=esigelec,dc=fr" \
  -D "cn=admin,dc=esigelec,dc=fr" \
  -w "admin" \
  uid=student1

# Si pas de résultat, créer l'utilisateur
# ou en créer un qui existe déjà (teacher1, etc.)
```

---

## 🔴 Erreur : "Connexion kali non trouvée"

### Symptôme
```
Response: "Connexion kali non trouvée"
```

### Cause
La connexion "kali" n'existe pas dans Guacamole

**Solution** :

#### Option 1: Vérifier via UI Guacamole
```
1. Aller sur http://localhost:8088/guacamole
2. S'authentifier: guacadmin / guacadmin
3. Menu: Administration > Connections
4. Chercher une connexion "kali" ou "c/kali"
5. Si n'existe pas, l'ajouter
```

#### Option 2: Vérifier via API
```bash
# Lister les connexions
GUAC_TOKEN=$(curl -s -X POST http://localhost:8088/guacamole/api/tokens \
  -d "username=guacadmin&password=guacadmin" | jq -r '.authToken')

curl -X GET http://localhost:8088/guacamole/api/datasources/postgresql/connections \
  -H "Guacamole-Token: $GUAC_TOKEN" | jq '.[] | {name}'

# Doit afficher "kali" ou "c/kali"
```

#### Option 3: Modifier le code
```python
# Dans tp.py, changer connection_id
await guac_service.get_direct_access_url(
    username=user.cas_id,
    cas_username=user.cas_id,
    connection_id="1"  # ou l'ID réel de la connexion
)
```

---

## 🔴 Frontend : Guacamole n'affiche que l'écran de chargement

### Symptôme
```
LabPage.jsx affiche:
"Démarrage de la VM..."
Indéfiniment
```

### Causes

#### 1️⃣ L'endpoint retourne une erreur

```bash
# Vérifier dans la console du navigateur (F12)
# Ou tester directement:

TOKEN=<votre_token>
curl -X GET http://localhost:8000/api/tp/1/guacamole-access \
  -H "Authorization: Bearer $TOKEN" | jq .

# Doit retourner {"guacamole_url": "..."}
```

#### 2️⃣ L'URL Guacamole est malformée

```bash
# Vérifier l'URL retournée
GUAC_URL=$(curl -s -X GET http://localhost:8000/api/tp/1/guacamole-access \
  -H "Authorization: Bearer $TOKEN" | jq -r '.guacamole_url')

echo $GUAC_URL

# Doit être:
# http://guacamole:8080/guacamole/#/client/c/kali?username=student1
```

#### 3️⃣ CORS Issue

```javascript
// Dans LabPage.jsx, vérifier
console.log(guacResponse.data);

// Si erreur CORS:
// Vérifier que backend a CORS configuré
```

**Solution** :
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🟡 Avertissement : "Service Guacamole initialisé mais pas authentifié"

### Signification
```
Le service est disponible mais n'a pas pu s'authentifier au démarrage
```

### Solution
```bash
# Vérifier les logs au démarrage
docker-compose logs backend | head -50

# Vérifier les credentials
docker-compose config | grep GUACAMOLE

# Redémarrer
docker-compose restart backend
```

---

## 🟡 Avertissement : "Utilisateur existe déjà"

### Signification
```
OK - L'utilisateur student1 existe déjà dans Guacamole
Pas d'erreur, c'est normal sur les appels suivants
```

### Info
C'est un comportement normal. Les logs montreront:
```
✅ Utilisateur student1 existe déjà
```

---

## 🟢 Tests de Diagnostic Rapides

### Test 1 : Connectivité

```bash
# Backend vers Guacamole
docker exec ping61-backend curl http://guacamole:8080/guacamole

# Résultat attendu: 200 OK
```

### Test 2 : Authentification CAS

```bash
curl -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "password"}' | jq .

# Doit retourner un token valide
```

### Test 3 : Authentification Guacamole

```bash
curl -X POST http://localhost:8088/guacamole/api/tokens \
  -d "username=guacadmin&password=guacadmin" | jq .

# Doit retourner un authToken
```

### Test 4 : Accès TP Guacamole

```bash
curl -X GET http://localhost:8000/api/tp/1/guacamole-access \
  -H "Authorization: Bearer <TOKEN>" | jq .

# Doit retourner guacamole_url
```

---

## 📋 Checklist de Vérification

```bash
# Si quelque chose ne fonctionne pas, vérifier:

☐ docker-compose ps | grep guacamole (running?)
☐ docker-compose logs guacamole | tail -20 (errors?)
☐ docker-compose config | grep GUACAMOLE (variables set?)
☐ curl http://localhost:8088/guacamole (accessible?)
☐ curl http://guacamole:8080/guacamole (accessible from backend?)
☐ CAS login fonctionne (token obtenu?)
☐ LDAP user existe (student1?)
☐ Backend logs propres (pas d'erreurs de démarrage?)
```

---

## 💡 Tips Utiles

### Voir les logs en temps réel

```bash
# Backend
docker-compose logs -f backend

# Guacamole
docker-compose logs -f guacamole

# CAS
docker-compose logs -f cas

# LDAP
docker-compose logs -f openldap
```

### Réinitialiser Complètement

```bash
# ⚠️ Cela supprime TOUTES les données!

docker-compose down
docker volume rm ping61_mysql_data
docker volume rm ping61_postgres_data
docker-compose up -d

# Laisser le temps aux services de démarrer
sleep 30

# Vérifier
docker-compose ps
```

### Entrer dans un container

```bash
# Entrer dans le backend
docker exec -it ping61-backend /bin/bash

# Ou le frontend
docker exec -it ping61-frontend /bin/bash

# Ou Guacamole
docker exec -it ping61-guacamole /bin/bash
```

---

## 📞 Escalade

Si vous avez essayé tous les troubleshooting ci-dessus et ça ne marche toujours pas :

1. **Exécuter le script de test complet** : [TEST_COMPLET_GUACAMOLE.md](TEST_COMPLET_GUACAMOLE.md)
2. **Lire les logs détaillés** : `docker-compose logs --tail=100`
3. **Consulter l'architecture** : [GUACAMOLE_CAS_INTEGRATION.md](GUACAMOLE_CAS_INTEGRATION.md)
4. **Vérifier les prérequis** : [QUICK_START_GUACAMOLE.md](QUICK_START_GUACAMOLE.md)

---

**Créé le** : 27/01/2026  
**Status** : ✅ Guide Complet de Troubleshooting
