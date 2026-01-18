# 🎯 Formulaire de Connexion Direct - Sans Redirection CAS

## ✅ Changements appliqués

### Avant (avec redirection CAS)
```
http://localhost:3000
    ↓ Clic "SE CONNECTER VIA CAS"
    ↓ Redirection
http://localhost:8888/cas/login
    ↓ Formulaire CAS
    ↓ Authentification
    ↓ Redirection avec ticket
http://localhost:3000?ticket=ST-xxxxx
    ↓ Validation ticket
Dashboard
```

### Après (formulaire direct)
```
http://localhost:3000
    ↓ Formulaire directement sur la page
    ↓ Entrer identifiants
    ↓ Authentification LDAP directe
    ↓ JWT généré
Dashboard
```

## 📝 Modifications

### 1. Frontend - LoginPage.jsx
- ✅ Formulaire de connexion intégré directement
- ✅ Champs username et password
- ✅ Appel API `/api/auth/ldap-login`
- ❌ Plus de redirection vers CAS externe

### 2. Backend - auth.py
- ✅ Nouvelle route `/api/auth/ldap-login`
- ✅ Authentification LDAP directe
- ✅ Génération JWT immédiate

### 3. CAS Mock - app.py
- ✅ Nouveau endpoint `/ldap/authenticate`
- ✅ Validation LDAP sans ticket

## 🚀 Application des changements

```bash
apply-direct-login.bat
```

## 🧪 Test

1. Ouvrez http://localhost:3000
2. Vous voyez directement le formulaire de connexion
3. Entrez **student1** / **password123**
4. Cliquez **SE CONNECTER**
5. Vous êtes redirigé vers le dashboard

## 📊 Nouveau flux d'authentification

```
┌─────────────────────────────────────────┐
│  1. Utilisateur sur http://localhost:3000│
│     Formulaire visible directement       │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  2. Utilisateur entre credentials        │
│     username: student1                   │
│     password: password123                │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  3. Frontend → POST /api/auth/ldap-login │
│     {username, password}                 │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  4. Backend → POST /ldap/authenticate    │
│     Vers CAS Mock (port 8080)            │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  5. CAS Mock → Valide contre LDAP        │
│     OpenLDAP (port 389)                  │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  6. CAS Mock → Retourne user_info        │
│     {username, mail, givenName, sn}      │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  7. Backend → Crée/met à jour User en DB │
│     PostgreSQL                           │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  8. Backend → Génère JWT                 │
│     access_token, user_id, role          │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  9. Frontend → Stocke JWT                │
│     localStorage.setItem('token', ...)   │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  10. Frontend → Redirige vers dashboard  │
│      /dashboard ou /admin selon rôle     │
└─────────────────────────────────────────┘
```

## ✅ Avantages

1. **Plus simple** - Pas de redirection externe
2. **Plus rapide** - Moins d'étapes
3. **Meilleure UX** - Formulaire directement visible
4. **Moins de bugs** - Pas de gestion de tickets CAS
5. **LDAP toujours utilisé** - Authentification sécurisée

## 🔧 Services utilisés

| Service | Rôle | Port |
|---------|------|------|
| **Frontend** | Interface utilisateur | 3000 |
| **Backend** | API + Logique métier | 8000 |
| **CAS Mock** | Validation LDAP | 8080 |
| **OpenLDAP** | Annuaire utilisateurs | 389 |
| **PostgreSQL** | Base de données | 5432 |

## 📌 Routes supprimées

- ❌ `/api/auth/login` (redirection CAS)
- ❌ `/api/auth/callback` (validation ticket)
- ❌ `/cas/login` (formulaire CAS externe)

## 📌 Routes ajoutées

- ✅ `/api/auth/ldap-login` (authentification directe)
- ✅ `/ldap/authenticate` (validation LDAP dans CAS Mock)

## 🐛 Dépannage

### Erreur "Identifiants invalides"
```bash
# Vérifier que les utilisateurs LDAP existent
docker exec ping61-openldap ldapsearch -x -H ldap://localhost -b "dc=esigelec,dc=fr" "(uid=student1)"

# Recréer les utilisateurs si nécessaire
cd scripts
create-ldap-users.bat
```

### Erreur "Erreur serveur"
```bash
# Vérifier les logs
docker logs ping61-backend
docker logs ping61-cas

# Redémarrer les services
docker-compose restart backend cas
```

## ✅ Checklist

- [ ] Services rebuild
- [ ] Frontend affiche le formulaire directement
- [ ] Pas de redirection vers CAS externe
- [ ] Connexion avec student1 / password123 fonctionne
- [ ] Redirection vers dashboard après connexion
- [ ] JWT stocké dans localStorage

---

**Commande rapide:** `apply-direct-login.bat`
