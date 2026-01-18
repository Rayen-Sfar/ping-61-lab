@echo off
cls
echo ========================================
echo   CORRECTION FINALE - CAS + Guacamole
echo ========================================
echo.

echo [1/4] Redemarrage des services...
docker-compose restart backend cas guacamole
echo.

echo [2/4] Attente de 10 secondes...
timeout /t 10 /nobreak > nul
echo.

echo [3/4] Verification...
echo.
echo Backend:
curl -s -o nul -w "  Status: %%{http_code}\n" http://localhost:8000/health
echo.
echo CAS:
curl -s -o nul -w "  Status: %%{http_code}\n" http://localhost:8888/cas/login
echo.
echo Guacamole:
curl -s -o nul -w "  Status: %%{http_code}\n" http://localhost:8088/guacamole/
echo.

echo [4/4] Logs backend (dernières 10 lignes):
docker logs --tail 10 ping61-backend
echo.

echo ========================================
echo   TERMINE !
echo ========================================
echo.
echo Test maintenant:
echo   1. http://localhost:3000
echo   2. SE CONNECTER VIA CAS
echo   3. student1 / password123
echo.
echo Guacamole: http://localhost:8088/guacamole/
echo   (Credentials par defaut: guacadmin / guacadmin)
echo.
pause
