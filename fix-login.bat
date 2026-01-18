@echo off
echo Redemarrage du backend...
docker-compose restart backend
timeout /t 5 /nobreak > nul
echo.
echo Teste maintenant: http://localhost:3000
echo Identifiants: student1 / password123
pause
