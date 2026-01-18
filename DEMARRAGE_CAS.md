# 🚀 Démarrage Rapide - Lab on Demand avec CAS + LDAP

## ⚠️ Important

Ce projet utilise **UN SEUL serveur CAS** (Apereo CAS 7.0.3) avec authentification LDAP.
Le `cas-mock` a été supprimé pour éviter les conflits de ports.

## 📋 Prérequis

- Docker Desktop installé et démarré
- Ports disponibles : 3000, 8000, 8888, 8081, 389, 5432, 3306, 8088

## 🎯 Démarrage automatique (Recommandé)

```bash
start-with-cas.bat
```

Ce script fait tout automatiquement :
1. Arrête les anciens conteneurs
2. Démarre tous les services
3. Attend 30 secondes
4. Crée les utilisateurs LDAP

## 🔧 Démarrage manuel

### Étape 1 : Démarrer les services

```bash
docker-compose up -d
```

### Étape 2 : Attendre 30 secondes

Les services ont besoin de temps pour démarrer, surtout CAS et OpenLDAP.

### Étape 3 : Créer les utilisateurs LDAP

```bash
cd scripts
create-ldap-users.bat
```

## 🌐 Accès aux services

| Service | URL | Description |
|---------|-----|-------------|
| **Application** | http://localhost:3000 | Interface principale |
| **Backend API** | http://localhost:8000 | API FastAPI |
| **CAS Server** | http://localhost:8888/cas | Serveur d'authentification |
| **LDAP Manager** | http://localhost:8081 | Gestion des utilisateurs LDAP |
| **Guacamole** | http://localhost:8088 | Accès aux VMs |

## 👤 Comptes de test

### Étudiant
- **Identifiant :** student1
- **Mot de passe :** password123
- **Email :** jean.dupont@esigelec.fr

### Enseignant
- **Identifiant :** teacher1
- **Mot de passe :** password123
- **Email :** marie.martin@esigelec.fr

## 🔄 Flux d'authentification

1. Accédez à http://localhost:3000
2. Cliquez sur "SE CONNECTER VIA CAS"
3. Vous êtes redirigé vers CAS (http://localhost:8888/cas/login)
4. Entrez vos identifiants (student1 / password123)
5. CAS valide contre LDAP
6. Vous êtes redirigé vers l'application avec un token JWT

## 🐛 Dépannage

### Les conteneurs ne démarrent pas

```bash
# Voir les logs
docker-compose logs

# Voir les logs d'un service spécifique
docker-compose logs cas
docker-compose logs openldap
```

### CAS ne répond pas

```bash
# Vérifier que CAS est démarré
docker ps | findstr cas

# Redémarrer CAS
docker restart ping61-cas

# Voir les logs CAS
docker logs ping61-cas
```

### LDAP ne répond pas

```bash
# Vérifier LDAP
docker ps | findstr openldap

# Tester la connexion LDAP
docker exec ping61-openldap ldapsearch -x -H ldap://localhost -b "dc=esigelec,dc=fr"
```

### Erreur "Ticket invalide"

1. Vérifiez que CAS est bien démarré
2. Vérifiez les logs : `docker logs ping61-cas`
3. Vérifiez que le fichier `cas-services/LabOnDemand-1.json` existe
4. Redémarrez CAS : `docker restart ping61-cas`

### Les utilisateurs LDAP n'existent pas

```bash
cd scripts
create-ldap-users.bat
```

## 🛑 Arrêter les services

```bash
docker-compose down
```

## 🗑️ Tout supprimer (données incluses)

```bash
docker-compose down -v
```

## 📊 Vérifier l'état des services

```bash
docker-compose ps
```

## 📝 Architecture

```
┌─────────────┐
│   Browser   │
│ :3000       │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Frontend   │─────▶│  Backend    │      │  PostgreSQL │
│  (React)    │◀─────│  (FastAPI)  │─────▶│  :5432      │
└──────┬──────┘      └──────┬──────┘      └─────────────┘
       │                    │
       │                    │
       ▼                    ▼
┌─────────────┐      ┌─────────────┐
│  CAS Server │─────▶│  OpenLDAP   │
│  :8888      │◀─────│  :389       │
└─────────────┘      └─────────────┘
       │
       ▼
┌─────────────┐
│     LAM     │
│  :8081      │
└─────────────┘
```

## ✅ Checklist de démarrage

- [ ] Docker Desktop est démarré
- [ ] Tous les ports sont disponibles
- [ ] `docker-compose up -d` exécuté
- [ ] Attente de 30 secondes
- [ ] Utilisateurs LDAP créés
- [ ] http://localhost:3000 accessible
- [ ] http://localhost:8888/cas accessible
- [ ] Connexion avec student1 / password123 fonctionne

## 📚 Documentation complète

- [Guide CAS + LDAP](docs/CAS_LDAP_GUIDE.md)
- [Guide Admin](docs/ADMIN_GUIDE.md)
- [API Documentation](docs/API.md)
