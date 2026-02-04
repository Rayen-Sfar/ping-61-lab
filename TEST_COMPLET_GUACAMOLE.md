# 🧪 Guide de Test Complet - Intégration Guacamole CAS

**Version** : 1.0  
**Date** : 27/01/2026  
**Durée estimée** : 30 minutes

---

## 🎯 Objectifs des Tests

✅ Vérifier que l'authentification CAS fonctionne  
✅ Vérifier que Guacamole est accessible depuis le backend  
✅ Vérifier que les utilisateurs sont créés dans Guacamole  
✅ Vérifier que l'accès direct fonctionne  
✅ Vérifier que le frontend affiche la machine sans login supplémentaire  

---

## 📋 Prérequis

- [ ] Services Docker démarrés : `docker-compose up -d`
- [ ] Backend accessible : `http://localhost:8000`
- [ ] Frontend accessible : `http://localhost:3000`
- [ ] Guacamole accessible : `http://localhost:8088/guacamole`
- [ ] Utilisateur test LDAP : `student1` / `password`
- [ ] `curl` ou `Postman` installé

---

## 🔍 Étape 1 : Vérification des Services

### Test 1.1 : Services Docker

```bash
docker-compose ps

# Résultat attendu :
# NAME            STATUS
# postgres        Up
# mysql           Up
# guacamole       Up
# guacd           Up
# cas             Up
# backend         Up
# frontend        Up
# nginx           Up
```

### Test 1.2 : Connectivité Backend-Guacamole

```bash
# Depuis le backend, tester la connexion à Guacamole
docker exec ping61-backend curl -v http://guacamole:8080/guacamole

# Résultat attendu :
# HTTP/1.1 200 OK
# Content-Type: text/html
```

### Test 1.3 : Guacamole est Opérationnel

```bash
# Accès direct à Guacamole
curl http://localhost:8088/guacamole

# Résultat attendu :
# <html>...</html> (page HTML)
```

✅ **Étape 1 Validée** si tous les tests réussissent

---

## 🔐 Étape 2 : Authentification CAS

### Test 2.1 : Login LDAP Direct

```bash
curl -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "password"
  }' | jq .
```

**Résultat attendu** :
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "1",
  "username": "student1",
  "role": "student"
}
```

**Si erreur** :
```bash
# Vérifier que LDAP est accessible
docker-compose logs openldap | tail -20

# Vérifier les credentials LDAP
docker exec ping61-openldap ldapsearch -x -H ldap://localhost \
  -b "dc=esigelec,dc=fr" -D "cn=admin,dc=esigelec,dc=fr" \
  -w "admin" uid=student1
```

### Test 2.2 : Sauvegarder le Token

```bash
# Sauvegarder pour les tests suivants
export TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "password"}' \
  | jq -r '.access_token')

echo "Token: $TOKEN"
```

✅ **Étape 2 Validée** si un token valide est obtenu

---

## 🖥️ Étape 3 : Service Guacamole Backend

### Test 3.1 : Vérifier l'Initialisation

```bash
# Lire les logs du backend au démarrage
docker-compose logs backend | grep -i guacamole

# Résultat attendu :
# ✅ Authentification Guacamole réussie
# ✅ Service Guacamole initialisé et authentifié
```

**Si erreur** :
```bash
# Vérifier les variables d'environnement
docker-compose config | grep GUACAMOLE

# Vérifier la connexion directement
docker exec ping61-backend python3 -c "
import httpx
response = httpx.post(
    'http://guacamole:8080/guacamole/api/tokens',
    json={'username': 'guacadmin', 'password': 'guacadmin'}
)
print(response.status_code)
print(response.json())
"
```

### Test 3.2 : API Guacamole Service

```bash
# Tester le service Guacamole directement depuis le backend
docker exec ping61-backend python3 << 'EOF'
import asyncio
from app.services.guacamole_service import GuacamoleService

async def test():
    service = GuacamoleService(
        guac_url="http://guacamole:8080/guacamole",
        guac_username="guacadmin",
        guac_password="guacadmin"
    )
    
    # Tester l'authentification
    auth = await service.authenticate()
    print(f"Authentification: {auth}")
    
    # Lister les connexions
    connections = await service.list_connections()
    print(f"Connexions trouvées: {len(connections)}")
    for conn in connections:
        print(f"  - {conn.get('name', 'Unknown')}")

asyncio.run(test())
EOF
```

✅ **Étape 3 Validée** si Guacamole est initialisé et les connexions sont listées

---

## 🎓 Étape 4 : Endpoints Guacamole

### Test 4.1 : Accès Direct Guacamole

```bash
curl -X GET http://localhost:8000/api/guacamole/direct-access \
  -H "Authorization: Bearer $TOKEN" | jq .
```

**Résultat attendu** :
```json
{
  "guacamole_url": "http://guacamole:8080/guacamole/#/client/c/kali?username=student1",
  "username": "student1",
  "connection": "kali",
  "vm_id": "100"
}
```

**Si erreur "Service Guacamole non disponible"** :
- Vérifier les logs : `docker-compose logs backend`
- Vérifier les variables d'environnement

### Test 4.2 : Lister les Connexions

```bash
curl -X GET http://localhost:8000/api/guacamole/list-connections \
  -H "Authorization: Bearer $TOKEN" | jq .
```

**Résultat attendu** :
```json
{
  "connections": [
    {
      "name": "kali",
      "identifier": "c/kali",
      "protocol": "ssh"
    }
  ],
  "total": 1
}
```

✅ **Étape 4 Validée** si les endpoints retournent les bonnes données

---

## 🌟 Étape 5 : Accès TP avec Guacamole

### Test 5.1 : Créer un TP de Test

```bash
# Créer un TP test
curl -X POST http://localhost:8000/api/tp \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Guacamole",
    "description": "TP de test pour vérifier Guacamole",
    "instructions": "## Instructions\n\nTest d'\''intégration Guacamole CAS",
    "difficulty": "Facile",
    "duration": "1h",
    "vm_type": "kali",
    "status": "Published",
    "created_by": "admin"
  }' | jq .

# Sauvegarder l'ID (ex: 1)
export TP_ID=1
```

### Test 5.2 : Accès Direct TP + Guacamole

```bash
curl -X GET http://localhost:8000/api/tp/$TP_ID/guacamole-access \
  -H "Authorization: Bearer $TOKEN" | jq .
```

**Résultat attendu** :
```json
{
  "tp_id": 1,
  "tp_title": "Test Guacamole",
  "guacamole_url": "http://guacamole:8080/guacamole/#/client/c/kali?username=student1",
  "username": "student1",
  "vm_id": "100",
  "vm_name": "kali",
  "message": "Accès automatique avec authentification CAS"
}
```

### Test 5.3 : Vérifier la Création de l'Utilisateur Guacamole

```bash
# S'authentifier auprès de Guacamole (admin)
GUAC_TOKEN=$(curl -s -X POST http://localhost:8088/guacamole/api/tokens \
  -d "username=guacadmin&password=guacadmin" | jq -r '.authToken')

# Lister les utilisateurs
curl -X GET http://localhost:8088/guacamole/api/users \
  -H "Guacamole-Token: $GUAC_TOKEN" | jq '.[] | {username}'

# Chercher student1
curl -X GET http://localhost:8088/guacamole/api/users/student1 \
  -H "Guacamole-Token: $GUAC_TOKEN" | jq .
```

**Résultat attendu** : L'utilisateur `student1` doit exister dans Guacamole

✅ **Étape 5 Validée** si l'accès TP retourne une URL valide

---

## ⚛️ Étape 6 : Frontend React

### Test 6.1 : Accès au Frontend

```bash
# Ouvrir le navigateur
http://localhost:3000

# Vérifier :
# - Page de login visible
# - CAS login possible
```

### Test 6.2 : S'Authentifier

```
1. Cliquer sur "Login" ou "Sign In"
2. Redirection vers CAS
3. Entrer : student1 / password
4. Être redirigé vers le dashboard
```

### Test 6.3 : Accéder à un TP

```
1. Sur la page Dashboard, cliquer sur un TP
2. Observer le chargement :
   - "⏳ Initialisation de la machine virtuelle..."
   - "Authentification CAS et connexion à Kali..."
3. Après quelques secondes :
   - "✅ Connecté en tant que: student1"
   - Guacamole iframe affichée
   - Interface Kali visible
```

### Test 6.4 : Interagir avec Kali

```
1. Cliquer dans l'iframe Guacamole
2. Tester les commandes (si SSH configuré)
3. Vérifier qu'aucun login supplémentaire n'est demandé
```

✅ **Étape 6 Validée** si Guacamole s'affiche sans login supplémentaire

---

## 🔄 Étape 7 : Tests Avancés

### Test 7.1 : Rechargement de Page

```
1. Sur la page du TP, appuyer sur F5 (Refresh)
2. Observer :
   - Nouveau call à /api/tp/{id}/guacamole-access
   - Utilisateur Guacamole re-vérifié
   - Accès accordé à nouveau
   - Guacamole se charge à nouveau
```

### Test 7.2 : Múltiples Utilisateurs

```bash
# Test avec student2
curl -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{"username": "student2", "password": "password"}' | jq -r '.access_token' > token2.txt

export TOKEN2=$(cat token2.txt)

curl -X GET http://localhost:8000/api/tp/1/guacamole-access \
  -H "Authorization: Bearer $TOKEN2" | jq .

# Vérifier que student2 est créé dans Guacamole
curl -X GET http://localhost:8088/guacamole/api/users/student2 \
  -H "Guacamole-Token: $GUAC_TOKEN" | jq .
```

### Test 7.3 : Token Expiré

```bash
# Attendre 61 minutes (JWT_EXPIRE_MINUTES = 60) ou modifier le token
# Tenter un accès avec le token expiré

curl -X GET http://localhost:8000/api/tp/1/guacamole-access \
  -H "Authorization: Bearer $OLD_TOKEN"

# Résultat attendu : 401 Unauthorized
```

✅ **Étape 7 Validée** si tous les cas avancés fonctionnent

---

## 📊 Étape 8 : Vérification Complète

### Checklist Finale

```
# Backend
☐ Logs montrent "✅ Service Guacamole initialisé"
☐ /api/auth/ldap-login retourne un token JWT
☐ /api/tp/{id}/guacamole-access retourne une URL
☐ /api/guacamole/direct-access fonctionne

# Guacamole
☐ Accessible sur http://localhost:8088/guacamole
☐ Admin credentials guacadmin:guacadmin fonctionnent
☐ Connexion "kali" existe
☐ Utilisateurs créés dynamiquement (student1, student2, etc.)

# Frontend
☐ Login CAS fonctionne
☐ Dashboard visible après auth
☐ Clic sur TP charge l'interface Guacamole
☐ Guacamole s'affiche sans login supplémentaire ✅
☐ Kali (machine 100) est accessible

# Sécurité
☐ JWT token valide pour chaque requête
☐ Credentials Guacamole admin ne sont pas exposés
☐ Utilisateurs Guacamole ont l'accès minimal
```

---

## 🐛 Résolution des Problèmes

### Problème : "Erreur 401 Unauthorized"

```bash
# Vérifier le token
echo $TOKEN

# S'il est vide, refaire la connexion
export TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "password"}' \
  | jq -r '.access_token')

# Tester
curl -X GET http://localhost:8000/api/guacamole/direct-access \
  -H "Authorization: Bearer $TOKEN"
```

### Problème : "Guacamole n'affiche que l'écran de chargement"

```bash
# Vérifier l'URL Guacamole retournée
GUAC_URL=$(curl -s -X GET http://localhost:8000/api/tp/1/guacamole-access \
  -H "Authorization: Bearer $TOKEN" | jq -r '.guacamole_url')

echo $GUAC_URL

# L'URL doit ressembler à :
# http://guacamole:8080/guacamole/#/client/c/kali?username=student1

# Tester l'accès direct
curl -I "$GUAC_URL"
```

### Problème : "Utilisateur Guacamole n'est pas créé"

```bash
# Vérifier les logs du backend
docker-compose logs backend | grep -i "utilisateur"

# Vérifier que le service Guacamole a pu s'authentifier
docker-compose logs backend | grep "Authentification Guacamole"

# Vérifier directement dans Guacamole
GUAC_TOKEN=$(curl -s http://localhost:8088/guacamole/api/tokens \
  -d "username=guacadmin&password=guacadmin" | jq -r '.authToken')

curl -X GET http://localhost:8088/guacamole/api/users \
  -H "Guacamole-Token: $GUAC_TOKEN"
```

---

## ✅ Validation Finale

Une fois tous les tests passés, vous pouvez valider :

```bash
echo "
╔════════════════════════════════════════════════════════════╗
║  ✅ INTÉGRATION GUACAMOLE + CAS - COMPLÈTE ET OPÉRATIONNELLE ║
╚════════════════════════════════════════════════════════════╝

✅ Authentification CAS - FONCTIONNELLE
✅ Accès Guacamole - AUTOMATIQUE
✅ Interface Kali - ACCESSIBLE
✅ Frontend - SANS LOGIN SUPPLÉMENTAIRE
✅ Sécurité - DOUBLE AUTHENTIFICATION

Status: Production Ready 🚀
"
```

---

## 📝 Notes

- 🕐 Chaque test doit prendre < 1 minute
- 📊 Les logs sont très utiles pour debugger
- 🔍 Vérifier toujours les variables d'environnement
- 💾 Sauvegarder les URLs et tokens pour les tests suivants

---

**Test réalisé le** : [Date]  
**Résultat** : ✅ / ❌  
**Commentaires** : 

---

**Créé le** : 27/01/2026  
**Status** : ✅ Guide complet
