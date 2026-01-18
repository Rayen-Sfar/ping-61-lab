@echo off
cls
echo ========================================
echo   CORRECTION CORS + JWT
echo ========================================
echo.

echo [1/3] Redemarrage du backend...
docker-compose restart backend
echo.

echo [2/3] Attente de 5 secondes...
timeout /t 5 /nobreak > nul
echo.

echo [3/3] Test de connexion...
curl -s http://localhost:8000/health
echo.
echo.

echo ========================================
echo   TERMINE !
echo ========================================
echo.
echo Testez maintenant:
echo   1. Allez sur http://localhost:3000
echo   2. Cliquez "SE CONNECTER VIA CAS"
echo   3. Connectez-vous avec student1 / password123
echo.
echo Si erreur, voir les logs:
echo   docker logs ping61-backend
echo.
pause
