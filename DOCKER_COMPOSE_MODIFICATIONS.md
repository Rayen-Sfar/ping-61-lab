# 🔧 Modifications docker-compose.yml pour Guacamole + CAS

## Résumé des Changements

Vous devez modifier le service `backend` dans votre `docker-compose.yml` pour ajouter les variables d'environnement Guacamole.

## Variables à Ajouter dans le Service Backend

```yaml
backend:
  build:
    context: ./backend
    dockerfile: Dockerfile
  container_name: ping61-backend
  environment:
    # ✅ CAS Configuration (EXISTANT)
    CAS_SERVER_URL: http://cas:8080
    CAS_SERVER_URL_PUBLIC: http://localhost:8888
    CAS_SERVICE_URL: http://localhost:3000
    
    # Database (EXISTANT)
    DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/${DB_NAME}
    
    # JWT (EXISTANT)
    JWT_SECRET_KEY: ${JWT_SECRET_KEY}
    JWT_ALGORITHM: HS256
    JWT_EXPIRE_MINUTES: 60
    
    # Proxmox (EXISTANT)
    PROXMOX_HOST: ${PROXMOX_HOST}
    PROXMOX_USER: ${PROXMOX_USER}
    PROXMOX_PASSWORD: ${PROXMOX_PASSWORD}
    
    # ✨ GUACAMOLE CONFIGURATION (À AJOUTER)
    GUACAMOLE_URL: http://guacamole:8080/guacamole
    GUACAMOLE_ADMIN_USERNAME: guacadmin
    GUACAMOLE_ADMIN_PASSWORD: guacadmin
    
    # Server (EXISTANT)
    LOG_LEVEL: INFO
```

## Points Importants

### 1. GUACAMOLE_URL

```yaml
# ✅ CORRECT - URL interne (backend vers guacamole)
GUACAMOLE_URL: http://guacamole:8080/guacamole

# ❌ INCORRECT - N'utiliser l'URL publique que pour le frontend
# GUACAMOLE_URL: http://localhost:8088/guacamole
```

### 2. Service Guacamole dans docker-compose.yml

Vérifiez que le service guacamole existe déjà (ligne ~155-175) :

```yaml
guacamole:
  image: guacamole/guacamole:latest
  container_name: ping61-guacamole
  environment:
    GUACD_HOSTNAME: guacd
    GUACD_PORT: 4822
    MYSQL_HOSTNAME: mysql
    MYSQL_DATABASE: guacamole
    MYSQL_USER: ${GUAC_DB_USER}
    MYSQL_PASSWORD: ${GUAC_DB_PASSWORD}
  ports:
    - "8088:8080"  # ✅ Port interne: 8080, externe: 8088
  depends_on:
    mysql:
      condition: service_healthy
    guacd:
      condition: service_started
```

### 3. Service MySQL pour Guacamole

Vérifiez que MySQL est configuré (ligne ~5-25) :

```yaml
mysql:
  image: mysql:8.0
  container_name: ping61-mysql
  environment:
    MYSQL_ROOT_PASSWORD: rootpassword
    MYSQL_DATABASE: guacamole
    MYSQL_USER: ${GUAC_DB_USER}
    MYSQL_PASSWORD: ${GUAC_DB_PASSWORD}
  volumes:
    - mysql_data:/var/lib/mysql
    - ./scripts/guacamole-init.sql:/docker-entrypoint-initdb.d/01-guacamole-init.sql
```

## Étapes de Mise à Jour

### 1. Modifier docker-compose.yml

```bash
# Ouvrir le fichier
nano docker-compose.yml
# ou dans VS Code
code docker-compose.yml
```

### 2. Trouver la section `backend`

Chercher : `# ============================================================================`  
Puis : `# BACKEND API (FastAPI)`

### 3. Ajouter les 3 lignes Guacamole

```yaml
    # ✨ GUACAMOLE CONFIGURATION
    GUACAMOLE_URL: http://guacamole:8080/guacamole
    GUACAMOLE_ADMIN_USERNAME: guacadmin
    GUACAMOLE_ADMIN_PASSWORD: guacadmin
```

### 4. Sauvegarder

```bash
# Ctrl+X, puis Y, puis Enter (dans nano)
# Ou Ctrl+S (dans VS Code)
```

### 5. Redémarrer les services

```bash
docker-compose down
docker-compose up -d backend guacamole mysql guacd
```

### 6. Vérifier les logs

```bash
docker-compose logs -f backend

# Chercher :
# ✅ "Service Guacamole initialisé et authentifié"
```

## Variables d'Environnement Recommandées (.env)

```bash
# Guacamole (ajouter à votre .env existant)
GUAC_DB_USER=guacamole
GUAC_DB_PASSWORD=guacamole_secure_password

# Les autres variables doivent déjà exister :
# CAS_SERVER_URL, DB_USER, DB_PASSWORD, JWT_SECRET_KEY, etc.
```

## Vérification Complète

### Checklist

```bash
# 1. Services actifs
docker-compose ps

# Vous devez voir :
# ✅ postgres    (running)
# ✅ mysql       (running)
# ✅ cas         (running)
# ✅ backend     (running)
# ✅ guacamole   (running)
# ✅ guacd       (running)

# 2. Guacamole accessible
curl http://localhost:8088/guacamole
# Réponse : HTML (page de login de Guacamole)

# 3. Backend peut accéder à Guacamole
docker exec ping61-backend curl http://guacamole:8080/guacamole/api/tokens \
  -d "username=guacadmin&password=guacadmin"

# Réponse : {"authToken":"..."}

# 4. Vérifier les logs du backend
docker-compose logs backend | grep "Service Guacamole"
# Chercher : ✅ "Service Guacamole initialisé et authentifié"
```

## Dépannage

### Service Guacamole refuse la connexion

```bash
# Vérifier que Guacamole est en cours d'exécution
docker ps | grep guacamole

# Vérifier les logs
docker-compose logs guacamole

# Redémarrer
docker-compose restart guacamole
```

### "GUACAMOLE_URL" non reconnu

```bash
# S'assurer que les variables sont bien définie dans docker-compose.yml
docker-compose config | grep GUACAMOLE

# Doit afficher :
# GUACAMOLE_URL: http://guacamole:8080/guacamole
# GUACAMOLE_ADMIN_USERNAME: guacadmin
# GUACAMOLE_ADMIN_PASSWORD: guacadmin
```

### Backend ne peut pas se connecter à Guacamole

```bash
# Vérifier le réseau
docker network ls
# Chercher : ping61-network

# Vérifier la connectivité
docker run --rm --network ping61-network alpine \
  wget -O - http://guacamole:8080/guacamole

# Si timeout : Guacamole n'est pas accessible
```

## Configuration Complète du Backend

```yaml
# docker-compose.yml - Section Backend Complète

backend:
  build:
    context: ./backend
    dockerfile: Dockerfile
  container_name: ping61-backend
  environment:
    # ✅ CAS Configuration
    CAS_SERVER_URL: http://cas:8080
    CAS_SERVER_URL_PUBLIC: http://localhost:8888
    CAS_SERVICE_URL: http://localhost:3000
    
    # Database
    DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/${DB_NAME}
    
    # JWT
    JWT_SECRET_KEY: ${JWT_SECRET_KEY}
    JWT_ALGORITHM: HS256
    JWT_EXPIRE_MINUTES: 60
    
    # Proxmox
    PROXMOX_HOST: ${PROXMOX_HOST}
    PROXMOX_USER: ${PROXMOX_USER}
    PROXMOX_PASSWORD: ${PROXMOX_PASSWORD}
    
    # ✨ Guacamole (NOUVEAU)
    GUACAMOLE_URL: http://guacamole:8080/guacamole
    GUACAMOLE_ADMIN_USERNAME: guacadmin
    GUACAMOLE_ADMIN_PASSWORD: guacadmin
    
    # Server
    LOG_LEVEL: INFO
  
  ports:
    - "8000:8000"
  
  depends_on:
    - postgres
    - mysql
    - cas
    - guacamole    # ✨ Ajouter cette dépendance
  
  volumes:
    - ./backend:/app
  
  command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Après la Configuration

Une fois modifié et redémarré, vous pouvez tester :

```bash
# 1. S'authentifier
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "password"}' \
  | jq -r '.access_token')

# 2. Accéder à Guacamole
curl -X GET http://localhost:8000/api/tp/1/guacamole-access \
  -H "Authorization: Bearer $TOKEN" | jq

# 3. Voir la réponse
{
  "tp_id": 1,
  "guacamole_url": "http://guacamole:8080/guacamole/#/client/c/kali?username=student1",
  ...
}
```

---

**Modification effectuée le** : 27/01/2026  
**Status** : ✅ Prêt à appliquer
