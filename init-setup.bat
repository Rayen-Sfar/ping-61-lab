@echo off
REM Script d'initialisation complète de Lab on Demand

cls
echo ================================================
echo   Lab on Demand - Initialisation Complète
echo ================================================
echo.

REM Vérifier PostgreSQL
echo 1. Vérification de PostgreSQL...
psql --version >nul 2>&1
if errorlevel 1 (
    echo ❌ PostgreSQL n'est pas installé ou non accessible
    echo   Veuillez installer PostgreSQL et l'ajouter au PATH
    pause
    exit /b 1
) else (
    echo ✅ PostgreSQL détecté
)
echo.

REM Créer la base de données
echo 2. Création de la base de données "labondemand"...
psql -U postgres -c "CREATE DATABASE labondemand;" 2>nul
if errorlevel 0 (
    echo ✅ Base de données créée (ou déjà existante)
) else (
    echo ⚠️  Impossible de créer la base (peut être déjà créée)
)
echo.

REM Installer les dépendances Python du backend
echo 3. Installation des dépendances Python du backend...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des dépendances
    pause
    exit /b 1
) else (
    echo ✅ Dépendances installées
)
cd ..
echo.

REM Initialiser la base de données avec SQLAlchemy
echo 4. Initialisation de la base de données PostgreSQL...
cd backend
python ../scripts/init_db.py
if errorlevel 1 (
    echo ⚠️  Erreur lors de l'initialisation
) else (
    echo ✅ Base de données initialisée
)
cd ..
echo.

REM Installer les dépendances frontend
echo 5. Installation des dépendances Node.js du frontend...
cd frontend
npm install
if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des dépendances npm
    pause
    exit /b 1
) else (
    echo ✅ Dépendances npm installées
)
cd ..
echo.

echo ================================================
echo ✅ Initialisation terminée avec succès!
echo ================================================
echo.
echo Prochaines étapes:
echo 1. Lancez le backend:
echo    cd backend && python main.py
echo.
echo 2. Dans un autre terminal, lancez le frontend:
echo    cd frontend && npm start
echo.
echo 3. Ouvrez votre navigateur sur:
echo    http://localhost:3000 ou http://localhost:3001
echo.
pause
