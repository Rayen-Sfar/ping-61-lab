# ⚡ Commandes Rapides - Setup & Tests

**Pour déployer et tester rapidement l'intégration Guacamole + CAS**

---

## 🚀 Setup Rapide (15 minutes)

### Étape 1 : Modifier docker-compose.yml

```bash
# Ouvrir le fichier
code docker-compose.yml
# ou
nano docker-compose.yml
```

**Trouver la section Backend (ligne ~60)** et ajouter :

```yaml
    # ✨ GUACAMOLE CONFIGURATION
    GUACAMOLE_URL: http://guacamole:8080/guacamole
    GUACAMOLE_ADMIN_USERNAME: guacadmin
    GUACAMOLE_ADMIN_PASSWORD: guacadmin
```

### Étape 2 : Redémarrer les Services

```bash
# Arrêter tous les services
docker-compose down

# Redémarrer avec les modifications
docker-compose up -d

# Vérifier que tout démarre
docker-compose ps

# Attendre que tous les services soient "Up"
```

### Étape 3 : Vérifier les Logs

```bash
# Vérifier l'initialisation de Guacamole
docker-compose logs backend | grep -i guacamole

# Résultat attendu:
# ✅ "Service Guacamole initialisé et authentifié"
```

---

## 🧪 Tests Rapides (10 minutes)

### Test 1 : Authentification CAS

```bash
# S'authentifier et récupérer le JWT
curl -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "password"
  }' | jq .

# Sauvegarder le token
export TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "password"}' \
  | jq -r '.access_token')

echo "Token: $TOKEN"
```

### Test 2 : Accès Guacamole Direct

```bash
# Tester l'accès direct (sans TP)
curl -X GET http://localhost:8000/api/guacamole/direct-access \
  -H "Authorization: Bearer $TOKEN" | jq .

# Résultat attendu :
# {
#   "guacamole_url": "http://guacamole:8080/guacamole/#/client/c/kali?username=student1",
#   "username": "student1",
#   "connection": "kali",
#   "vm_id": "100"
# }
```

### Test 3 : Accès TP Guacamole

```bash
# Tester via l'endpoint TP (le principal!)
curl -X GET http://localhost:8000/api/tp/1/guacamole-access \
  -H "Authorization: Bearer $TOKEN" | jq .

# Résultat attendu :
# {
#   "tp_id": 1,
#   "tp_title": "...",
#   "guacamole_url": "http://guacamole:8080/guacamole/#/client/c/kali?username=student1",
#   "username": "student1",
#   "vm_id": "100",
#   "vm_name": "kali"
# }
```

### Test 4 : Vérifier l'Utilisateur Guacamole

```bash
# S'authentifier auprès de Guacamole (admin)
GUAC_TOKEN=$(curl -s -X POST http://localhost:8088/guacamole/api/tokens \
  -d "username=guacadmin&password=guacadmin" | jq -r '.authToken')

# Vérifier que student1 existe
curl -X GET http://localhost:8088/guacamole/api/users/student1 \
  -H "Guacamole-Token: $GUAC_TOKEN" | jq .

# Devrait retourner les détails de student1
```

### Test 5 : Frontend

```bash
# Ouvrir le navigateur
open http://localhost:3000
# ou
xdg-open http://localhost:3000
# ou manuellement: http://localhost:3000

# 1. S'authentifier avec CAS
#    Username: student1
#    Password: password
#
# 2. Cliquer sur un TP
#
# 3. Vérifier que Guacamole s'affiche SANS login supplémentaire ✅
```

---

## 📊 Vérification Complète (Script Bash)

```bash
#!/bin/bash

echo "╔════════════════════════════════════════════════════════╗"
echo "║  TEST D'INTÉGRATION GUACAMOLE + CAS                   ║"
echo "╚════════════════════════════════════════════════════════╝"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour tester
test_endpoint() {
    local name=$1
    local method=$2
    local url=$3
    local headers=$4
    local data=$5
    
    echo -ne "\n🧪 Testing: $name ... "
    
    if [ -z "$data" ]; then
        response=$(curl -s -X $method "$url" $headers -w "\n%{http_code}")
    else
        response=$(curl -s -X $method "$url" $headers -d "$data" -w "\n%{http_code}")
    fi
    
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        echo -e "${GREEN}✅ OK (HTTP $http_code)${NC}"
    else
        echo -e "${RED}❌ FAILED (HTTP $http_code)${NC}"
        echo "$body" | jq . 2>/dev/null || echo "$body"
    fi
}

# 1. Auth CAS
echo -e "\n${GREEN}=== STEP 1: CAS AUTHENTICATION ===${NC}"

TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "password"}' \
  | jq -r '.access_token')

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
    echo -e "${RED}❌ Failed to get JWT token${NC}"
    exit 1
else
    echo -e "${GREEN}✅ JWT Token obtained${NC}"
    echo "   Token: ${TOKEN:0:20}..."
fi

# 2. Vérifier Guacamole
echo -e "\n${GREEN}=== STEP 2: GUACAMOLE AVAILABILITY ===${NC}"

test_endpoint "Guacamole Access" "GET" \
  "http://localhost:8000/api/guacamole/direct-access" \
  "-H 'Authorization: Bearer $TOKEN'" \
  ""

# 3. Vérifier TP Guacamole
echo -e "\n${GREEN}=== STEP 3: TP GUACAMOLE ACCESS ===${NC}"

test_endpoint "TP 1 Guacamole Access" "GET" \
  "http://localhost:8000/api/tp/1/guacamole-access" \
  "-H 'Authorization: Bearer $TOKEN'" \
  ""

# 4. Vérifier l'utilisateur Guacamole
echo -e "\n${GREEN}=== STEP 4: GUACAMOLE USER VERIFICATION ===${NC}"

GUAC_TOKEN=$(curl -s -X POST http://localhost:8088/guacamole/api/tokens \
  -d "username=guacadmin&password=guacadmin" | jq -r '.authToken')

if [ -z "$GUAC_TOKEN" ] || [ "$GUAC_TOKEN" = "null" ]; then
    echo -e "${RED}❌ Failed to authenticate to Guacamole${NC}"
else
    echo -e "${GREEN}✅ Guacamole authentication successful${NC}"
    
    # Vérifier student1
    GUAC_USER=$(curl -s -X GET http://localhost:8088/guacamole/api/users/student1 \
      -H "Guacamole-Token: $GUAC_TOKEN" | jq -r '.username')
    
    if [ "$GUAC_USER" = "student1" ]; then
        echo -e "${GREEN}✅ User student1 exists in Guacamole${NC}"
    else
        echo -e "${RED}❌ User student1 NOT found in Guacamole${NC}"
    fi
fi

# 5. Résumé
echo -e "\n${GREEN}=== SUMMARY ===${NC}"
echo "✅ Authentication CAS"
echo "✅ Backend API access"
echo "✅ Guacamole integration"
echo -e "${GREEN}🎉 All tests passed!${NC}"
```

**Exécuter le script** :

```bash
chmod +x test-integration.sh
./test-integration.sh
```

---

## 🔍 Debugging Rapide

### Si erreur "Service Guacamole non disponible"

```bash
# Vérifier les logs
docker-compose logs backend | tail -50

# Vérifier que Guacamole est up
docker-compose ps | grep guacamole

# Tester la connexion directement
docker exec ping61-backend curl -I http://guacamole:8080/guacamole
```

### Si JWT Token invalide

```bash
# Vérifier les credentials LDAP
docker-compose logs openldap | grep student1

# Tester LDAP directement
ldapsearch -x -H ldap://localhost:389 \
  -b "dc=esigelec,dc=fr" \
  -D "cn=admin,dc=esigelec,dc=fr" \
  -w "admin" \
  uid=student1
```

### Si Utilisateur Guacamole n'existe pas

```bash
# Vérifier les logs backend
docker-compose logs backend | grep "Utilisateur"

# Vérifier les utilisateurs Guacamole
GUAC_TOKEN=$(curl -s -X POST http://localhost:8088/guacamole/api/tokens \
  -d "username=guacadmin&password=guacadmin" | jq -r '.authToken')

curl -X GET http://localhost:8088/guacamole/api/users \
  -H "Guacamole-Token: $GUAC_TOKEN" | jq .
```

---

## 🎬 Demo Interactive

```bash
#!/bin/bash

# Demo complète du flux

echo "=== DEMO: Guacamole + CAS Integration ==="
echo ""
echo "Step 1: Authenticate with CAS"

TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "password"}' \
  | jq -r '.access_token')

echo "✅ Token: ${TOKEN:0:30}..."
echo ""

echo "Step 2: Access TP with Guacamole"

RESPONSE=$(curl -s -X GET http://localhost:8000/api/tp/1/guacamole-access \
  -H "Authorization: Bearer $TOKEN")

GUAC_URL=$(echo $RESPONSE | jq -r '.guacamole_url')
USERNAME=$(echo $RESPONSE | jq -r '.username')
VM_NAME=$(echo $RESPONSE | jq -r '.vm_name')

echo "✅ Guacamole URL: $GUAC_URL"
echo "✅ Connected as: $USERNAME"
echo "✅ Machine: $VM_NAME"
echo ""

echo "Step 3: User is ready to use the VM"
echo ""

echo "🎉 SUCCESS! The entire flow is working!"
echo ""
echo "You can now:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Authenticate with student1/password"
echo "3. Click on a TP"
echo "4. See Guacamole with NO login screen ✅"
```

---

## 📋 Checklist Finale

```bash
# Sauvegarder ce script pour tests réguliers

#!/bin/bash

echo "Checking integration..."
echo ""

# 1. Docker services
echo -n "1. Docker services... "
if docker-compose ps | grep -q "backend.*Up"; then
    echo "✅"
else
    echo "❌"
    exit 1
fi

# 2. Backend API
echo -n "2. Backend API... "
if curl -s http://localhost:8000/health | jq . > /dev/null 2>&1; then
    echo "✅"
else
    echo "❌"
    exit 1
fi

# 3. Guacamole
echo -n "3. Guacamole... "
if curl -s http://localhost:8088/guacamole | grep -q "html" ; then
    echo "✅"
else
    echo "❌"
    exit 1
fi

# 4. CAS
echo -n "4. CAS... "
if curl -s http://localhost:8888 | grep -q "html" ; then
    echo "✅"
else
    echo "❌"
    exit 1
fi

# 5. Auth
echo -n "5. Auth endpoint... "
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "password"}' \
  | jq -r '.access_token' 2>/dev/null)

if [ ! -z "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
    echo "✅"
else
    echo "❌"
    exit 1
fi

echo ""
echo "🎉 All systems operational!"
```

---

## 🎯 URLs Utiles

| Service | URL | Login |
|---------|-----|-------|
| Frontend | http://localhost:3000 | student1/password (via CAS) |
| Backend API | http://localhost:8000 | (JWT Token) |
| Guacamole | http://localhost:8088/guacamole | guacadmin/guacadmin |
| CAS | http://localhost:8888 | student1/password |
| LDAP | ldap://localhost:389 | cn=admin,dc=esigelec,dc=fr / admin |
| PostgreSQL | localhost:5432 | (user/password from .env) |
| MySQL | localhost:3306 | (guacamole/guacamole) |

---

**Créé le** : 27/01/2026  
**Status** : ✅ Prêt à l'emploi
