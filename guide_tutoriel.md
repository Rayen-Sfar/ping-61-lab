# Guide Tutoriel - Lab on Demand
## Création du projet de A à Z

---

## 📋 Table des matières

1. [Phase 1: Planification et Architecture](#phase-1-planification-et-architecture)
2. [Phase 2: Configuration de l'environnement](#phase-2-configuration-de-lenvironnement)
3. [Phase 3: Base de données](#phase-3-base-de-données)
4. [Phase 4: Backend (API)](#phase-4-backend-api)
5. [Phase 5: Frontend (Interface utilisateur)](#phase-5-frontend-interface-utilisateur)
6. [Phase 6: Authentification](#phase-6-authentification)
7. [Phase 7: Intégration et tests](#phase-7-intégration-et-tests)
8. [Phase 8: Déploiement](#phase-8-déploiement)
9. [Tests complets de l'application](#tests-complets-de-lapplication)

---

## Phase 1: Planification et Architecture

### Objectif
Définir l'architecture technique et fonctionnelle du projet

### Étapes

#### 1.1 Analyse des besoins
- **Objectif**: Identifier les fonctionnalités requises
- **Actions**:
  - Définir les rôles utilisateurs (Enseignant, Étudiant)
  - Lister les fonctionnalités par rôle
  - Définir les contraintes techniques

#### 1.2 Conception de l'architecture
- **Objectif**: Structurer l'application en couches
- **Actions**:
  ```
  Frontend (React) ↔ Backend (FastAPI) ↔ Database (PostgreSQL)
                           ↕
                    Services externes (CAS, VM)
  ```

#### 1.3 Choix technologiques
- **Objectif**: Sélectionner la stack technique
- **Technologies choisies**:
  - Frontend: React 19.2.3
  - Backend: FastAPI 0.104.1
  - Base de données: PostgreSQL
  - ORM: SQLAlchemy 2.0.23
  - Authentification: CAS

---

## Phase 2: Configuration de l'environnement

### Objectif
Préparer l'environnement de développement

### Étapes

#### 2.1 Structure du projet
- **Objectif**: Organiser les dossiers du projet
- **Actions**:
  ```bash
  mkdir ping-61-lab
  cd ping-61-lab
  mkdir frontend backend scripts docs
  ```

#### 2.2 Configuration Git
- **Objectif**: Initialiser le versioning
- **Actions**:
  ```bash
  git init
  # Créer .gitignore
  echo "node_modules/" > .gitignore
  echo "__pycache__/" >> .gitignore
  echo ".env" >> .gitignore
  ```

#### 2.3 Environnement Python
- **Objectif**: Configurer l'environnement backend
- **Actions**:
  ```bash
  cd backend
  python -m venv venv
  venv\Scripts\activate  # Windows
  pip install fastapi uvicorn sqlalchemy asyncpg
  ```

#### 2.4 Environnement Node.js
- **Objectif**: Configurer l'environnement frontend
- **Actions**:
  ```bash
  cd frontend
  npx create-react-app . --template typescript
  npm install axios react-router-dom
  ```

---

## Phase 3: Base de données

### Objectif
Concevoir et implémenter la structure de données

### Étapes

#### 3.1 Installation PostgreSQL
- **Objectif**: Installer et configurer PostgreSQL
- **Actions**:
  ```bash
  # Installation via installateur officiel
  # Configuration du service
  # Création de la base de données
  psql -U postgres -c "CREATE DATABASE labondemand;"
  ```

#### 3.2 Modélisation des données
- **Objectif**: Définir les entités et relations
- **Entités principales**:
  - Users (utilisateurs)
  - TPs (travaux pratiques)
  - Sessions (sessions de travail)
  - Logs (historique)

#### 3.3 Création des modèles SQLAlchemy
- **Objectif**: Implémenter les modèles de données
- **Fichier**: `backend/app/db/models.py`
- **Contenu**:
  ```python
  from sqlalchemy import Column, Integer, String, DateTime, Text
  from sqlalchemy.ext.declarative import declarative_base

  Base = declarative_base()

  class User(Base):
      __tablename__ = "users"
      id = Column(Integer, primary_key=True)
      username = Column(String(50), unique=True)
      email = Column(String(100))
      role = Column(String(20))
      created_at = Column(DateTime)

  class TP(Base):
      __tablename__ = "tps"
      id = Column(Integer, primary_key=True)
      title = Column(String(200))
      description = Column(Text)
      instructions = Column(Text)
      difficulty = Column(String(20))
      duration = Column(String(10))
      vm_type = Column(String(50))
      status = Column(String(20))
      created_by = Column(String(50))
      created_at = Column(DateTime)
  ```

#### 3.4 Script d'initialisation
- **Objectif**: Automatiser la création des tables
- **Fichier**: `scripts/init_db.py`
- **Actions**:
  - Créer les tables
  - Insérer des données de test
  - Configurer les permissions

---

## Phase 4: Backend (API)

### Objectif
Développer l'API REST avec FastAPI

### Étapes

#### 4.1 Structure du backend
- **Objectif**: Organiser le code backend
- **Structure**:
  ```
  backend/
  ├── app/
  │   ├── api/          # Routes API
  │   ├── db/           # Modèles et base de données
  │   ├── schemas/      # Schémas Pydantic
  │   ├── services/     # Logique métier
  │   └── core/         # Configuration
  └── main.py
  ```

#### 4.2 Configuration FastAPI
- **Objectif**: Initialiser l'application FastAPI
- **Fichier**: `backend/main.py`
- **Contenu**:
  ```python
  from fastapi import FastAPI
  from fastapi.middleware.cors import CORSMiddleware
  from app.api import tp, auth, admin

  app = FastAPI(title="Lab on Demand API")

  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:3000"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )

  app.include_router(tp.router, prefix="/tp")
  app.include_router(auth.router, prefix="/auth")
  app.include_router(admin.router, prefix="/admin")
  ```

#### 4.3 Développement des routes API
- **Objectif**: Implémenter les endpoints
- **Routes principales**:
  - `/tp` - CRUD des travaux pratiques
  - `/auth` - Authentification
  - `/admin` - Administration
  - `/vm` - Gestion des machines virtuelles

#### 4.4 Schémas Pydantic
- **Objectif**: Valider les données d'entrée/sortie
- **Fichier**: `backend/app/schemas/tp.py`
- **Contenu**:
  ```python
  from pydantic import BaseModel
  from datetime import datetime

  class TPBase(BaseModel):
      title: str
      description: str
      instructions: str
      difficulty: str
      duration: str
      vm_type: str

  class TPCreate(TPBase):
      pass

  class TPResponse(TPBase):
      id: int
      status: str
      created_by: str
      created_at: datetime
  ```

---

## Phase 5: Frontend (Interface utilisateur)

### Objectif
Développer l'interface utilisateur avec React

### Étapes

#### 5.1 Structure du frontend
- **Objectif**: Organiser les composants React
- **Structure**:
  ```
  frontend/src/
  ├── components/       # Composants réutilisables
  ├── pages/           # Pages de l'application
  ├── services/        # Services API
  ├── context/         # Context React
  └── styles/          # Fichiers CSS
  ```

#### 5.2 Configuration du routage
- **Objectif**: Configurer React Router
- **Fichier**: `frontend/src/App.js`
- **Contenu**:
  ```jsx
  import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
  import LoginPage from './pages/LoginPage';
  import DashboardPage from './pages/DashboardPage';
  import AdminPage from './pages/AdminPage';
  import LabPage from './pages/LabPage';

  function App() {
    return (
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/lab/:id" element={<LabPage />} />
        </Routes>
      </Router>
    );
  }
  ```

#### 5.3 Services API
- **Objectif**: Créer les services pour communiquer avec l'API
- **Fichier**: `frontend/src/services/api.js`
- **Contenu**:
  ```javascript
  import axios from 'axios';

  const API_BASE_URL = 'http://localhost:8000';

  const api = axios.create({
    baseURL: API_BASE_URL,
    withCredentials: true,
  });

  export const tpService = {
    getAllTPs: () => api.get('/tp'),
    getTP: (id) => api.get(`/tp/${id}`),
    createTP: (data) => api.post('/tp', data),
    deleteTP: (id) => api.delete(`/tp/${id}`),
  };

  export const authService = {
    login: (credentials) => api.post('/auth/login', credentials),
    logout: () => api.post('/auth/logout'),
  };
  ```

#### 5.4 Développement des pages
- **Objectif**: Créer les interfaces utilisateur
- **Pages principales**:
  - LoginPage - Authentification
  - DashboardPage - Liste des TPs
  - AdminPage - Gestion des TPs
  - LabPage - Interface de travail

#### 5.5 Gestion d'état
- **Objectif**: Gérer l'état global avec Context API
- **Fichier**: `frontend/src/context/AuthContext.js`
- **Contenu**:
  ```jsx
  import React, { createContext, useContext, useState } from 'react';

  const AuthContext = createContext();

  export const useAuth = () => useContext(AuthContext);

  export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const login = (userData) => {
      setUser(userData);
      setIsAuthenticated(true);
    };

    const logout = () => {
      setUser(null);
      setIsAuthenticated(false);
    };

    return (
      <AuthContext.Provider value={{ user, isAuthenticated, login, logout }}>
        {children}
      </AuthContext.Provider>
    );
  };
  ```

---

## Phase 6: Authentification

### Objectif
Implémenter l'authentification CAS et le système de sessions

### Étapes

#### 6.1 Configuration CAS
- **Objectif**: Intégrer l'authentification CAS d'Esigelec
- **Actions**:
  - Configurer les URLs CAS
  - Implémenter le callback CAS
  - Gérer les sessions utilisateur

#### 6.2 Middleware d'authentification
- **Objectif**: Sécuriser les routes API
- **Fichier**: `backend/app/core/auth.py`
- **Contenu**:
  ```python
  from fastapi import Depends, HTTPException, status
  from fastapi.security import HTTPBearer

  security = HTTPBearer()

  async def get_current_user(token: str = Depends(security)):
      # Validation du token
      # Récupération des informations utilisateur
      pass

  def require_admin(user = Depends(get_current_user)):
      if user.role != "admin":
          raise HTTPException(status_code=403, detail="Admin required")
      return user
  ```

#### 6.3 Mode développement
- **Objectif**: Faciliter le développement sans CAS
- **Actions**:
  - Créer un système d'authentification de test
  - Comptes par défaut (testuser/password)
  - Basculement automatique si CAS indisponible

---

## Phase 7: Intégration et tests

### Objectif
Intégrer tous les composants et effectuer les tests

### Étapes

#### 7.1 Tests unitaires backend
- **Objectif**: Tester les fonctions individuelles
- **Framework**: pytest
- **Fichiers de test**: `backend/tests/`

#### 7.2 Tests d'intégration
- **Objectif**: Tester les interactions entre composants
- **Actions**:
  - Tests API avec des données réelles
  - Tests de la base de données
  - Tests d'authentification

#### 7.3 Tests frontend
- **Objectif**: Tester l'interface utilisateur
- **Framework**: Jest + React Testing Library
- **Types de tests**:
  - Tests de composants
  - Tests d'intégration
  - Tests end-to-end

#### 7.4 Scripts d'automatisation
- **Objectif**: Automatiser le démarrage et les tests
- **Fichiers**:
  - `init-setup.bat` - Installation automatique
  - `start-dev.bat` - Démarrage en mode développement
  - `run-tests.bat` - Exécution des tests

---

## Phase 8: Déploiement

### Objectif
Préparer et déployer l'application en production

### Étapes

#### 8.1 Configuration de production
- **Objectif**: Adapter la configuration pour la production
- **Actions**:
  - Variables d'environnement
  - Configuration HTTPS
  - Optimisation des performances

#### 8.2 Containerisation (optionnel)
- **Objectif**: Faciliter le déploiement avec Docker
- **Fichiers**:
  - `Dockerfile` pour backend et frontend
  - `docker-compose.yml` pour l'orchestration

#### 8.3 Documentation
- **Objectif**: Documenter l'installation et l'utilisation
- **Fichiers**:
  - README.md
  - Guide administrateur
  - Documentation API

---

## Tests complets de l'application

### 1. Tests fonctionnels

#### 1.1 Tests d'authentification
```bash
# Test de connexion CAS
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password"}'

# Test de déconnexion
curl -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer <token>"

# Test d'accès non autorisé
curl -X GET http://localhost:8000/admin/users
```

#### 1.2 Tests CRUD des TPs
```bash
# Créer un TP
curl -X POST http://localhost:8000/tp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "title": "TP Test",
    "description": "Description test",
    "instructions": "Instructions test",
    "difficulty": "Facile",
    "duration": "2h",
    "vm_type": "Linux"
  }'

# Lister tous les TPs
curl -X GET http://localhost:8000/tp

# Récupérer un TP spécifique
curl -X GET http://localhost:8000/tp/1

# Supprimer un TP
curl -X DELETE http://localhost:8000/tp/1 \
  -H "Authorization: Bearer <token>"
```

#### 1.3 Tests de l'interface utilisateur
```javascript
// Test de navigation
describe('Navigation Tests', () => {
  test('should navigate to dashboard after login', () => {
    // Simuler la connexion
    // Vérifier la redirection
  });

  test('should display TPs list', () => {
    // Charger la page dashboard
    // Vérifier l'affichage des TPs
  });
});

// Test de création de TP
describe('TP Creation Tests', () => {
  test('should create new TP', () => {
    // Remplir le formulaire
    // Soumettre
    // Vérifier la création
  });
});
```

### 2. Tests de performance

#### 2.1 Tests de charge API
```bash
# Test avec Apache Bench
ab -n 1000 -c 10 http://localhost:8000/tp

# Test avec curl en boucle
for i in {1..100}; do
  curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/tp
done
```

#### 2.2 Tests de performance frontend
```javascript
// Test de temps de chargement
describe('Performance Tests', () => {
  test('should load dashboard in less than 2 seconds', () => {
    const start = Date.now();
    // Charger la page
    const loadTime = Date.now() - start;
    expect(loadTime).toBeLessThan(2000);
  });
});
```

### 3. Tests de sécurité

#### 3.1 Tests d'injection SQL
```bash
# Test d'injection dans les paramètres
curl "http://localhost:8000/tp?search='; DROP TABLE tps; --"

# Test d'injection dans le body
curl -X POST http://localhost:8000/tp \
  -H "Content-Type: application/json" \
  -d '{"title": "'; DROP TABLE tps; --"}'
```

#### 3.2 Tests XSS
```javascript
// Test d'injection de script
const maliciousInput = '<script>alert("XSS")</script>';
// Tenter d'injecter dans les champs de formulaire
```

#### 3.3 Tests d'autorisation
```bash
# Test d'accès admin sans permissions
curl -X GET http://localhost:8000/admin/users \
  -H "Authorization: Bearer <student_token>"

# Test de modification de TP par un étudiant
curl -X DELETE http://localhost:8000/tp/1 \
  -H "Authorization: Bearer <student_token>"
```

### 4. Tests d'intégration

#### 4.1 Tests base de données
```python
# Test de connexion PostgreSQL
def test_database_connection():
    # Tester la connexion
    # Vérifier les tables
    # Tester les requêtes

# Test de migration
def test_database_migration():
    # Exécuter les migrations
    # Vérifier la structure
```

#### 4.2 Tests API complète
```python
# Test du workflow complet
def test_complete_workflow():
    # 1. Connexion utilisateur
    # 2. Création d'un TP
    # 3. Consultation du TP
    # 4. Modification du TP
    # 5. Suppression du TP
    # 6. Déconnexion
```

### 5. Tests de compatibilité

#### 5.1 Tests navigateurs
- Chrome (dernière version)
- Firefox (dernière version)
- Edge (dernière version)
- Safari (si disponible)

#### 5.2 Tests responsive
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

### 6. Scripts de test automatisés

#### 6.1 Script de test complet
```bash
# test-all.bat
@echo off
echo "=== Tests Backend ==="
cd backend
python -m pytest tests/ -v

echo "=== Tests Frontend ==="
cd ../frontend
npm test -- --coverage

echo "=== Tests API ==="
cd ../scripts
python test_api.py

echo "=== Tests de performance ==="
ab -n 100 -c 5 http://localhost:8000/tp

echo "Tests terminés !"
```

#### 6.2 Tests de régression
```bash
# Avant chaque release
# 1. Tests fonctionnels complets
# 2. Tests de performance
# 3. Tests de sécurité
# 4. Tests de compatibilité
```

### 7. Monitoring et logs

#### 7.1 Tests de logging
```python
# Vérifier que les logs sont générés
def test_logging():
    # Effectuer une action
    # Vérifier la présence du log
    # Vérifier le format du log
```

#### 7.2 Tests de monitoring
```bash
# Vérifier les métriques
curl http://localhost:8000/health
curl http://localhost:8000/metrics
```

---

## Conclusion

Ce guide présente une approche structurée pour développer Lab on Demand de A à Z. Chaque phase a des objectifs clairs et des étapes détaillées. Les tests couvrent tous les aspects : fonctionnalité, performance, sécurité et compatibilité.

**Points clés du succès :**
- Architecture modulaire et évolutive
- Tests automatisés à chaque étape
- Documentation complète
- Sécurité intégrée dès le début
- Interface utilisateur intuitive

**Prochaines étapes :**
- Intégration continue (CI/CD)
- Monitoring en production
- Évolutions fonctionnelles
- Optimisations de performance

---

*Guide créé pour le projet Lab on Demand - ESIGELEC Promo Ing61*
*Dernière mise à jour : 16 janvier 2026*