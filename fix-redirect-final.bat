@echo off
cls
echo ========================================
echo   CORRECTION FINALE REDIRECTION
echo ========================================
echo.

echo [1/3] Redemarrage backend...
docker-compose restart backend
echo.

echo [2/3] Attente de 5 secondes...
timeout /t 5 /nobreak > nul
echo.

echo [3/3] Test de l'URL de redirection...
curl -s http://localhost:8000/api/auth/login
echo.
echo.

echo ========================================
echo   CORRECTION APPLIQUEE !
echo ========================================
echo.
echo TESTEZ MAINTENANT:
echo   1. http://localhost:3000
echo   2. SE CONNECTER VIA CAS
echo   3. student1 / password123
echo   4. Redirection vers /dashboard
echo.
echo Si probleme, voir les logs:
echo   logs-backend-live.bat
echo.
pause