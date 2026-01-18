# 🖥️ Guide Guacamole - Accès aux VMs

## ❌ Erreur 404 sur http://localhost:8088/

C'est **normal** ! Guacamole n'a pas de page d'accueil sur la racine.

## ✅ URL correcte

**http://localhost:8088/guacamole/**

⚠️ **Important :** N'oubliez pas le `/guacamole/` à la fin !

## 🔑 Credentials par défaut

- **Username :** guacadmin
- **Password :** guacadmin

## 🧪 Test rapide

```bash
debug-guacamole.bat
```

## 📊 URLs Guacamole

| URL | Statut | Description |
|-----|--------|-------------|
| http://localhost:8088/ | ❌ 404 | Racine (pas de contenu) |
| http://localhost:8088/guacamole/ | ✅ 200 | Interface Guacamole |
| http://localhost:8088/guacamole/api/ | ✅ 200 | API Guacamole |

## 🔧 Si Guacamole ne fonctionne pas

### 1. Vérifier que les conteneurs tournent
```bash
docker ps | findstr guac
```

Vous devriez voir :
- ping61-guacamole
- ping61-guacd
- ping61-mysql

### 2. Vérifier les logs
```bash
docker logs ping61-guacamole
docker logs ping61-mysql
```

### 3. Redémarrer Guacamole
```bash
docker-compose restart guacamole guacd mysql
```

### 4. Attendre 30 secondes
Guacamole prend du temps à démarrer car il doit :
- Attendre que MySQL soit prêt
- Initialiser la base de données
- Démarrer l'interface web

## 🎯 Intégration avec Lab on Demand

Dans le futur, quand un étudiant clique "Commencer le TP", l'application :

1. **Crée une VM** via Proxmox
2. **Configure l'accès** dans Guacamole
3. **Redirige** vers Guacamole avec connexion automatique
4. **L'étudiant** accède à sa VM via le navigateur

## 🔗 URLs importantes

- **Interface Guacamole :** http://localhost:8088/guacamole/
- **API Guacamole :** http://localhost:8088/guacamole/api/
- **Documentation :** https://guacamole.apache.org/doc/

## 📝 Configuration actuelle

Guacamole est configuré avec :
- **Base de données :** MySQL (ping61-mysql)
- **Daemon :** guacd (ping61-guacd)
- **Port :** 8088
- **Protocoles supportés :** VNC, RDP, SSH

---

**URL à retenir :** http://localhost:8088/guacamole/