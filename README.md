# 🚀 Lab on Demand - Plateforme de Travaux Pratiques

##  Vue d'ensemble

**Lab on Demand** est une plateforme complète pour la gestion et l'exécution de Travaux Pratiques (TPs) en environnement virtualisé. Elle permet aux enseignants de créer des TPs et aux étudiants de les exécuter dans un environnement sécurisé et isolé.

### ✨ Fonctionnalités principales

-  **Authentification CAS** - Intégration avec le système CAS d'Esigelec
-  **Espace Enseignant** - Création et gestion des TPs via une interface web
-  **Base de données PostgreSQL** - Stockage persistant des TPs
-  **Dashboard Étudiant** - Affichage des TPs disponibles
-  **Machine Virtuelle** - Accès à des VMs via Guacamole
-  **Interface moderne** - Design responsive et intuitif

##  Architecture

```
<img width="1483" height="892" alt="image" src="https://github.com/user-attachments/assets/194fb45a-a823-4630-9c7f-405ec0aae511" />

```

## 📦 Technologies utilisées

### Frontend
- **React** 19.2.3 - Framework UI
- **React Router** 7.12.0 - Routage
- **Axios** 1.13.2 - Client HTTP
- **CSS3** - Styling

### Backend
- **FastAPI** 0.104.1 - Framework API
- **SQLAlchemy** 2.0.23 - ORM
- **AsyncPG** 0.29.0 - Driver PostgreSQL asynchrone
- **Pydantic** 2.5.0 - Validation des données

### Base de données
- **PostgreSQL** - SGBD relationnel

## 🚀 Démarrage rapide

### Prérequis
- Node.js 18+
- Python 3.8+
- PostgreSQL 12+

### Installation automatique (Windows)

```bash
init-setup.bat
```

### Installation manuelle

#### 1. Configuration de PostgreSQL
```bash
# Créer la base de données
psql -U postgres -c "CREATE DATABASE labondemand;"

# Mettre à jour le fichier .env
# DATABASE_URL=postgresql://postgres:password@localhost:5432/labondemand
```

#### 2. Installation du backend
```bash
cd backend
pip install -r requirements.txt

# Initialiser la base de données
python ../scripts/init_db.py
```

#### 3. Installation du frontend
```bash
cd frontend
npm install
```

## 🎯 Utilisation

### Démarrer le backend
```bash
cd backend
python main.py
```
Le backend démarre sur `http://localhost:8000`

### Démarrer le frontend
```bash
cd frontend
npm start
```
Le frontend démarre sur `http://localhost:3000` ou `http://localhost:3001`

### Accéder à l'application
Ouvrez votre navigateur sur `http://localhost:3000`

## 📚 Guides détaillés

- [Guide Enseignant (Admin)](docs/ADMIN_GUIDE.md) - Création et gestion des TPs
- [API Documentation](docs/API.md) - Endpoints et modèles
- [Architecture](docs/ARCHITECTURE.md) - Vue technique détaillée
- [Installation](docs/INSTALLATION.md) - Détails d'installation

## 🔑 Comptes par défaut

### Authentification en développement
- Utilisateur: `testuser`
- Mot de passe: `password`

L'authentification CAS est automatiquement redéfinie en mode dev si la connexion échoue.

##  Structure des données

### Modèle TP
```python
{
    "id": 1,
    "title": "TP 1: Introduction à Linux",
    "description": "Apprendre les commandes de base",
    "instructions": "# Instructions...",
    "difficulty": "Facile",
    "duration": "2h",
    "vm_type": "Linux",
    "status": "Published",
    "created_by": "Enseignant",
    "created_at": "2024-01-16T10:30:00",
    "updated_at": "2024-01-16T10:30:00"
}
```

##  Endpoints API

### TPs
- `GET /tp` - Liste tous les TPs
- `POST /tp` - Créer un nouveau TP
- `GET /tp/{id}` - Récupérer un TP spécifique
- `DELETE /tp/{id}` - Supprimer un TP

### Authentification
- `POST /auth/login` - Se connecter
- `GET /auth/cas/callback` - Callback CAS
- `POST /auth/logout` - Se déconnecter

## Développement

### Structure du projet
```
.
├── frontend/                 # Application React
│   ├── public/              # Fichiers statiques
│   ├── src/
│   │   ├── components/      # Composants réutilisables
│   │   ├── pages/          # Pages de l'application
│   │   ├── services/       # Services API
│   │   ├── context/        # Context React
│   │   └── styles/         # Fichiers CSS
│   └── package.json
│
├── backend/                  # Application FastAPI
│   ├── app/
│   │   ├── api/            # Routes API
│   │   ├── db/             # Modèles et base de données
│   │   ├── schemas/        # Schémas Pydantic
│   │   ├── services/       # Logique métier
│   │   └── core/           # Configuration
│   ├── main.py
│   └── requirements.txt
│
├── scripts/                  # Scripts utilitaires
│   ├── init_db.py          # Initialisation BD
│   └── init-db-postgresql.sql
│
├── docs/                     # Documentation
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── INSTALLATION.md
│   └── ADMIN_GUIDE.md
│
└── README.md
```

##  Dépannage

### PostgreSQL ne démarre pas
```bash
# Vérifier l'installation
psql --version

# Vérifier le service (Windows)
Get-Service postgresql-*
```

### Le frontend ne se connecte pas au backend
- Vérifiez que le backend démarre sur le port 8000
- Vérifiez la console du navigateur (F12)
- Essayez: `curl http://localhost:8000/health`

### Erreur de base de données
- Vérifiez les credentials dans `.env`
- Vérifiez que la base existe: `psql -l`
- Réinitialisez: `python scripts/init_db.py`

##  Documentation supplémentaire

Consultez les fichiers dans le dossier `docs/` pour plus de détails:
- Configuration détaillée
- Intégration CAS
- API complète
- Architecture système

---

**Dernière mise à jour**: 16 janvier 2026
# last-version



