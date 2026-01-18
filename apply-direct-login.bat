@echo off
cls
echo ========================================
echo   INTEGRATION FORMULAIRE DIRECT
echo ========================================
echo.

echo [1/3] Rebuild des services...
docker-compose build --no-cache cas backend
echo.

echo [2/3] Redemarrage...
docker-compose up -d cas backend frontend
echo.

echo [3/3] Attente de 10 secondes...
timeout /t 10 /nobreak > nul
echo.

echo ========================================
echo   TERMINE !
echo ========================================
echo.
echo NOUVEAU FLUX:
echo   1. Allez sur http://localhost:3000
echo   2. Le formulaire de connexion est directement sur la page
echo   3. Entrez student1 / password123
echo   4. Cliquez SE CONNECTER
echo   5. Redirection vers le dashboard
echo.
echo Plus besoin de page CAS externe !
echo.
pause
