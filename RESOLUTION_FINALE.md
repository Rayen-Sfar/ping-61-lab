# 🔧 Résolution Finale - Ticket CAS + Guacamole

## ❌ Problèmes

1. **"Échec de l'authentification CAS"** - Le backend ne peut pas valider le ticket
2. **Guacamole 404** - URL incorrecte

## ✅ Corrections appliquées

### 1. URL de service CAS corrigée
Le service CAS utilisait la mauvaise URL de callback.

**Avant:**
```python
service_url=f"{settings.cas_service_url}/api/auth/callback"
```

**Après:**
```python
service_url=settings.cas_service_url  # http://localhost:3000
```

### 2. Logs ajoutés
Ajout de logs détaillés pour déboguer le flux CAS.

### 3. Guacamole URL
L'URL correcte est: **http://localhost:8088/guacamole/** (avec `/guacamole/`)

## 🚀 Correction rapide

```bash
fix-final.bat
```

## 🧪 Test complet

### 1. Test CAS
```bash
# Vérifier que CAS répond
curl http://localhost:8888/cas/login

# Voir les logs CAS
docker logs ping61-cas
```

### 2. Test Backend
```bash
# Vérifier que le backend répond
curl http://localhost:8000/health

# Voir les logs backend
docker logs -f ping61-backend
```

### 3. Test Guacamole
```bash
# URL correcte avec /guacamole/
curl http://localhost:8088/guacamole/

# Logs Guacamole
docker logs ping61-guacamole
```

### 4. Test d'authentification complet

1. Ouvrez http://localhost:3000
2. Cliquez "SE CONNECTER VIA CAS"
3. Connectez-vous avec **student1** / **password123**
4. Regardez les logs backend en temps réel:
   ```bash
   docker logs -f ping61-backend
   ```

Vous devriez voir:
```
🎫 Callback CAS reçu avec ticket: ST-xxxxx
🔍 Validation du ticket auprès de CAS: http://cas:8080
✅ Validation CAS réussie pour: student1
✅ JWT généré pour student1
```

## 📊 Flux CAS corrigé

```
1. Frontend → Clic "SE CONNECTER VIA CAS"
   ↓
2. Frontend → GET /api/auth/login
   ↓
3. Backend → Retourne http://localhost:8888/cas/login?service=http://localhost:3000
   ↓
4. CAS → Affiche formulaire
   ↓
5. Utilisateur → student1 / password123
   ↓
6. CAS → Valide contre LDAP
   ↓
7. CAS → Génère ticket ST-xxxxx
   ↓
8. CAS → Redirige vers http://localhost:3000?ticket=ST-xxxxx
   ↓
9. Frontend → GET /api/auth/callback?ticket=ST-xxxxx
   ↓
10. Backend → Valide ticket auprès de http://cas:8080/cas/validate?ticket=ST-xxxxx&service=http://localhost:3000
    ↓
11. CAS → Retourne XML avec infos utilisateur
    ↓
12. Backend → Crée/met à jour utilisateur en DB
    ↓
13. Backend → Génère JWT
    ↓
14. Frontend → Stocke JWT
    ↓
15. Frontend → Redirige vers /dashboard
```

## 🐛 Si ça ne marche toujours pas

### Erreur "Échec de l'authentification CAS"

```bash
# 1. Voir les logs backend en temps réel
docker logs -f ping61-backend

# 2. Tester la validation CAS manuellement
# Connectez-vous sur CAS et récupérez un ticket
# Puis testez:
curl "http://localhost:8888/cas/validate?ticket=ST-xxxxx&service=http://localhost:3000"
```

### Guacamole 404

L'URL correcte est: **http://localhost:8088/guacamole/**

Credentials par défaut:
- Username: **guacadmin**
- Password: **guacadmin**

Si ça ne marche pas:
```bash
# Vérifier que MySQL est prêt
docker logs ping61-mysql

# Vérifier que guacd tourne
docker ps | findstr guacd

# Redémarrer Guacamole
docker-compose restart guacamole
```

## 📝 Variables d'environnement importantes

```env
# Backend
CAS_SERVER_URL=http://cas:8080              # URL interne
CAS_SERVER_URL_PUBLIC=http://localhost:8888  # URL publique
CAS_SERVICE_URL=http://localhost:3000        # URL du frontend
JWT_SECRET_KEY=your-secret-key-change-in-production
```

## ✅ Checklist finale

- [ ] Backend redémarré
- [ ] CAS redémarré
- [ ] Guacamole redémarré
- [ ] Logs backend affichent les messages de debug
- [ ] Test CAS réussi (student1 / password123)
- [ ] Redirection vers dashboard fonctionne
- [ ] Guacamole accessible sur /guacamole/

## 🎯 Commandes utiles

```bash
# Tout redémarrer
docker-compose restart

# Voir tous les logs
docker-compose logs -f

# Voir logs d'un service spécifique
docker logs -f ping61-backend
docker logs -f ping61-cas
docker logs -f ping61-guacamole

# Rebuild si nécessaire
docker-compose build --no-cache backend cas
docker-compose up -d
```

---

**Commande rapide:** `fix-final.bat`
