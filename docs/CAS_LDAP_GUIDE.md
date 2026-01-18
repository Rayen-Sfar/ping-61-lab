# 🔐 Guide d'Authentification CAS avec LDAP

## Vue d'ensemble

Ce projet utilise **CAS (Central Authentication Service)** avec **OpenLDAP** pour l'authentification des utilisateurs.

## Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Frontend  │─────▶│  CAS Server │─────▶│   OpenLDAP  │
│  (React)    │◀─────│  (Apereo)   │◀─────│             │
└─────────────┘      └─────────────┘      └─────────────┘
       │                                           │
       │                                           │
       ▼                                           ▼
┌─────────────┐                          ┌─────────────┐
│   Backend   │                          │     LAM     │
│  (FastAPI)  │                          │  (Web UI)   │
└─────────────┘                          └─────────────┘
```

## 🚀 Démarrage rapide

### 1. Démarrer tous les services

```bash
docker-compose up -d
```

Cela démarre :
- **OpenLDAP** (port 389) - Annuaire LDAP
- **LAM** (port 8081) - Interface web pour gérer LDAP
- **CAS** (port 8888) - Serveur d'authentification
- **Backend** (port 8000) - API FastAPI
- **Frontend** (port 3000) - Application React
- **PostgreSQL** (port 5432) - Base de données

### 2. Créer des utilisateurs LDAP

**Windows :**
```bash
cd scripts
create-ldap-users.bat
```

**Linux/Mac :**
```bash
cd scripts
chmod +x create-ldap-users.sh
./create-ldap-users.sh
```

### 3. Accéder à l'application

Ouvrez votre navigateur : **http://localhost:3000**

## 👥 Comptes de test

### Étudiants
- **Identifiant :** student1
- **Mot de passe :** password123
- **Email :** jean.dupont@esigelec.fr

### Enseignants
- **Identifiant :** teacher1
- **Mot de passe :** password123
- **Email :** marie.martin@esigelec.fr

## 🔧 Gestion LDAP

### Via LDAP Account Manager (LAM)

1. Accédez à **http://localhost:8081**
2. Connectez-vous avec :
   - **Login :** cn=admin,dc=esigelec,dc=fr
   - **Password :** admin

### Via ligne de commande

**Lister tous les utilisateurs :**
```bash
docker exec ping61-openldap ldapsearch -x -H ldap://localhost -b "dc=esigelec,dc=fr" -D "cn=admin,dc=esigelec,dc=fr" -w admin
```

**Ajouter un utilisateur :**
```bash
docker exec ping61-openldap ldapadd -x -D "cn=admin,dc=esigelec,dc=fr" -w admin << EOF
dn: uid=newuser,ou=users,dc=esigelec,dc=fr
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: newuser
cn: New User
sn: User
givenName: New
mail: newuser@esigelec.fr
uidNumber: 10003
gidNumber: 10003
homeDirectory: /home/newuser
userPassword: password123
EOF
```

**Supprimer un utilisateur :**
```bash
docker exec ping61-openldap ldapdelete -x -D "cn=admin,dc=esigelec,dc=fr" -w admin "uid=newuser,ou=users,dc=esigelec,dc=fr"
```

## 🔄 Flux d'authentification

1. **Utilisateur clique sur "SE CONNECTER VIA CAS"**
   - Frontend → Backend `/api/auth/login`
   - Backend retourne l'URL CAS

2. **Redirection vers CAS**
   - Utilisateur redirigé vers `http://localhost:8888/cas/login`
   - CAS affiche le formulaire de connexion

3. **Authentification LDAP**
   - CAS valide les credentials contre OpenLDAP
   - Si succès, CAS génère un ticket (ST-xxxxx)

4. **Callback**
   - CAS redirige vers `http://localhost:3000?ticket=ST-xxxxx`
   - Frontend envoie le ticket au Backend `/api/auth/callback`

5. **Validation du ticket**
   - Backend valide le ticket auprès de CAS
   - CAS retourne les informations utilisateur (username, email, etc.)

6. **Création de session**
   - Backend crée/met à jour l'utilisateur en base
   - Backend génère un JWT
   - Frontend stocke le JWT et redirige vers le dashboard

## 🛠️ Configuration

### Modifier le domaine LDAP

Éditez `docker-compose.yml` :
```yaml
openldap:
  environment:
    LDAP_ORGANISATION: "VotreOrganisation"
    LDAP_DOMAIN: "votre-domaine.fr"
    LDAP_ADMIN_PASSWORD: "votre-mot-de-passe"
```

### Modifier la configuration CAS

Éditez `cas-config/cas.properties` :
```properties
cas.authn.ldap[0].ldap-url=ldap://openldap:389
cas.authn.ldap[0].base-dn=dc=votre-domaine,dc=fr
cas.authn.ldap[0].bind-dn=cn=admin,dc=votre-domaine,dc=fr
```

## 🐛 Dépannage

### CAS ne démarre pas
```bash
# Vérifier les logs
docker logs ping61-cas

# Redémarrer CAS
docker restart ping61-cas
```

### LDAP ne répond pas
```bash
# Vérifier le statut
docker ps | grep openldap

# Tester la connexion
docker exec ping61-openldap ldapsearch -x -H ldap://localhost -b "dc=esigelec,dc=fr"
```

### Erreur "Ticket invalide"
- Vérifiez que le service est bien enregistré dans `cas-services/`
- Vérifiez que l'URL de callback correspond

### Utilisateur non trouvé
- Vérifiez que l'utilisateur existe dans LDAP
- Vérifiez le filtre de recherche dans `cas.properties`

## 📚 Ressources

- [Documentation CAS](https://apereo.github.io/cas/)
- [Documentation OpenLDAP](https://www.openldap.org/doc/)
- [LDAP Account Manager](https://www.ldap-account-manager.org/)

## 🔒 Sécurité en production

⚠️ **Important :** Cette configuration est pour le développement uniquement !

En production :
1. Utilisez HTTPS pour CAS
2. Changez tous les mots de passe par défaut
3. Utilisez des certificats SSL valides
4. Configurez un vrai serveur LDAP (Active Directory, etc.)
5. Activez les logs d'audit
6. Limitez les accès réseau

## 📝 Notes

- Les mots de passe LDAP sont stockés en clair pour le développement
- En production, utilisez SSHA ou un autre algorithme de hachage
- Le port 8888 est utilisé pour CAS (au lieu de 8443 HTTPS)
- LAM est accessible sans authentification (à sécuriser en production)
