# 🚀 Quick Start - Intégration Guacamole + CAS

## Checklist de Déploiement

### ✅ Step 1 : Vérifier la Configuration Guacamole

```bash
# 1. Se connecter à Guacamole en admin
# URL: http://localhost:8080/guacamole
# Username: guacadmin
# Password: guacadmin

# 2. Vérifier que la connexion "kali" existe
# Menu: Administration > Connections
# Chercher une connexion SSH vers 10.3.0.100:22
```

### ✅ Step 2 : Configurer les Variables d'Environnement

**Dans docker-compose.yml ou .env** :

```yaml
# Backend Service
backend:
  environment:
    # Guacamole Configuration
    GUACAMOLE_URL: "http://guacamole:8080/guacamole"
    GUACAMOLE_ADMIN_USERNAME: "guacadmin"
    GUACAMOLE_ADMIN_PASSWORD: "guacadmin"
    
    # CAS (existant)
    CAS_SERVER_URL: "http://cas:8080"
    CAS_SERVER_URL_PUBLIC: "http://localhost:8888"
    CAS_SERVICE_URL: "http://localhost:3000"
    
    # Database
    DATABASE_URL: "postgresql://user:password@postgres:5432/labdb"
```

### ✅ Step 3 : Redémarrer le Backend

```bash
# Docker Compose
docker-compose down
docker-compose up -d backend

# Vérifier les logs
docker-compose logs -f backend

# Chercher :
# ✅ "Service Guacamole initialisé et authentifié"
```

### ✅ Step 4 : Tester le Flux Complet

#### Test 1 : Authentification CAS

```bash
curl -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "password"
  }'

# Réponse :
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "user_id": "1",
  "username": "student1",
  "role": "student"
}
```

#### Test 2 : Accès à Guacamole via TP

```bash
# Utiliser le token de la réponse précédente
TOKEN="eyJhbGci..."

curl -X GET http://localhost:8000/api/tp/1/guacamole-access \
  -H "Authorization: Bearer $TOKEN"

# Réponse :
{
  "tp_id": 1,
  "tp_title": "Exploitation Kali",
  "guacamole_url": "http://guacamole:8080/guacamole/#/client/c/kali?username=student1",
  "username": "student1",
  "vm_id": "100",
  "vm_name": "kali",
  "message": "Accès automatique avec authentification CAS"
}
```

#### Test 3 : Frontend

```bash
# 1. Se connecter au frontend
# http://localhost:3000

# 2. S'authentifier avec CAS
# Username: student1
# Password: password

# 3. Cliquer sur un TP
# → Devrait voir l'interface Kali automatiquement

# 4. Vérifier :
# ✅ "✅ Connecté en tant que: student1"
# ✅ Affichage de Kali dans l'iframe
# ✅ Aucun écran de login Guacamole
```

## 🔍 Troubleshooting

### Problème : "Service Guacamole non disponible"

```bash
# Vérifier que Guacamole est accessible
curl http://guacamole:8080/guacamole/api/tokens \
  -d "username=guacadmin&password=guacadmin"

# Si erreur de connexion :
# - Vérifier que guacamole est dans docker-compose.yml
# - Vérifier que GUACAMOLE_URL est correct
```

### Problème : "Impossible de créer/vérifier l'utilisateur"

```bash
# Vérifier les credentials admin
curl -v http://guacamole:8080/guacamole/api/tokens \
  -d "username=guacadmin&password=guacadmin"

# Si 401 : le password est incorrect
# Réinitialiser le mot de passe dans guacamole-init.sql
```

### Problème : "Connexion kali non trouvée"

```bash
# Vérifier que la connexion existe dans Guacamole
curl http://guacamole:8080/guacamole/api/datasources/postgresql/connections \
  -H "Guacamole-Token: $TOKEN"

# La réponse doit contenir une connexion avec :
# "name": "kali" (ou "c/kali")
# "protocol": "ssh"
# "hostname": "10.3.0.100"
```

### Problème : JWT Token invalide

```bash
# Vérifier que le JWT_SECRET_KEY est configuré
# Dans main.py, vérifier settings.JWT_SECRET_KEY

# Régénérer le token :
curl -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "password"}'
```

## 📊 Vérification Complète

### Checklist Finale

- [ ] Guacamole accessible sur `http://guacamole:8080/guacamole`
- [ ] Admin credentials guacadmin:guacadmin fonctionnent
- [ ] Connexion "kali" existe dans Guacamole
- [ ] Variables GUACAMOLE_* configurées dans backend
- [ ] Backend redémarré et logs montrent "✅ Service Guacamole initialisé"
- [ ] Login CAS fonctionne (get JWT token)
- [ ] `/api/tp/{id}/guacamole-access` retourne une URL
- [ ] Frontend affiche Guacamole sans login supplémentaire

## 🎯 Résultat Attendu

### Avant (Ancien Flux)

```
1. User authentifié CAS ✅
2. Click sur TP → Envoie vers Guacamole
3. Écran de login Guacamole ❌
4. User entre ses credentials Guacamole ❌
5. Accès à la machine
```

### Après (Nouveau Flux) ✨

```
1. User authentifié CAS ✅
2. Click sur TP → Appel API /tp/{id}/guacamole-access
3. Backend crée user Guacamole automatiquement ✨
4. Backend accorde l'accès à la machine ✨
5. URL d'accès direct générée ✨
6. Frontend affiche Guacamole + iframe ✅
7. Aucun login supplémentaire ✅
8. User voit la machine immédiatement ✅
```

## 📝 Configuration Recommandée

```yaml
# docker-compose.yml

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      # CAS
      CAS_SERVER_URL: "http://cas:8080"
      CAS_SERVER_URL_PUBLIC: "http://localhost:8888"
      CAS_SERVICE_URL: "http://localhost:3000"
      
      # JWT
      JWT_SECRET_KEY: "votre_clé_secrète_très_longue"
      JWT_EXPIRE_MINUTES: "60"
      
      # ✨ GUACAMOLE ✨
      GUACAMOLE_URL: "http://guacamole:8080/guacamole"
      GUACAMOLE_ADMIN_USERNAME: "guacadmin"
      GUACAMOLE_ADMIN_PASSWORD: "guacadmin"  # Changer en production
      
      # Database
      DATABASE_URL: "postgresql://user:password@postgres:5432/labdb"
    depends_on:
      - guacamole
      - cas
      - postgres

  guacamole:
    image: guacamole/guacamole:latest
    ports:
      - "8080:8080"
    environment:
      GUACAMOLE_HOME: /etc/guacamole
      MYSQL_HOSTNAME: mysql
      MYSQL_DATABASE: guacamole_db
      MYSQL_USER: guacamole
      MYSQL_PASSWORD: guacamole
    depends_on:
      - mysql

  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: guacamole_db
      MYSQL_USER: guacamole
      MYSQL_PASSWORD: guacamole
    volumes:
      - mysql_data:/var/lib/mysql

  # CAS, Frontend, etc...
```

## 🎬 Démo Interactive

```bash
#!/bin/bash

# 1. Authentification
echo "🔐 Authentification CAS..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "password"}')

TOKEN=$(echo $RESPONSE | jq -r '.access_token')
echo "✅ JWT Token obtenu: ${TOKEN:0:20}..."

# 2. Accès TP
echo -e "\n🎓 Accès au TP..."
TP_RESPONSE=$(curl -s -X GET http://localhost:8000/api/tp/1/guacamole-access \
  -H "Authorization: Bearer $TOKEN")

GUAC_URL=$(echo $TP_RESPONSE | jq -r '.guacamole_url')
echo "✅ URL Guacamole: $GUAC_URL"

# 3. Vérification
echo -e "\n📊 Résumé:"
echo "- User: student1"
echo "- TP ID: 1"
echo "- VM: kali (100)"
echo "- Accès: Automatique ✅"
echo "- URL: $GUAC_URL"
```

---

**Documentation créée le** : 27/01/2026  
**Status** : ✅ Prêt à déployer
