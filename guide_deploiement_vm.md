# Guide de Déploiement - Lab on Demand sur VM
## Installation et Configuration Complète

---

## 🎯 Prérequis VM

### Configuration minimale recommandée
- **OS** : Ubuntu 22.04 LTS ou CentOS 8+
- **RAM** : 8 GB minimum (16 GB recommandé)
- **CPU** : 4 cores minimum
- **Stockage** : 50 GB minimum (100 GB recommandé)
- **Réseau** : Accès Internet + ports ouverts

---

## 📋 Étape 1 : Préparation de la VM

### 1.1 Mise à jour du système
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
# ou pour les versions récentes
sudo dnf update -y
```

### 1.2 Installation des outils de base
```bash
# Ubuntu/Debian
sudo apt install -y curl wget git vim nano htop net-tools

# CentOS/RHEL
sudo yum install -y curl wget git vim nano htop net-tools
```

---

## 🐳 Étape 2 : Installation Docker et Docker Compose

### 2.1 Installation Docker (Ubuntu)
```bash
# Supprimer les anciennes versions
sudo apt remove docker docker-engine docker.io containerd runc

# Installer les dépendances
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Ajouter la clé GPG officielle Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Ajouter le repository Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Installer Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Démarrer et activer Docker
sudo systemctl start docker
sudo systemctl enable docker

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER
```

### 2.2 Installation Docker (CentOS)
```bash
# Supprimer les anciennes versions
sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine

# Installer les dépendances
sudo yum install -y yum-utils

# Ajouter le repository Docker
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Installer Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Démarrer et activer Docker
sudo systemctl start docker
sudo systemctl enable docker

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER
```

### 2.3 Vérification de l'installation
```bash
# Redémarrer la session ou faire
newgrp docker

# Tester Docker
docker --version
docker compose version

# Test de fonctionnement
docker run hello-world
```

---

## 📥 Étape 3 : Clonage du projet

### 3.1 Cloner le repository
```bash
# Aller dans le répertoire home
cd ~

# Cloner le projet (remplacez par votre URL GitHub)
git clone https://github.com/votre-username/ping-61-lab.git

# Aller dans le dossier du projet
cd ping-61-lab

# Vérifier le contenu
ls -la
```

### 3.2 Vérifier la structure du projet
```bash
# La structure doit ressembler à :
tree -L 2
# ou
find . -maxdepth 2 -type d
```

---

## ⚙️ Étape 4 : Configuration de l'environnement

### 4.1 Créer le fichier .env
```bash
# Copier le template
cp .env.example .env

# Éditer le fichier .env
nano .env
```

### 4.2 Configuration .env complète
```bash
# Créer le fichier .env avec les bonnes valeurs
cat > .env << 'EOF'
# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
DB_USER=labuser
DB_PASSWORD=labpassword123
DB_NAME=labondemand
DB_HOST=postgres
DB_PORT=5432

# =============================================================================
# GUACAMOLE DATABASE
# =============================================================================
GUAC_DB_USER=guacuser
GUAC_DB_PASSWORD=guacpassword123

# =============================================================================
# JWT CONFIGURATION
# =============================================================================
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# =============================================================================
# CAS CONFIGURATION
# =============================================================================
CAS_SERVER_URL=http://localhost:8888
CAS_LOGIN_URL=http://localhost:8888/cas/login
CAS_SERVICE_URL=http://localhost:3000

# =============================================================================
# PROXMOX CONFIGURATION (optionnel pour les VMs)
# =============================================================================
PROXMOX_HOST=your-proxmox-host
PROXMOX_USER=your-proxmox-user
PROXMOX_PASSWORD=your-proxmox-password

# =============================================================================
# APPLICATION CONFIGURATION
# =============================================================================
REACT_APP_API_URL=http://localhost:8000
REACT_APP_CAS_LOGIN_URL=http://localhost:8888/cas/login

# =============================================================================
# DEVELOPMENT
# =============================================================================
NODE_ENV=development
LOG_LEVEL=INFO
EOF
```

### 4.3 Créer les dossiers nécessaires
```bash
# Créer les dossiers pour les volumes
mkdir -p data/postgres data/mysql data/ldap ssl logs

# Permissions appropriées
chmod 755 data/
chmod 700 ssl/
```

---

## 🔧 Étape 5 : Configuration des services

### 5.1 Vérifier les Dockerfiles
```bash
# Vérifier que les Dockerfiles existent
ls -la */Dockerfile

# Si manquants, les créer :
```

### 5.2 Dockerfile Backend (si manquant)
```bash
cat > backend/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier les requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Exposer le port
EXPOSE 8000

# Commande par défaut
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
```

### 5.3 Dockerfile Frontend (si manquant)
```bash
cat > frontend/Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le code source
COPY . .

# Exposer le port
EXPOSE 3000

# Commande par défaut
CMD ["npm", "start"]
EOF
```

### 5.4 Dockerfile CAS Mock (si manquant)
```bash
mkdir -p cas-mock
cat > cas-mock/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN pip install flask python-ldap3

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
EOF
```

---

## 🚀 Étape 6 : Lancement de l'application

### 6.1 Construire les images
```bash
# Construire toutes les images
docker compose build

# Ou construire individuellement si nécessaire
docker compose build backend
docker compose build frontend
docker compose build cas
```

### 6.2 Démarrer les services
```bash
# Démarrer tous les services
docker compose up -d

# Vérifier le statut
docker compose ps

# Voir les logs
docker compose logs -f
```

### 6.3 Vérifier les services
```bash
# Vérifier que tous les conteneurs sont en cours d'exécution
docker ps

# Tester les endpoints
curl http://localhost:8000/health
curl http://localhost:3000
curl http://localhost:8888/cas
```

---

## 🔍 Étape 7 : Initialisation des données

### 7.1 Initialiser la base de données
```bash
# Attendre que PostgreSQL soit prêt
sleep 30

# Exécuter les scripts d'initialisation
docker compose exec backend python scripts/init_db.py

# Ou manuellement :
docker compose exec postgres psql -U labuser -d labondemand -f /docker-entrypoint-initdb.d/01-init.sql
```

### 7.2 Créer les utilisateurs LDAP
```bash
# Exécuter le script de création des utilisateurs
docker compose exec openldap bash -c "
ldapadd -x -D 'cn=admin,dc=esigelec,dc=fr' -w admin << 'EOF'
dn: ou=users,dc=esigelec,dc=fr
objectClass: organizationalUnit
ou: users

dn: uid=student1,ou=users,dc=esigelec,dc=fr
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: student1
cn: Student One
sn: One
givenName: Student
mail: student1@esigelec.fr
uidNumber: 1001
gidNumber: 1001
homeDirectory: /home/student1
userPassword: password123

dn: uid=teacher1,ou=users,dc=esigelec,dc=fr
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: teacher1
cn: Teacher One
sn: One
givenName: Teacher
mail: teacher1@esigelec.fr
uidNumber: 1002
gidNumber: 1002
homeDirectory: /home/teacher1
userPassword: password123
EOF
"
```

---

## 🌐 Étape 8 : Configuration réseau et firewall

### 8.1 Ouvrir les ports nécessaires
```bash
# Ubuntu (UFW)
sudo ufw allow 3000/tcp  # Frontend
sudo ufw allow 8000/tcp  # Backend API
sudo ufw allow 8888/tcp  # CAS Server
sudo ufw allow 8081/tcp  # LDAP Manager
sudo ufw allow 8088/tcp  # Guacamole
sudo ufw allow 22/tcp    # SSH
sudo ufw enable

# CentOS (firewalld)
sudo firewall-cmd --permanent --add-port=3000/tcp
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --permanent --add-port=8888/tcp
sudo firewall-cmd --permanent --add-port=8081/tcp
sudo firewall-cmd --permanent --add-port=8088/tcp
sudo firewall-cmd --reload
```

### 8.2 Vérifier la connectivité
```bash
# Tester depuis la VM
curl -I http://localhost:3000
curl -I http://localhost:8000/health
curl -I http://localhost:8888/cas

# Tester depuis l'extérieur (remplacez IP_VM par l'IP de votre VM)
curl -I http://IP_VM:3000
```

---

## ✅ Étape 9 : Tests de validation

### 9.1 Tests des services
```bash
# Script de test automatique
cat > test-services.sh << 'EOF'
#!/bin/bash

echo "=== Test des services Lab on Demand ==="

# Test Frontend
echo "🔍 Test Frontend (React)..."
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend OK"
else
    echo "❌ Frontend KO"
fi

# Test Backend
echo "🔍 Test Backend (FastAPI)..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend OK"
else
    echo "❌ Backend KO"
fi

# Test CAS
echo "🔍 Test CAS Server..."
if curl -s http://localhost:8888/cas > /dev/null; then
    echo "✅ CAS OK"
else
    echo "❌ CAS KO"
fi

# Test LDAP Manager
echo "🔍 Test LDAP Manager..."
if curl -s http://localhost:8081 > /dev/null; then
    echo "✅ LDAP Manager OK"
else
    echo "❌ LDAP Manager KO"
fi

# Test Guacamole
echo "🔍 Test Guacamole..."
if curl -s http://localhost:8088/guacamole > /dev/null; then
    echo "✅ Guacamole OK"
else
    echo "❌ Guacamole KO"
fi

# Test Base de données
echo "🔍 Test PostgreSQL..."
if docker compose exec -T postgres pg_isready -U labuser > /dev/null 2>&1; then
    echo "✅ PostgreSQL OK"
else
    echo "❌ PostgreSQL KO"
fi

echo "=== Tests terminés ==="
EOF

chmod +x test-services.sh
./test-services.sh
```

### 9.2 Test de l'authentification
```bash
# Test de connexion LDAP
docker compose exec openldap ldapsearch -x -H ldap://localhost -b "dc=esigelec,dc=fr" -D "cn=admin,dc=esigelec,dc=fr" -w admin

# Test API d'authentification
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "password123"}'
```

---

## 🔧 Étape 10 : Dépannage courant

### 10.1 Problèmes fréquents

#### Services qui ne démarrent pas
```bash
# Vérifier les logs
docker compose logs backend
docker compose logs frontend
docker compose logs postgres

# Redémarrer un service spécifique
docker compose restart backend

# Reconstruire et redémarrer
docker compose down
docker compose build --no-cache
docker compose up -d
```

#### Problèmes de permissions
```bash
# Corriger les permissions des volumes
sudo chown -R $USER:$USER data/
sudo chmod -R 755 data/

# Recréer les volumes si nécessaire
docker compose down -v
docker volume prune -f
docker compose up -d
```

#### Problèmes de réseau
```bash
# Vérifier les réseaux Docker
docker network ls
docker network inspect ping61-network

# Recréer le réseau
docker compose down
docker network prune -f
docker compose up -d
```

### 10.2 Commandes utiles de monitoring
```bash
# Surveiller les ressources
docker stats

# Voir les logs en temps réel
docker compose logs -f --tail=100

# Vérifier l'espace disque
df -h
docker system df

# Nettoyer si nécessaire
docker system prune -f
```

---

## 📱 Étape 11 : Accès à l'application

### 11.1 URLs d'accès
Une fois tout configuré, vous pouvez accéder à :

- **Application principale** : http://IP_VM:3000
- **API Backend** : http://IP_VM:8000
- **Documentation API** : http://IP_VM:8000/docs
- **CAS Server** : http://IP_VM:8888/cas
- **LDAP Manager** : http://IP_VM:8081
- **Guacamole** : http://IP_VM:8088/guacamole

### 11.2 Comptes de test
- **Étudiant** : student1 / password123
- **Enseignant** : teacher1 / password123

---

## 🔄 Étape 12 : Maintenance et mise à jour

### 12.1 Sauvegarde
```bash
# Script de sauvegarde
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/$DATE"

mkdir -p $BACKUP_DIR

# Sauvegarde base de données
docker compose exec -T postgres pg_dump -U labuser labondemand > $BACKUP_DIR/database.sql

# Sauvegarde volumes
docker run --rm -v ping61-lab_postgres_data:/data -v $(pwd)/$BACKUP_DIR:/backup alpine tar czf /backup/postgres_data.tar.gz -C /data .
docker run --rm -v ping61-lab_ldap_data:/data -v $(pwd)/$BACKUP_DIR:/backup alpine tar czf /backup/ldap_data.tar.gz -C /data .

echo "Sauvegarde créée dans $BACKUP_DIR"
EOF

chmod +x backup.sh
```

### 12.2 Mise à jour du code
```bash
# Mettre à jour depuis GitHub
git pull origin main

# Reconstruire et redémarrer
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

## 🎯 Résumé des commandes essentielles

```bash
# Démarrage complet
cd ~/ping-61-lab
docker compose up -d

# Arrêt
docker compose down

# Redémarrage
docker compose restart

# Logs
docker compose logs -f

# Status
docker compose ps

# Tests
./test-services.sh
```

---

*Guide de déploiement Lab on Demand*  
*Version VM - Janvier 2026*