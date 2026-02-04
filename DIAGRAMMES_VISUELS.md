# 🎨 Diagrammes Visuels - Intégration Guacamole CAS

---

## 1️⃣ Flux d'Authentification & Accès TP

```
┌────────────────────────────────────────────────────────────────────────────┐
│                          🌐 NAVIGATEUR UTILISATEUR                         │
│                              http://localhost:3000                         │
└────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ 1. Cliquer "Login"
                                      ▼
                          ┌─────────────────────────┐
                          │   Page de Login CAS     │
                          │  Username: student1     │
                          │  Password: ••••••       │
                          └────────┬────────────────┘
                                   │
                                   │ 2. Submittre form
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      🔐 SERVEUR CAS (Port 8888)                            │
│                                                                             │
│  ✅ Valide credentials contre LDAP                                         │
│  ✅ Génère un ticket CAS                                                  │
└────────────┬────────────────────────────────────────────────────────────────┘
             │
             │ 3. Redirige vers /api/auth/callback?ticket=ST-xxx
             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    📡 BACKEND API (FastAPI Port 8000)                      │
│                   app/api/auth.py → /api/auth/callback                     │
│                                                                             │
│  ✅ Valide le ticket CAS                                                  │
│  ✅ Récupère infos utilisateur (student1)                                 │
│  ✅ Crée utilisateur local en DB si nécessaire                            │
│  ✅ Génère JWT token                                                      │
└────────────┬────────────────────────────────────────────────────────────────┘
             │
             │ 4. Redirige vers /dashboard?token=JWT&user=student1
             ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                      ⚛️  FRONTEND DASHBOARD                                │
│                  src/pages/DashboardPage.jsx                               │
│                                                                             │
│  ✅ Stock JWT dans localStorage                                           │
│  ✅ Affiche la liste des TPs                                              │
│  ✅ Utilisateur authentifié ✓ student1                                    │
└────────────┬───────────────────────────────────────────────────────────────┘
             │
             │ 5. Cliquer sur un TP
             ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                    ⚛️ FRONTEND TP PAGE (NEW!)                              │
│                    src/pages/LabPage.jsx                                   │
│                                                                             │
│  📊 État: loading = true                                                  │
│  "⏳ Initialisation de la machine virtuelle..."                            │
└────────────┬───────────────────────────────────────────────────────────────┘
             │
             │ 6. Appel API avec JWT
             │    GET /api/tp/{tpId}/guacamole-access
             │    Header: Authorization: Bearer JWT
             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    📡 BACKEND (FastAPI Port 8000)                          │
│                  app/api/tp.py → /tp/{id}/guacamole-access                │
│                                                                             │
│  ✅ Vérifie JWT token (valid? non expiré?)                               │
│  ✅ Récupère user de la DB (student1)                                     │
│  ✅ Appelle GuacamoleService.get_direct_access_url()                      │
│                                                                             │
│  Dépendances:                                                             │
│    - postgresql (DB users)                                                │
│    - guacamole API (port 8080)                                            │
└────────────┬────────────────────────────────────────────────────────────────┘
             │
             │ 7. GuacamoleService s'active!
             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│            🛠️ GUACAMOLE SERVICE (app/services/guacamole_service.py)        │
│                                                                             │
│  Étape 1: S'authentifier auprès de Guacamole (admin)                      │
│  ────────────────────────────────────────────────────────                 │
│  POST /guacamole/api/tokens                                               │
│  {username: "guacadmin", password: "guacadmin"}                           │
│        │                                                                   │
│        ▼ Obtient authToken                                                │
│                                                                            │
│  Étape 2: Créer/Vérifier utilisateur Guacamole                            │
│  ───────────────────────────────────────────────                          │
│  GET /api/users/student1  (vérifier si existe)                           │
│  Si n'existe pas:                                                         │
│    POST /api/users                                                        │
│    {username: "student1", password: "student1"}                           │
│        │                                                                   │
│        ▼ Utilisateur créé                                                 │
│                                                                            │
│  Étape 3: Accorder l'accès à la connexion Kali                            │
│  ────────────────────────────────────────────                             │
│  PATCH /api/users/student1/permissions                                    │
│  {"op": "add", "path": "/connectionPermissions/c/kali"}                   │
│        │                                                                   │
│        ▼ Permission accordée                                               │
│                                                                            │
│  Étape 4: Générer URL d'accès direct                                      │
│  ──────────────────────────────────────                                   │
│  URL = http://guacamole:8080/guacamole/#/client/c/kali                   │
│        ?username=student1                                                  │
│        │                                                                   │
│        ▼ Retourner au backend                                             │
└────────────┬────────────────────────────────────────────────────────────────┘
             │
             │ 8. Réponse JSON
             │ {
             │   "guacamole_url": "http://guacamole/...",
             │   "username": "student1",
             │   "vm_id": "100",
             │   "vm_name": "kali"
             │ }
             ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                    ⚛️ FRONTEND LabPage.jsx                                 │
│                                                                             │
│  📊 État: loading = false                                                 │
│  ✅ État: guacamoleUrl = "http://guacamole/..."                          │
│                                                                             │
│  Affichage:                                                                │
│  ┌─────────────────────────────────────────┐                              │
│  │  TP: Exploitation Kali       [Timer]    │                              │
│  ├─────────────────────────────────────────┤                              │
│  │ ✅ Connecté: student1                   │                              │
│  │ ┌─────────────────────────────────────┐ │                              │
│  │ │                                     │ │                              │
│  │ │  IFRAME GUACAMOLE (Kali Terminal)   │ │                              │
│  │ │  - Aucun écran de login             │ │                              │
│  │ │  - Utilisateur authentifié auto ✅  │ │                              │
│  │ │  - Prêt à utiliser                  │ │                              │
│  │ │                                     │ │                              │
│  │ └─────────────────────────────────────┘ │                              │
│  └─────────────────────────────────────────┘                              │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 2️⃣ Architecture Système

```
                           UTILISATEURS
                                │
                    ┌───────────┼───────────┐
                    │           │           │
                 student1    student2    teacher1
                    │           │           │
                    └───────────┼───────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   LDAP (OpenLDAP)   │ ← Authentification
                    │   port 389          │
                    └─────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
            ┌─────────┐  ┌──────────────┐ ┌──────────┐
            │   CAS   │  │  PostgreSQL  │ │   MySQL  │
            │(Auth)   │  │  (User DB)   │ │(Guacamole│
            │8888     │  │  5432        │ │ DB) 3306 │
            └────┬────┘  └──────┬───────┘ └────┬─────┘
                 │             │              │
                 └─────────────┼──────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
            ┌─────────────────┐  ┌──────────────────┐
            │  BACKEND API    │  │  GUACAMOLE +     │
            │  (FastAPI)      │  │  GUACD           │
            │  8000           │  │  8080 (proxy 4822)
            │                 │  │                  │
            │  ✅ Valide JWT  │  │  ✅ Crée users   │
            │  ✅ Auth CAS    │  │  ✅ Gère accès   │
            │  ✅ Appelle Guac│  │  ✅ Encrypte VNC │
            └────────┬────────┘  └──────────┬───────┘
                     │                      │
                     │        ┌─────────────┘
                     │        │
                     ▼        ▼
                ┌────────────────────┐
                │   FRONTEND (React) │
                │   3000             │
                │                    │
                │ ✅ Redux state     │
                │ ✅ Affiche UI      │
                │ ✅ Iframe Guacamole│
                └────────┬───────────┘
                         │
                         ▼
                   ┌──────────────┐
                   │ NAVIGATEUR   │
                   │ User Display │
                   │ http://...   │
                   └──────────────┘
```

---

## 3️⃣ Flux de Données - Requête API

```
FRONTEND (React)
    │
    │ GET /api/tp/1/guacamole-access
    │ Header: Authorization: Bearer eyJhbGci...
    │
    ▼
BACKEND (FastAPI - tp.py)
    │
    ├─ 1. verify_jwt_token(token)
    │      └─ Valide la signature JWT
    │      └─ Récupère user_id = 1
    │
    ├─ 2. db.get(User, 1)
    │      └─ Récupère user: {id: 1, cas_id: "student1"}
    │
    ├─ 3. get_guacamole_service()
    │      └─ Obtient instance GuacamoleService
    │
    ├─ 4. guac_service.get_direct_access_url(
    │      username="student1",
    │      cas_username="student1",
    │      connection_id="c/kali"
    │      )
    │
    ▼
GUACAMOLE SERVICE (Python)
    │
    ├─ 1. authenticate()
    │      POST http://guacamole:8080/guacamole/api/tokens
    │      {username: "guacadmin", password: "guacadmin"}
    │      ← authToken: "abc123xyz..."
    │
    ├─ 2. create_user_if_not_exists("student1")
    │      GET  http://guacamole:8080/guacamole/api/users/student1
    │      ├─ Existe? → Retourner True
    │      └─ N'existe pas?
    │         POST http://guacamole:8080/guacamole/api/users
    │         {username: "student1", password: "student1", ...}
    │         → Créer et retourner True
    │
    ├─ 3. grant_connection_access("student1", "c/kali")
    │      PATCH http://guacamole:8080/guacamole/api/users/student1/permissions
    │      {
    │        "op": "add",
    │        "path": "/connectionPermissions/c/kali",
    │        "value": "READ"
    │      }
    │      → Permission accordée
    │
    └─ 4. Retourner URL
         "http://guacamole:8080/guacamole/#/client/c/kali?username=student1"
    │
    ▼
BACKEND (tp.py)
    │
    └─ Retourner JSON
       {
         "tp_id": 1,
         "tp_title": "Exploitation Kali",
         "guacamole_url": "...",
         "username": "student1",
         "vm_id": "100",
         "vm_name": "kali"
       }
    │
    ▼
FRONTEND (React - LabPage.jsx)
    │
    ├─ setGuacamoleUrl(guacamole_url)
    ├─ setLoading(false)
    └─ Render:
       <iframe src={iframeSrc} />
       ↓
       GUACAMOLE INTERFACE (dans iframe)
       ├─ User student1 already authenticated ✅
       ├─ Connection c/kali accessible ✅
       └─ Affiche Terminal/VNC Kali ✅
```

---

## 4️⃣ Schéma de Base de Données

```
┌─────────────────────────────────┐
│   PostgreSQL (User DB)          │
└─────────────────────────────────┘
            │
            ▼
    ┌──────────────┐
    │ users        │
    ├──────────────┤
    │ id (PK)      │──┐
    │ cas_id       │  │ "student1"
    │ email        │  │ "student1@esigelec.fr"
    │ first_name   │  │ "Student"
    │ last_name    │  │ "One"
    │ role         │  │ "student"
    │ auth_provider│  │ "cas"
    │ is_active    │  │ true
    │ created_at   │  │ 2026-01-27
    │ last_login   │  │ 2026-01-27 18:45
    └──────────────┘  │
                      │
                      └──> ID = 1

┌─────────────────────────────────┐
│   PostgreSQL (TP DB)            │
└─────────────────────────────────┘
            │
            ▼
    ┌──────────────┐
    │ tps          │
    ├──────────────┤
    │ id (PK)      │──┐
    │ title        │  │ "Exploitation Kali"
    │ description  │  │ "..."
    │ instructions │  │ "## Objectif\n..."
    │ difficulty   │  │ "Moyen"
    │ duration     │  │ "2h"
    │ vm_type      │  │ "kali"
    │ status       │  │ "Published"
    │ created_by   │  │ "admin"
    │ created_at   │  │ 2026-01-20
    │ updated_at   │  │ 2026-01-27
    └──────────────┘  │
                      │
                      └──> ID = 1

┌─────────────────────────────────┐
│   MySQL (Guacamole DB)          │
└─────────────────────────────────┘
            │
            ▼
    ┌────────────────────┐
    │ guacamole_entity   │
    ├────────────────────┤
    │ entity_id (PK)     │
    │ name               │ "student1"
    │ type               │ "USER"
    └────────────────────┘
            ▲
            │ FK
            │
    ┌────────────────────┐
    │ guacamole_user     │
    ├────────────────────┤
    │ entity_id (FK)     │
    │ password           │ hash("student1")
    │ attributes         │ {...}
    └────────────────────┘
            ▲
            │ FK (permissions)
            │
    ┌────────────────────────────┐
    │ guacamole_user_permission  │
    ├────────────────────────────┤
    │ entity_id (FK)             │ = student1's entity_id
    │ connection_id (FK)         │ = c/kali's ID
    │ permission (enum)          │ "READ"
    └────────────────────────────┘
            ▲
            │ FK
            │
    ┌────────────────────┐
    │ guacamole_connection
    ├────────────────────┤
    │ connection_id (PK) │
    │ connection_name    │ "kali"
    │ protocol           │ "ssh"
    │ parameters: {      │
    │   hostname         │ "10.3.0.100"
    │   port             │ "22"
    │   username         │ "root"
    │ }                  │
    └────────────────────┘
```

---

## 5️⃣ Flux d'Erreur & Récupération

```
GET /api/tp/1/guacamole-access
    │
    ├─ ❌ JWT Token invalide
    │      └─ 401 Unauthorized
    │         └─ Frontend redirige vers /login
    │
    ├─ ❌ Token expiré
    │      └─ 401 Token Expired
    │         └─ Frontend redirige vers /login
    │
    ├─ ❌ TP n'existe pas
    │      └─ 404 Not Found
    │         └─ Frontend affiche erreur
    │
    ├─ ❌ Guacamole inaccessible
    │      └─ 500 Service Guacamole non disponible
    │         └─ Frontend affiche "Erreur d'accès"
    │
    ├─ ❌ Impossible créer user Guacamole
    │      └─ 500 Erreur lors de la création d'utilisateur
    │         └─ Frontend affiche erreur
    │
    └─ ✅ Tout OK
        └─ 200 OK
           └─ {guacamole_url: "..."}
              └─ Frontend affiche iframe

RETRY LOGIC:
    │
    └─ Si erreur, page de retry disponible
       ├─ Bouton "Réessayer"
       ├─ Backend re-crée user Guacamole
       ├─ Ré-accorde les permissions
       └─ Génère nouvelle URL d'accès
```

---

## 6️⃣ Timeline d'Une Session Utilisateur

```
T0:00  ├─ Utilisateur charge http://localhost:3000
       │  │
       │  ├─ Frontend affiche "Loading..."
       │  │
       │  └─ Vérifie localStorage pour JWT
       │     └─ Pas trouvé → Affiche login

T0:05  ├─ Utilisateur clique "Login with CAS"
       │  │
       │  └─ Redirection vers CAS

T0:15  ├─ Utilisateur entre credentials
       │  │ Username: student1
       │  │ Password: password
       │  │
       │  └─ Submit form

T0:20  ├─ CAS valide contre LDAP
       │  │
       │  └─ Redirige avec ticket

T0:25  ├─ Backend valide ticket CAS
       │  │
       │  ├─ Crée/Met à jour user en DB
       │  │
       │  └─ Génère JWT token

T0:30  ├─ Frontend reçoit JWT
       │  │
       │  ├─ Stock dans localStorage
       │  │
       │  └─ Affiche Dashboard

T0:40  ├─ Utilisateur clique sur TP
       │  │
       │  └─ Navigation vers /lab/1

T0:45  ├─ Frontend charge LabPage.jsx
       │  │
       │  ├─ État: loading = true
       │  │
       │  └─ Affiche "Initialisation..."

T0:50  ├─ Appel GET /api/tp/1/guacamole-access
       │  │
       │  ├─ Header: JWT Token
       │  │
       │  └─ Envoi au backend

T0:55  ├─ Backend valide JWT
       │  │
       │  ├─ Récupère user: student1
       │  │
       │  ├─ Appelle GuacamoleService
       │  │
       │  └─ Service s'authentifie auprès de Guacamole

T1:00  ├─ GuacamoleService crée user dans Guacamole
       │  │
       │  ├─ POST /guacamole/api/users/student1
       │  │
       │  └─ User créé ✅

T1:05  ├─ GuacamoleService accorde l'accès
       │  │
       │  ├─ PATCH /guacamole/api/users/student1/permissions
       │  │
       │  └─ Permission accordée ✅

T1:10  ├─ GuacamoleService génère URL
       │  │
       │  └─ "http://guacamole:8080/guacamole/#/client/c/kali?username=student1"

T1:15  ├─ Backend retourne JSON
       │  │
       │  └─ {guacamole_url: "...", username: "student1", ...}

T1:20  ├─ Frontend reçoit URL
       │  │
       │  ├─ setGuacamoleUrl(...)
       │  │
       │  ├─ setLoading(false)
       │  │
       │  └─ Render iframe

T1:25  ├─ Guacamole charge dans iframe
       │  │
       │  ├─ Student1 déjà authentifié ✅
       │  │
       │  ├─ Accès à kali accordé ✅
       │  │
       │  └─ Terminal affichée ✅

T1:30  └─ Utilisateur peut travailler sur Kali
        │ SANS AUCUN LOGIN SUPPLÉMENTAIRE ✅
        │
        └─ Session reste active pendant 60 min (JWT expire)
           Après expiration → Redirection CAS login
```

---

## 7️⃣ Comparaison: Avant vs Après

```
╔══════════════════════════════════════════════════════════════════════════╗
║                            AVANT (OLD FLOW)                             ║
╚══════════════════════════════════════════════════════════════════════════╝

User Browser
    │
    ├─ 🔐 Login CAS (1min) ────────────┐
    │  Username: student1              │
    │  Password: password              │
    │                                  │
    ├─ 🖱️ Click TP (10sec) ─────────────┤─ TOTAL TIME: 3-5 min
    │                                  │
    ├─ 🔓 Guacamole Login (30sec) ◄────┤ ❌ EXTRA LOGIN
    │  Username: student1              │ ❌ EXTRA SCREEN
    │  Password: ??                    │ ❌ CONFUSING
    │                                  │
    └─ 📱 View Terminal (2min) ─────────┘

╔══════════════════════════════════════════════════════════════════════════╗
║                            APRÈS (NEW FLOW) ✨                          ║
╚══════════════════════════════════════════════════════════════════════════╝

User Browser
    │
    ├─ 🔐 Login CAS (1min) ──────────┐
    │  Username: student1             │
    │  Password: password             │
    │                                 │
    ├─ 🖱️ Click TP (10sec) ──────────┤─ TOTAL TIME: 1.5 min
    │                                 │
    └─ 📱 View Terminal (30sec) ◄────┘ ✅ NO EXTRA LOGIN
                                       ✅ AUTOMATIC AUTH
                                       ✅ SEAMLESS UX

═════════════════════════════════════════════════════════════════════════════

Time saved per student: 2-3 minutes per TP ✅
For 30 students: 60-90 minutes saved ✅
Better UX: Seamless experience ✅
More secure: Double auth ✅
```

---

**Créé le** : 27/01/2026  
**Status** : ✅ Diagrammes Complets
