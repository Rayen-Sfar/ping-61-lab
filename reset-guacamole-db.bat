@echo off
cls
echo ========================================
echo   RESET COMPLET GUACAMOLE + DB
echo ========================================
echo.
echo ATTENTION: Ceci va supprimer toutes les donnees Guacamole !
echo.
set /p confirm="Continuer ? (y/N): "
if /i not "%confirm%"=="y" (
    echo Operation annulee.
    pause
    exit /b
)
echo.

echo [1/6] Arret des services...
docker-compose stop guacamole mysql
echo.

echo [2/6] Suppression des conteneurs...
docker rm ping61-guacamole ping61-mysql
echo.

echo [3/6] Suppression du volume MySQL...
docker volume rm ping61-lab_mysql_data
echo.

echo [4/6] Redemarrage MySQL...
docker-compose up -d mysql
echo.

echo [5/6] Attente MySQL (20 secondes)...
timeout /t 20 /nobreak > nul
echo.

echo [6/6] Demarrage Guacamole...
docker-compose up -d guacamole
echo.

echo Attente de l'initialisation (45 secondes)...
timeout /t 45 /nobreak > nul
echo.

echo ========================================
echo   RESET COMPLET TERMINE !
echo ========================================
echo.
echo Base de donnees Guacamole reinitialisee.
echo.
echo Testez maintenant:
echo   URL: http://localhost:8088/guacamole/
echo   Username: guacadmin
echo   Password: guacadmin
echo.
pause