# Guide d'Utilisation - Espace Enseignant (AdminPage)

## Vue d'ensemble

L'**Espace Enseignant** vous permet de créer, gérer et publier des Travaux Pratiques (TPs) pour vos étudiants. Les TPs sont stockés dans une base de données PostgreSQL et sont immédiatement disponibles pour les étudiants sur leur dashboard.

## Fonctionnalités Principales

### 1. **Créer un nouveau TP**

#### Accès
- Depuis le Dashboard étudiant, cliquez sur le bouton **"🏫 Espace Enseignant"** en haut à droite
- Vous serez redirigé vers la page de gestion des TPs

#### Formulaire de création
1. Cliquez sur **"➕ Ajouter un nouveau TP"**
2. Remplissez les champs suivants:

| Champ | Type | Description | Obligatoire |
|-------|------|-------------|-------------|
| **Titre du TP** | Texte | Ex: "TP 1 - Introduction à Linux" | ✅ Oui |
| **Description** | Texte long | Résumé de 2-3 lignes décrivant l'objectif du TP | ✅ Oui |
| **Instructions** | Texte long | Détails complets des étapes (supporte Markdown) | ✅ Oui |
| **Difficulté** | Sélecteur | Facile / Moyen / Difficile | ❌ Non |
| **Durée estimée** | Sélecteur | 1h / 2h / 3h / 4h | ❌ Non |
| **Type de VM** | Sélecteur | Linux / Windows / Docker / Kubernetes | ❌ Non |
| **Statut** | Sélecteur | Published / Draft / Archived | ❌ Non |

3. Cliquez sur **"✅ Créer le TP"**

#### Exemple de TP
```
Titre: TP 1 - Introduction à Linux
Description: Apprendre les commandes de base Linux et la navigation dans le système de fichiers

Instructions:
# Instructions TP 1

## Objectifs
1. Connectez-vous à la VM
2. Apprenez les commandes de base
3. Créez une arborescence de fichiers

## Étapes
1. Lancez la VM Linux
2. Ouvrez un terminal
3. Tapez: ls -la
4. Créez un dossier: mkdir mon-projet
5. Entrez dans le dossier: cd mon-projet
```

### 2. **Afficher la liste des TPs**

Tous les TPs créés s'affichent dans la section **"📚 Liste des TPs"** avec:
- Le titre du TP
- Le statut (Published/Draft/Archived)
- La description
- Les métadonnées (Difficulté, Durée, Type VM)
- Le nom du créateur
- Un bouton pour supprimer le TP

### 3. **Supprimer un TP**

1. Localisez le TP dans la liste
2. Cliquez sur le bouton **"🗑️ Supprimer"**
3. Confirmez la suppression dans la boîte de dialogue

## Architecture de la Base de Données

### Table `tps`

```sql
CREATE TABLE tps (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    instructions TEXT,
    difficulty VARCHAR DEFAULT 'Moyen',
    duration VARCHAR DEFAULT '2h',
    created_by VARCHAR,
    vm_type VARCHAR,
    status VARCHAR DEFAULT 'Published',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Champs
- **id**: Identifiant unique du TP
- **title**: Titre du TP
- **description**: Description courte
- **instructions**: Instructions détaillées (format libre)
- **difficulty**: Niveau de difficulté
- **duration**: Durée estimée
- **created_by**: Nom du créateur
- **vm_type**: Type de machine virtuelle
- **status**: État du TP (Published/Draft/Archived)
- **created_at**: Date de création
- **updated_at**: Date de dernière modification

## API Backend

### Créer un TP
```http
POST /tp
Content-Type: application/json

{
  "title": "TP 1: Introduction à Linux",
  "description": "Apprendre les commandes de base",
  "instructions": "# Instructions...",
  "difficulty": "Facile",
  "duration": "2h",
  "vm_type": "Linux",
  "status": "Published",
  "created_by": "Enseignant"
}

Response 201:
{
  "id": 1,
  "title": "TP 1: Introduction à Linux",
  ...
}
```

### Récupérer tous les TPs
```http
GET /tp

Response 200:
[
  {
    "id": 1,
    "title": "TP 1: Introduction à Linux",
    "description": "Apprendre les commandes de base",
    ...
  }
]
```

### Récupérer un TP spécifique
```http
GET /tp/{tp_id}

Response 200:
{
  "id": 1,
  "title": "TP 1: Introduction à Linux",
  ...
}
```

### Supprimer un TP
```http
DELETE /tp/{tp_id}

Response 204 No Content
```

## Installation et Configuration

### Configuration PostgreSQL

1. **Installer PostgreSQL** (si pas déjà installé)
   - Windows: https://www.postgresql.org/download/windows/
   - Notez l'utilisateur (par défaut `postgres`) et le mot de passe

2. **Configuration de la base de données**
   
   Modifiez le fichier `.env` à la racine du projet:
   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/labondemand
   ```

3. **Initialiser la base de données**
   
   Option 1 - Script automatique (Windows):
   ```bash
   init-setup.bat
   ```
   
   Option 2 - Manuel (Python):
   ```bash
   cd backend
   python ../scripts/init_db.py
   cd ..
   ```

### Démarrer le Backend

```bash
cd backend
python main.py
```

Le backend démarre sur `http://localhost:8000`

### Démarrer le Frontend

```bash
cd frontend
npm start
```

Le frontend démarre sur `http://localhost:3000` ou `http://localhost:3001`

## Flux Utilisateur Complet

### Pour l'Enseignant:
1. ✅ Se connecter via la page Login
2. ✅ Cliquer sur "🏫 Espace Enseignant"
3. ✅ Cliquer sur "➕ Ajouter un nouveau TP"
4. ✅ Remplir les champs du formulaire
5. ✅ Cliquer sur "✅ Créer le TP"
6. ✅ Le TP est immédiatement stocké dans PostgreSQL

### Pour l'Étudiant:
1. ✅ Se connecter via la page Login
2. ✅ Voir la liste des TPs sur le Dashboard
3. ✅ Cliquer sur "▶️ Commencer le TP" pour démarrer

## Statuts des TPs

- **Published**: TP visible et accessible aux étudiants
- **Draft**: TP en cours de rédaction, non visible
- **Archived**: TP archivé, non visible mais conservé

## Markdown dans les Instructions

Les instructions supportent le Markdown pour un meilleur formatage:

```markdown
# Titre principal
## Sous-titre
- Liste à puces
- Élément 2

1. Liste numérotée
2. Élément 2

**Texte en gras**
*Texte en italique*
`Code inline`

```code block```
```

## Dépannage

### Erreur: "Cannot connect to database"
- Vérifiez que PostgreSQL est installé et démarré
- Vérifiez les credentials dans `.env`
- Essayez: `psql -U postgres` dans un terminal

### Les TPs ne s'affichent pas dans le Dashboard
- Vérifiez que le backend répond: `http://localhost:8000/health`
- Vérifiez la console du navigateur (F12) pour les erreurs
- Redémarrez le frontend: `npm start`

### Erreur de création de TP
- Assurez-vous que tous les champs obligatoires sont remplis
- Vérifiez que PostgreSQL est accessible
- Vérifiez les logs du backend

## Support

Pour plus d'informations, consultez:
- Documentation API: `docs/API.md`
- Architecture: `docs/ARCHITECTURE.md`
- Installation: `docs/INSTALLATION.md`
