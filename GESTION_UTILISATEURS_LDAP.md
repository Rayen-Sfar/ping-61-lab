# 👥 Gestion des Utilisateurs LDAP

## ✅ Réponse à votre question

**OUI**, vous pouvez utiliser **TOUS les utilisateurs disponibles dans LDAP** pour vous connecter, pas seulement les comptes de test !

## 📋 Utilisateurs disponibles

### 🔍 Voir tous les utilisateurs LDAP
```bash
list-ldap-users.bat
```

### 👤 Comptes de test (créés par défaut)
- **student1** / password123
- **teacher1** / password123

### ➕ Ajouter de nouveaux utilisateurs
```bash
add-ldap-user.bat
```

## 🌐 Méthodes de gestion des utilisateurs

### 1. Interface Web LAM (Recommandée)
- **URL :** http://localhost:8081
- **Login :** cn=admin,dc=esigelec,dc=fr
- **Password :** admin

### 2. Ligne de commande
```bash
# Lister les utilisateurs
docker exec ping61-openldap ldapsearch -x -H ldap://localhost -b "dc=esigelec,dc=fr" "(uid=*)"

# Ajouter un utilisateur
add-ldap-user.bat
```

### 3. Script personnalisé
Modifiez `scripts/create-ldap-users.bat` pour ajouter vos utilisateurs.

## 🧪 Test d'authentification

### Avec n'importe quel utilisateur LDAP :
1. Allez sur http://localhost:3000
2. Cliquez "SE CONNECTER VIA CAS"
3. Entrez **n'importe quel identifiant LDAP** et son mot de passe
4. L'authentification fonctionne !

### Exemple avec un nouvel utilisateur :
```bash
# Créer l'utilisateur
add-ldap-user.bat
# Entrer : alice / Alice / Dupont / alice@esigelec.fr / monmotdepasse

# Tester la connexion
# http://localhost:3000 → alice / monmotdepasse
```

## 📊 Structure LDAP

```
dc=esigelec,dc=fr
├── ou=users
│   ├── uid=student1
│   ├── uid=teacher1
│   ├── uid=alice
│   ├── uid=bob
│   └── uid=... (tous vos utilisateurs)
└── cn=admin (administrateur LDAP)
```

## 🔑 Attributs utilisateur LDAP

Chaque utilisateur a :
- **uid** : Identifiant de connexion
- **userPassword** : Mot de passe
- **cn** : Nom complet
- **mail** : Email
- **givenName** : Prénom
- **sn** : Nom de famille

## 🎯 Cas d'usage

### Étudiants
```bash
# Créer plusieurs étudiants
add-ldap-user.bat
# etudiant1 / password123
# etudiant2 / password123
# etudiant3 / password123
```

### Enseignants
```bash
# Créer des enseignants
add-ldap-user.bat
# prof.martin / motdepasse
# prof.durand / motdepasse
```

### Administrateurs
```bash
# Créer des admins
add-ldap-user.bat
# admin.tech / adminpass
```

## 🔧 Gestion avancée

### Modifier un utilisateur existant
Via LAM (http://localhost:8081) ou ligne de commande :
```bash
docker exec -it ping61-openldap bash
ldapmodify -x -D "cn=admin,dc=esigelec,dc=fr" -w admin
```

### Supprimer un utilisateur
```bash
docker exec ping61-openldap ldapdelete -x -D "cn=admin,dc=esigelec,dc=fr" -w admin "uid=username,ou=users,dc=esigelec,dc=fr"
```

### Changer un mot de passe
Via LAM ou :
```bash
docker exec ping61-openldap ldappasswd -x -D "cn=admin,dc=esigelec,dc=fr" -w admin -s nouveaumotdepasse "uid=username,ou=users,dc=esigelec,dc=fr"
```

## 📝 Bonnes pratiques

1. **Utilisez LAM** pour la gestion graphique
2. **Conventions de nommage** : prenom.nom ou matricule
3. **Mots de passe forts** en production
4. **Groupes LDAP** pour organiser les utilisateurs
5. **Sauvegarde** des données LDAP

## 🚀 Commandes utiles

```bash
# Voir tous les utilisateurs
list-ldap-users.bat

# Ajouter un utilisateur
add-ldap-user.bat

# Interface web
start http://localhost:8081

# Tester la connexion
start http://localhost:3000
```

## ✅ Résumé

**Tous les utilisateurs LDAP peuvent se connecter** à votre application Lab on Demand via CAS. Les comptes student1/teacher1 ne sont que des exemples !

---

**Commandes rapides :**
- `list-ldap-users.bat` - Voir tous les utilisateurs
- `add-ldap-user.bat` - Ajouter un utilisateur
- http://localhost:8081 - Interface LAM