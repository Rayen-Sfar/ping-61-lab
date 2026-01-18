# 🔒 Résolution "Too many failed authentication attempts"

## ❌ Problème

Guacamole affiche : **"Too many failed authentication attempts. Please try again later."**

## 🔍 Causes possibles

1. **Tentatives de connexion échouées** - Trop d'essais avec de mauvais credentials
2. **Base de données corrompue** - Problème d'initialisation MySQL
3. **Blocage temporaire** - Sécurité Guacamole activée

## ✅ Solutions (par ordre de simplicité)

### Solution 1 : Attendre (5 minutes)
Le blocage est temporaire. Attendez 5 minutes et réessayez.

### Solution 2 : Redémarrage simple
```bash
reset-guacamole.bat
```

### Solution 3 : Reset complet (si problème persiste)
```bash
reset-guacamole-db.bat
```
⚠️ **Attention :** Supprime toutes les données Guacamole !

## 🧪 Test après correction

1. Attendez la fin du script
2. Allez sur **http://localhost:8088/guacamole/**
3. Connectez-vous avec :
   - **Username :** guacadmin
   - **Password :** guacadmin

## 🔧 Vérification des logs

```bash
# Logs Guacamole
docker logs ping61-guacamole

# Logs MySQL
docker logs ping61-mysql

# État des conteneurs
docker ps | findstr guac
```

## 📊 Erreurs courantes et solutions

| Erreur | Cause | Solution |
|--------|-------|----------|
| 429 Too Many Requests | Trop de tentatives | Attendre ou reset |
| 403 Forbidden | Credentials incorrects | Vérifier guacadmin/guacadmin |
| 500 Internal Error | Base de données | reset-guacamole-db.bat |
| Connection refused | Service arrêté | docker-compose up -d guacamole |

## 🎯 Credentials par défaut

Après reset, utilisez **toujours** :
- **Username :** guacadmin
- **Password :** guacadmin

## 🔄 Si le problème persiste

1. **Vérifiez les ports :**
   ```bash
   netstat -ano | findstr :8088
   netstat -ano | findstr :3306
   ```

2. **Redémarrez Docker Desktop**

3. **Vérifiez l'espace disque :**
   ```bash
   docker system df
   ```

4. **Nettoyage complet :**
   ```bash
   docker-compose down -v
   docker system prune -f
   docker-compose up -d
   ```

## 📝 Temps d'attente normaux

- **MySQL :** 10-20 secondes
- **Guacamole :** 30-45 secondes
- **Initialisation complète :** 1-2 minutes

## 🎉 Résultat attendu

Après correction, vous devriez voir :
- Page de login Guacamole
- Connexion réussie avec guacadmin/guacadmin
- Interface d'administration Guacamole

---

**Commande rapide :** `reset-guacamole.bat`