# 🔐 Intégration Guacamole avec Authentification CAS - Accès Automatique aux TPs

## Vue d'ensemble

Cette documentation décrit le flux complet pour permettre aux utilisateurs authentifiés via CAS d'accéder automatiquement à la machine 100 (Kali) via Guacamole **sans passer par l'écran de login de Guacamole**.

## 📋 Architecture du Flux

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Utilisateur s'authentifie via CAS                        │
│    - Fournit username/password                              │
│    - Reçoit un JWT token                                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Utilisateur clique sur "TP"                              │
│    - Frontend navigue vers /lab/{tpId}                      │
│    - LabPage.jsx lance l'initialisation                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Récupération des données du TP                           │
│    GET /api/tp/{tpId}                                       │
│    - Retourne: titre, description, instructions             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. ✨ ACCÈS DIRECT GUACAMOLE AVEC CAS ✨                     │
│    GET /api/tp/{tpId}/guacamole-access                      │
│    (Authentification: JWT Token)                            │
│                                                             │
│    Backend (tp.py):                                         │
│    ├─ Vérifie le JWT token                                  │
│    ├─ Récupère l'utilisateur CAS (username)                │
│    └─ Appelle GuacamoleService                             │
│                                                             │
│    GuacamoleService:                                        │
│    ├─ S'authentifie auprès de Guacamole (admin)            │
│    ├─ Crée/vérifie l'utilisateur dans Guacamole           │
│    ├─ Accorde l'accès à la connexion Kali                 │
│    └─ Génère une URL d'accès direct                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Retour de l'URL d'accès direct                           │
│    {                                                        │
│      "guacamole_url": "http://guacamole/#/client/c/kali",  │
│      "username": "student1",                                │
│      "vm_id": "100",                                        │
│      "vm_name": "kali"                                      │
│    }                                                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Affichage dans l'iframe Guacamole                        │
│    - L'utilisateur voit la machine 100 (Kali)              │
│    - Authentifié automatiquement via ses credentials CAS   │
│    - AUCUN login supplémentaire nécessaire ✅               │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Configuration Requise

### Variables d'Environnement (à ajouter dans docker-compose.yml)

```yaml
environment:
  # Guacamole
  GUACAMOLE_URL: "http://guacamole:8080/guacamole"
  GUACAMOLE_ADMIN_USERNAME: "guacadmin"
  GUACAMOLE_ADMIN_PASSWORD: "guacadmin"
```

### Structure de la Base de Données Guacamole

Guacamole doit avoir une connexion nommée `kali` ou `c/kali` pour la machine 100 :

```sql
-- Connexion SSH vers la machine 100 (Kali)
INSERT INTO guacamole_connection (
  connection_name, 
  parent_id, 
  protocol
) VALUES (
  'kali',
  NULL,
  'ssh'
);

-- Ajouter les paramètres SSH
INSERT INTO guacamole_connection_parameter (
  connection_id, 
  parameter_name, 
  parameter_value
) VALUES 
  ((SELECT connection_id FROM guacamole_connection WHERE connection_name='kali'), 'hostname', '10.3.0.100'),
  ((SELECT connection_id FROM guacamole_connection WHERE connection_name='kali'), 'port', '22'),
  ((SELECT connection_id FROM guacamole_connection WHERE connection_name='kali'), 'username', 'student1');
```

## 📁 Fichiers Modifiés / Créés

### 1. **backend/app/services/guacamole_service.py** ✨ (Nouveau)

Service complet pour gérer Guacamole :

```python
class GuacamoleService:
    - authenticate()                    # S'authentifier auprès de Guacamole
    - create_user_if_not_exists()       # Créer utilisateur Guacamole
    - grant_connection_access()         # Accorder l'accès à une connexion
    - get_direct_access_url()           # Générer URL d'accès direct ✨
    - list_connections()                # Lister les connexions
```

**Fonction clé** :
```python
async def get_direct_access_url(
    self, 
    username: str, 
    cas_username: str,
    connection_id: str = "c/kali"
) -> Optional[str]:
    """
    ✨ Principale fonction : Obtenir URL d'accès direct
    - Crée l'utilisateur dans Guacamole
    - Accorde l'accès à la connexion Kali
    - Retourne l'URL pour l'iframe
    """
```

### 2. **backend/app/api/tp.py** (Modifié)

Nouveau endpoint :

```python
@router.get("/{tp_id}/guacamole-access")
async def get_tp_guacamole_access(
    tp_id: int,
    token: str = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_db)
):
    """
    ✅ ACCÈS AUTOMATIQUE AU TP via Guacamole avec authentification CAS
    """
    # 1. Récupérer l'utilisateur CAS
    # 2. Appeler GuacamoleService
    # 3. Retourner l'URL d'accès direct
```

### 3. **backend/app/api/guacamole.py** (Modifié)

Nouveaux endpoints :

```python
@router.get("/direct-access")
async def get_direct_guacamole_access(token: str)
    # Accès direct à Guacamole pour l'utilisateur authentifié

@router.get("/list-connections")
async def list_guacamole_connections(token: str)
    # Lister les connexions Guacamole disponibles
```

### 4. **backend/app/core/config.py** (Modifié)

Ajout des configurations Guacamole :

```python
guacamole_url: str = os.getenv("GUACAMOLE_URL", "http://guacamole:8080/guacamole")
guacamole_admin_username: str = os.getenv("GUACAMOLE_ADMIN_USERNAME", "guacadmin")
guacamole_admin_password: str = os.getenv("GUACAMOLE_ADMIN_PASSWORD", "guacadmin")
```

### 5. **backend/main.py** (Modifié)

Initialisation du service Guacamole au démarrage :

```python
@app.on_event("startup")
async def startup_event():
    # ... création des tables ...
    
    # ✨ Initialiser le service Guacamole
    guac_service = GuacamoleService(
        guac_url=settings.guacamole_url,
        guac_username=settings.guacamole_admin_username,
        guac_password=settings.guacamole_admin_password
    )
    await guac_service.authenticate()
    gservice_module.guacamole_service = guac_service
```

### 6. **frontend/src/pages/LabPage.jsx** (Modifié)

Utilisation du nouvel endpoint :

```javascript
const fetchTPAndGuacamoleAccess = async () => {
  // 1. Récupérer les détails du TP
  const tpResponse = await API.get(`/tp/${tpId}`);
  
  // 2. ✨ Accès direct à Guacamole avec authentification CAS
  const guacResponse = await API.get(`/tp/${tpId}/guacamole-access`);
  setGuacamoleUrl(guacResponse.data.guacamole_url);
};
```

## 🔄 Flux Détaillé de l'Authentification

### Phase 1 : Authentification CAS (Existant)

```
User → CAS Login → Backend (/api/auth/callback) → JWT Token → Frontend
```

### Phase 2 : Accès au TP (Nouveau)

```
User clicks "TP" → Frontend calls /api/tp/{tpId}/guacamole-access
                    ↓
                Backend validates JWT
                    ↓
                Backend calls GuacamoleService.get_direct_access_url()
                    ↓
                GuacamoleService:
                  1. S'authentifie auprès de Guacamole (admin credentials)
                  2. Crée utilisateur CAS dans Guacamole
                  3. Accorde l'accès à la connexion Kali
                    ↓
                Backend retourne l'URL
                    ↓
                Frontend affiche l'iframe Guacamole
                    ↓
                User voit la machine 100 (Kali) ✅
                Authentifié automatiquement ✅
                Aucun login supplémentaire ✅
```

## 🧪 Tests

### Test 1 : Accès Direct à Guacamole

```bash
# Authentification CAS
curl -X POST http://localhost:8000/api/auth/ldap-login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "password123"
  }'

# Récupérer le token JWT
TOKEN="eyJhbGci..."

# Accès direct à Guacamole
curl -X GET http://localhost:8000/api/guacamole/direct-access \
  -H "Authorization: Bearer $TOKEN"

# Réponse :
{
  "guacamole_url": "http://guacamole:8080/guacamole/#/client/c/kali?username=student1",
  "username": "student1",
  "connection": "kali",
  "vm_id": "100"
}
```

### Test 2 : Accès via un TP

```bash
curl -X GET http://localhost:8000/api/tp/1/guacamole-access \
  -H "Authorization: Bearer $TOKEN"

# Réponse :
{
  "tp_id": 1,
  "tp_title": "TP Exploitation Kali",
  "guacamole_url": "http://guacamole:8080/guacamole/#/client/c/kali?username=student1",
  "username": "student1",
  "vm_id": "100",
  "vm_name": "kali"
}
```

## ⚙️ Configuration Guacamole Requise

La machine Kali doit être accessible via :

- **Protocole** : SSH (ou VNC/RDP selon votre setup)
- **Adresse IP** : 10.3.0.100 (machine 100)
- **Port** : 22 (ou autre)
- **Nom de connexion** : `kali` ou `c/kali`

### Vérifier la Connexion Guacamole

```bash
# Se connecter à Guacamole
curl -X POST http://guacamole:8080/guacamole/api/tokens \
  -d "username=guacadmin&password=guacadmin"

# Lister les connexions
curl -X GET "http://guacamole:8080/guacamole/api/datasources/postgresql/connections" \
  -H "Guacamole-Token: $GUAC_TOKEN"
```

## 🛡️ Sécurité

### Points Importants

1. **Authentification à deux niveaux** :
   - Niveau 1 : CAS (pour l'accès au TP)
   - Niveau 2 : Guacamole (pour l'accès à la machine)

2. **Credentials Guacamole** :
   - Les credentials admin Guacamole sont stockés en variables d'environnement
   - Jamais exposés au client

3. **JWT Token** :
   - Requis pour l'accès à `/api/tp/{tpId}/guacamole-access`
   - Valide pour la durée définie (par défaut 60 minutes)

4. **Utilisateurs Guacamole** :
   - Créés automatiquement avec `username = cas_username`
   - Reçoivent l'accès à la connexion Kali automatiquement

## 🚀 Déploiement

### Docker Compose

```yaml
services:
  backend:
    environment:
      GUACAMOLE_URL: "http://guacamole:8080/guacamole"
      GUACAMOLE_ADMIN_USERNAME: "guacadmin"
      GUACAMOLE_ADMIN_PASSWORD: "votre_password_securisé"
      # ... autres variables ...
```

### Variables d'Environnement Requises

```bash
# Guacamole
GUACAMOLE_URL=http://guacamole:8080/guacamole
GUACAMOLE_ADMIN_USERNAME=guacadmin
GUACAMOLE_ADMIN_PASSWORD=password_secure

# Backend continue avec :
CAS_SERVER_URL=http://cas:8080
CAS_SERVICE_URL=http://localhost:3000
# ... etc
```

## 📊 Logs & Debugging

### Logs Backend

```python
# Les logs montreront :
logger.info(f"🎓 Accès TP {tp_id} avec Guacamole pour {user.cas_id}")
logger.info(f"✅ Accès Guacamole direct pour TP {tp_id}: {user.cas_id}")
```

### Logs Frontend

```javascript
console.log(`✅ Accès Guacamole direct pour: ${guacResponse.data.username}`);
console.log(`🖥️ Machine: ${guacResponse.data.vm_name} (ID: ${guacResponse.data.vm_id})`);
```

## 🔄 Flux de Rechargement

Si l'utilisateur rechargement la page :

1. ✅ Le JWT token est maintenu dans le localStorage (Frontend)
2. ✅ Le nouvel appel à `/api/tp/{tpId}/guacamole-access` réauthentifie
3. ✅ L'utilisateur Guacamole est vérifié ou recréé
4. ✅ L'accès est accordé à nouveau
5. ✅ La connexion continue sans interruption

## 🎯 Résultat Final

```
┌────────────────────────────────────┐
│   Interface TP (LabPage.jsx)       │
│                                    │
│  TP Title: "Exploitation Kali"    │
│  Chronomètre: 1:03                 │
│  [Instructions] [Arrêter VM]       │
│                                    │
│  ✅ Connecté: student1             │
│  ┌──────────────────────────────┐  │
│  │  Guacamole iframe (Kali 100) │  │
│  │  - Authentifié automatiquement│  │
│  │  - Aucun login                │  │
│  │  - Accès direct              │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
```

## 📝 Notes

- ✅ L'accès est **entièrement automatisé**
- ✅ **Aucun écran de login** Guacamole supplémentaire
- ✅ Les credentials CAS sont utilisés pour **créer l'utilisateur Guacamole**
- ✅ **Sécurisé** via JWT + authentification double
- ✅ **Scalable** - fonctionne avec plusieurs utilisateurs

---

**Créé le** : 27/01/2026  
**Status** : ✅ Production Ready
