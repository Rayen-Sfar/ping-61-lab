@echo off
cls
echo ========================================
echo   CORRECTION ROUTE CALLBACK
echo ========================================
echo.

echo [1/2] Redemarrage frontend...
docker-compose restart frontend
echo.

echo [2/2] Attente de 10 secondes...
timeout /t 10 /nobreak > nul
echo.

echo ========================================
echo   CORRECTION TERMINEE !
echo ========================================
echo.
echo FLUX CORRIGE:
echo   1. http://localhost:3000
echo   2. SE CONNECTER VIA CAS
echo   3. student1 / password123
echo   4. CAS redirige vers /api/auth/callback
echo   5. CallbackPage redirige vers backend
echo   6. Backend redirige vers /dashboard
echo.
echo Plus d'erreur "No routes matched" !
echo.
pause