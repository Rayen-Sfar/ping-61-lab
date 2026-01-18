# 🚀 QUICK START - Démarrage Rapide

## ⚡ En 5 minutes

### 1. Installation (Windows)
```bash
# Double-cliquez sur:
init-setup.bat

# Attendez la fin de l'installation
```

### 2. Démarrage
```bash
# Double-cliquez sur:
start-all.bat

# Attendez ~10 secondes que tout démarre
```

### 3. Ouvrez votre navigateur
```
http://localhost:3000
```

### 4. Testez!

**Login**:
- Identifiant: `test`
- Mot de passe: `test`
- Cliquez "SE CONNECTER"

**Dashboard** (vous êtes redirigé):
- Vous voyez 3 TPs de test
- Cliquez "🏫 Espace Enseignant" en haut à droite

**Admin (Gestion des TPs)**:
- Cliquez "➕ Ajouter un nouveau TP"
- Remplissez le formulaire
- Cliquez "✅ Créer le TP"
- **BOOM!** ✨ Votre TP est créé et affiché!

---

## 📋 Checklist

### Installation
- [ ] `init-setup.bat` exécuté (ou installation manuelle faite)
- [ ] PostgreSQL fonctionnant
- [ ] Dépendances Python installées
- [ ] Dépendances Node.js installées

### Démarrage
- [ ] Backend en cours d'exécution (port 8000)
- [ ] Frontend en cours d'exécution (port 3000/3001)
- [ ] Pas d'erreur dans les consoles

### Test
- [ ] Page de login affichée
- [ ] Connexion réussie
- [ ] Dashboard affiche les TPs
- [ ] Espace enseignant accessible
- [ ] Formulaire de création du TP fonctionne
- [ ] TP créé apparaît dans la liste
- [ ] TP créé apparaît dans le Dashboard après rafraîchir

---

## 🔧 Dépannage rapide

### PostgreSQL
```bash
# Vérifier si PostgreSQL démarre
psql --version

# Redémarrer PostgreSQL (Windows)
Get-Service postgresql-* | Restart-Service
```

### Frontend
```bash
# Arrêter et redémarrer
Ctrl+C
npm start
```

### Backend
```bash
# Arrêter et redémarrer
Ctrl+C
python run.py
```

### Base de données
```bash
# Réinitialiser la BD
python scripts/init_db.py
```

---

## 📞 Aide

**Les TPs ne s'affichent pas?**
- Vérifiez que le backend répond: http://localhost:8000/health
- Ouvrez F12 (console) et cherchez les erreurs
- Vérifiez que PostgreSQL est actif

**Le formulaire ne marche pas?**
- Vérifiez que tous les champs sont remplis
- Vérifiez la console F12 pour les erreurs
- Redémarrez le frontend

**"Cannot connect to database"?**
- Vérifiez que PostgreSQL est démarré
- Vérifiez le .env: `DATABASE_URL=...`
- Réinitialisez: `python scripts/init_db.py`

---

## 📚 Documentation complète

- `RESUME_MODIFICATIONS.md` - Ce qui a changé
- `TESTING_GUIDE.md` - Guide de test détaillé
- `MANIFEST.md` - Liste complète de tous les changements
- `docs/ADMIN_GUIDE.md` - Guide pour les enseignants
- `README.md` - Documentation générale

---

## 🎯 Prochaines fois

Pour démarrer à nouveau:
1. Double-cliquez `start-all.bat`
2. Attendez que ça démarre
3. Ouvrez http://localhost:3000
4. C'est prêt! 🚀

---

**Bon travail!** 🎉
