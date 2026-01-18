#!/usr/bin/env python3
"""
Script de démarrage du serveur backend Lab on Demand
Vérifie les configurations et initialise la base de données si nécessaire
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path

# Ajouter le répertoire courant au chemin Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("  🚀 Lab on Demand - Backend Startup")
print("=" * 70)
print()

# Vérifier les prérequis
print("📋 Vérification des prérequis...")
print()

# 1. Vérifier Python version
python_version = sys.version_info
if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
    print("❌ Python 3.8+ requis")
    sys.exit(1)
else:
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")

# 2. Vérifier les variables d'environnement
env_file = Path(".env")
if env_file.exists():
    print("✅ Fichier .env trouvé")
    # Charger les variables
    from dotenv import load_dotenv
    load_dotenv()
else:
    print("⚠️  Fichier .env non trouvé, utilisation des valeurs par défaut")

# 3. Vérifier la base de données
print()
print("🔍 Vérification de la configuration de la base de données...")
db_url = os.getenv("DATABASE_URL", "sqlite:///./labondemand.db")
print(f"   URL: {db_url}")

if "postgresql" in db_url:
    print("✅ Utilisation de PostgreSQL")
    print()
    print("⏳ Tentative de connexion à PostgreSQL...")
    
    # Tenter une connexion
    try:
        import asyncpg
        from sqlalchemy.ext.asyncio import create_async_engine
        
        async def check_db():
            if db_url.startswith("postgresql://"):
                url = db_url.replace("postgresql://", "postgresql+asyncpg://")
            else:
                url = db_url
            
            try:
                engine = create_async_engine(url, echo=False)
                async with engine.begin() as conn:
                    await conn.exec_driver_sql("SELECT 1")
                await engine.dispose()
                return True
            except Exception as e:
                print(f"   ❌ Erreur de connexion: {e}")
                return False
        
        result = asyncio.run(check_db())
        if result:
            print("   ✅ Connexion à PostgreSQL établie")
        else:
            print("   ⚠️  Impossible de se connecter à PostgreSQL")
            print("   Assurez-vous que PostgreSQL est démarré")
    except ImportError:
        print("   ⚠️  asyncpg non installé, installation des dépendances recommandée")
elif "sqlite" in db_url:
    print("✅ Utilisation de SQLite")

print()
print("📦 Vérification des dépendances Python...")
try:
    import fastapi
    print(f"✅ FastAPI {fastapi.__version__}")
except ImportError:
    print("❌ FastAPI non installé, exécutez: pip install -r requirements.txt")
    sys.exit(1)

try:
    import sqlalchemy
    print(f"✅ SQLAlchemy {sqlalchemy.__version__}")
except ImportError:
    print("❌ SQLAlchemy non installé")
    sys.exit(1)

try:
    import uvicorn
    print(f"✅ Uvicorn installé")
except ImportError:
    print("❌ Uvicorn non installé")
    sys.exit(1)

print()
print("=" * 70)
print("  ✅ Tous les prérequis sont satisfaits!")
print("=" * 70)
print()

# Afficher les informations de démarrage
print("📌 Informations de démarrage:")
print(f"   Host: 0.0.0.0")
print(f"   Port: 8000")
print(f"   Reload: True (mode développement)")
print()
print("🌐 Endpoints disponibles:")
print("   - API: http://localhost:8000")
print("   - Docs (Swagger): http://localhost:8000/docs")
print("   - ReDoc: http://localhost:8000/redoc")
print("   - Health: http://localhost:8000/health")
print()
print("=" * 70)
print()

# Démarrer le serveur
try:
    print("🚀 Démarrage du serveur...")
    print()
    os.system('uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload')
except KeyboardInterrupt:
    print()
    print("👋 Serveur arrêté par l'utilisateur")
    sys.exit(0)
except Exception as e:
    print(f"❌ Erreur lors du démarrage: {e}")
    sys.exit(1)
