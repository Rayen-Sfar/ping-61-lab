#!/usr/bin/env python3
"""
Script d'initialisation de la base de données PostgreSQL
Crée la connexion et les tables nécessaires pour Lab on Demand
"""

import asyncio
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

# Ajouter le chemin du backend au sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.db.database import Base
from app.db.models import User, TP
from app.core.config import settings


async def init_db():
    """Initialiser la base de données PostgreSQL"""
    
    # Vérifier si on utilise PostgreSQL
    if not settings.database_url.startswith("postgresql"):
        print("❌ Erreur: La base de données doit être PostgreSQL")
        print(f"URL actuelle: {settings.database_url}")
        return False
    
    print("🔄 Connexion à PostgreSQL...")
    
    try:
        # Créer le moteur asynchrone
        if settings.database_url.startswith("postgresql://"):
            db_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
        else:
            db_url = settings.database_url
        
        engine = create_async_engine(db_url, echo=False)
        
        # Créer les tables
        print("📊 Création des tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("✅ Tables créées avec succès!")
        
        # Insérer les données initiales
        print("📝 Insertion des données initiales...")
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with async_session() as session:
            # Vérifier si des TPs existent déjà
            from sqlalchemy import select, func
            result = await session.execute(select(func.count(TP.id)))
            count = result.scalar()
            
            if count == 0:
                # Ajouter les TPs de test
                tp1 = TP(
                    title="TP 1: Introduction à Linux",
                    description="Apprendre les commandes de base Linux et la navigation",
                    instructions="""# Instructions TP 1

## Objectifs
1. Connectez-vous à la VM
2. Apprenez les commandes de base (ls, cd, pwd, mkdir, touch)
3. Créez une arborescence de fichiers

## Étapes
1. Lancez la VM Linux
2. Ouvrez un terminal
3. Explorez la structure des répertoires
4. Créez un nouveau répertoire "mon-projet"
5. Navigez dans ce répertoire
6. Créez un fichier test.txt""",
                    difficulty="Facile",
                    duration="2h",
                    created_by="Admin",
                    vm_type="Linux",
                    status="Published"
                )
                
                tp2 = TP(
                    title="TP 2: Administration Système",
                    description="Gérer les utilisateurs, les groupes et les permissions",
                    instructions="""# Instructions TP 2

## Objectifs
1. Créer et supprimer des utilisateurs
2. Gérer les groupes
3. Modifier les permissions
4. Utiliser sudo

## Étapes
1. Créez un nouvel utilisateur
2. Définissez un mot de passe
3. Créez un groupe
4. Ajoutez l'utilisateur au groupe""",
                    difficulty="Moyen",
                    duration="3h",
                    created_by="Admin",
                    vm_type="Linux",
                    status="Published"
                )
                
                tp3 = TP(
                    title="TP 3: Services Réseau",
                    description="Configurer et utiliser les services réseau essentiels",
                    instructions="""# Instructions TP 3

## Objectifs
1. Configurer un serveur Web
2. Utiliser SSH
3. Gérer les ports réseau
4. Tester les connexions

## Étapes
1. Installez Apache
2. Démarrez le service
3. Vérifiez le statut
4. Testez la connexion""",
                    difficulty="Difficile",
                    duration="4h",
                    created_by="Admin",
                    vm_type="Linux",
                    status="Published"
                )
                
                session.add_all([tp1, tp2, tp3])
                await session.commit()
                print("✅ 3 TPs de test insérés!")
            else:
                print(f"ℹ️  {count} TP(s) existant(s), pas d'insertion supplémentaire")
        
        await engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


async def main():
    """Fonction principale"""
    print("=" * 60)
    print("🚀 Initialisation de la base de données PostgreSQL")
    print("=" * 60)
    print(f"Base de données: {settings.database_url}")
    print("=" * 60)
    
    success = await init_db()
    
    print("=" * 60)
    if success:
        print("✅ Initialisation terminée avec succès!")
    else:
        print("❌ L'initialisation a échoué")
    print("=" * 60)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
