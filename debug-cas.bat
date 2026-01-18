@echo off
cls
echo ========================================
echo   DIAGNOSTIC ET CORRECTION CAS
echo ========================================
echo.

echo [1] Verification des services...
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | findstr ping61
echo.

echo [2] Test CAS validation manuelle...
curl -s "http://localhost:8888/cas/validate?ticket=ST-test&service=http://localhost:3000"
echo.
echo.

echo [3] Logs backend (dernieres 20 lignes)...
docker logs --tail 20 ping61-backend
echo.

echo [4] Redemarrage backend + cas...
docker-compose restart backend cas
echo.

echo [5] Attente de 10 secondes...
timeout /t 10 /nobreak > nul
echo.

echo ========================================
echo   DIAGNOSTIC TERMINE
echo ========================================
echo.
echo Testez maintenant:
echo   1. http://localhost:3000
echo   2. SE CONNECTER VIA CAS
echo   3. student1 / password123
echo.
pause