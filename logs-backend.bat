@echo off
echo Redemarrage du backend...
docker-compose restart backend
timeout /t 3 /nobreak > nul
echo.
echo Logs backend:
docker logs --tail 50 -f ping61-backend
