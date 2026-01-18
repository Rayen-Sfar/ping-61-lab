@echo off
REM Script de démarrage complet Lab on Demand

cd /d "%~dp0"

cls
echo ================================================
echo   Lab on Demand - Démarrage Complet
echo ================================================
echo.

REM Vérifier que les répertoires existent
if not exist "backend" (
    echo ❌ Erreur: le répertoire 'backend' n'existe pas
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ❌ Erreur: le répertoire 'frontend' n'existe pas
    pause
    exit /b 1
)

echo 🚀 Démarrage du backend...
echo    Port: 8000
echo    Docs: http://localhost:8000/docs
echo.

REM Démarrer le backend dans une nouvelle fenêtre
start "Lab on Demand - Backend" cmd /k "cd backend && python run.py"

REM Attendre un peu que le backend démarre
timeout /t 3

echo.
echo 🚀 Démarrage du frontend...
echo    Port: 3000 ou 3001
echo    URL: http://localhost:3000
echo.

REM Démarrer le frontend dans une nouvelle fenêtre
start "Lab on Demand - Frontend" cmd /k "cd frontend && npm start"

echo.
echo ================================================
echo ✅ Application en cours de démarrage!
echo ================================================
echo.
echo 📌 Accédez à l'application:
echo    http://localhost:3000
echo.
echo 📌 Documentation API:
echo    http://localhost:8000/docs
echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause >nul
