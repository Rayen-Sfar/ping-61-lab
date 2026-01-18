@echo off
cls
echo ========================================
echo   CORRECTION FINALE CAS
echo ========================================
echo.

echo [1/3] Redemarrage backend...
docker-compose restart backend
echo.

echo [2/3] Attente de 5 secondes...
timeout /t 5 /nobreak > nul
echo.

echo [3/3] Test de l'URL de redirection...
curl -s http://localhost:8000/api/auth/login
echo.
echo.

echo ========================================
echo   CORRECTION APPLIQUEE !
echo ========================================
echo.
echo FLUX CORRIGE:
echo   1. http://localhost:3000
echo   2. Clic "SE CONNECTER VIA CAS"
echo   3. Redirection vers CAS avec callback correct
echo   4. student1 / password123
echo   5. Validation du ticket
echo   6. Connexion reussie
echo.
echo Testez maintenant !
echo.
pause