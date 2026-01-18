@echo off
cls
echo ========================================
echo   REINITIALISATION GUACAMOLE
echo ========================================
echo.

echo [1/5] Arret de Guacamole...
docker-compose stop guacamole
echo.

echo [2/5] Suppression du conteneur...
docker rm ping61-guacamole
echo.

echo [3/5] Redemarrage MySQL...
docker-compose restart mysql
echo.

echo [4/5] Attente MySQL (10 secondes)...
timeout /t 10 /nobreak > nul
echo.

echo [5/5] Redemarrage Guacamole...
docker-compose up -d guacamole
echo.

echo Attente de 30 secondes pour l'initialisation...
timeout /t 30 /nobreak > nul
echo.

echo ========================================
echo   REINITIALISATION TERMINEE !
echo ========================================
echo.
echo Testez maintenant:
echo   URL: http://localhost:8088/guacamole/
echo   Username: guacadmin
echo   Password: guacadmin
echo.
echo Si probleme persiste:
echo   - Attendez 5 minutes (blocage temporaire)
echo   - Ou utilisez: reset-guacamole-db.bat
echo.
pause