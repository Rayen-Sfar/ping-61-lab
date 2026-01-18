@echo off
echo ========================================
echo Redemarrage du backend
echo ========================================
echo.

echo Arret du backend...
docker-compose stop backend
echo.

echo Demarrage du backend...
docker-compose up -d backend
echo.

echo Attente de 5 secondes...
timeout /t 5 /nobreak
echo.

echo Test de connexion...
curl -s http://localhost:8000/health
echo.

echo ========================================
echo Backend redemarre !
echo ========================================
echo.
echo Testez maintenant: http://localhost:3000
echo.
pause
