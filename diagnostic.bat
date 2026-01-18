@echo off
echo ========================================
echo DIAGNOSTIC COMPLET
echo ========================================
echo.

echo [1] Etat des conteneurs:
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | findstr ping61
echo.

echo [2] Logs CAS (dernieres 20 lignes):
docker logs --tail 20 ping61-cas 2>&1
echo.

echo [3] Test port 8888:
netstat -ano | findstr :8888
echo.

echo [4] Test connexion CAS:
curl -I http://localhost:8888/cas/login 2>&1
echo.

pause
