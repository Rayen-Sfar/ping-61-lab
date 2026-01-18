@echo off
echo Redemarrage du backend pour appliquer les changements...
docker-compose restart backend
timeout /t 5 /nobreak > nul
echo.
echo Testez maintenant:
echo   1. http://localhost:3000
echo   2. SE CONNECTER VIA CAS
echo   3. student1 / password123
echo   4. Redirection automatique vers /dashboard
echo.
pause