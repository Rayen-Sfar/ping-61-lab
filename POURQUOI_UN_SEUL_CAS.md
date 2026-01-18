# ❓ Pourquoi un seul serveur CAS ?

## 🔴 Problème initial

Vous aviez **DEUX** serveurs CAS qui essayaient de démarrer :
1. **cas-mock** (serveur de test simple en Python/Flask)
2. **cas** (vrai serveur Apereo CAS avec LDAP)

Les deux utilisaient le **même port 8888**, ce qui causait un conflit.

## ✅ Solution

Nous avons **supprimé cas-mock** et gardé uniquement le **vrai serveur CAS** avec LDAP.

## 📊 Comparaison

| Caractéristique | cas-mock (❌ Supprimé) | cas (✅ Utilisé) |
|----------------|----------------------|------------------|
| Type | Serveur de test simple | Serveur CAS complet |
| Technologie | Python/Flask | Java/Apereo CAS |
| Authentification | Utilisateurs en mémoire | LDAP (OpenLDAP) |
| Port | 8888 | 8888 |
| Utilisation | Développement rapide | Production-ready |
| Gestion utilisateurs | Code Python | Interface LDAP (LAM) |

## 🎯 Architecture actuelle

```
Frontend (React)
    ↓
CAS Server (Apereo) ← Port 8888
    ↓
OpenLDAP ← Port 389
    ↓
LAM (Web UI) ← Port 8081
```

## 🔧 Avantages de cette solution

1. **Un seul serveur CAS** = Pas de conflit de ports
2. **LDAP** = Gestion centralisée des utilisateurs
3. **LAM** = Interface web pour créer/modifier des utilisateurs
4. **Production-ready** = Peut être utilisé en production

## 📝 Fichiers modifiés

- ✅ `docker-compose.yml` - Suppression de cas-mock, ajout de CAS + LDAP
- ✅ `scripts/create-ldap-users.bat` - Script pour créer des utilisateurs
- ✅ `.env` - Configuration CAS mise à jour
- ✅ `frontend/src/pages/LoginPage.jsx` - Bouton CAS au lieu du formulaire

## 🚀 Pour démarrer

```bash
start-with-cas.bat
```

Puis accédez à http://localhost:3000 et connectez-vous avec :
- **student1** / **password123**
- **teacher1** / **password123**

## 🆘 En cas de problème

```bash
# Vérifier l'état
check-services.bat

# Voir les logs CAS
docker logs ping61-cas

# Voir les logs LDAP
docker logs ping61-openldap

# Redémarrer tout
docker-compose restart
```
