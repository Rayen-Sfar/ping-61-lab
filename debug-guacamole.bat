@echo off
cls
echo ========================================
echo   DIAGNOSTIC GUACAMOLE
echo ========================================
echo.

echo [1] Etat des conteneurs Guacamole:
docker ps | findstr guac
echo.

echo [2] Test URL racine (404 attendu):
curl -I http://localhost:8088/
echo.

echo [3] Test URL correcte Guacamole:
curl -I http://localhost:8088/guacamole/
echo.

echo [4] Logs Guacamole:
docker logs --tail 10 ping61-guacamole
echo.

echo [5] Logs MySQL:
docker logs --tail 5 ping61-mysql
echo.

echo ========================================
echo   DIAGNOSTIC TERMINE
echo ========================================
echo.
echo URL correcte: http://localhost:8088/guacamole/
echo Credentials par defaut: guacadmin / guacadmin
echo.
pause