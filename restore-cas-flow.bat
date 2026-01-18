@echo off
cls
echo ========================================
echo   RESTAURATION FLUX CAS CLASSIQUE
echo ========================================
echo.

echo [1/2] Redemarrage du frontend...
docker-compose restart frontend
echo.

echo [2/2] Attente de 5 secondes...
timeout /t 5 /nobreak > nul
echo.

echo ========================================
echo   FLUX CAS RESTAURE !
echo ========================================
echo.
echo NOUVEAU FLUX (classique CAS):
echo   1. Allez sur http://localhost:3000
echo   2. Cliquez \"SE CONNECTER VIA CAS\"
echo   3. Redirection vers http://localhost:8888/cas/login
echo   4. Entrez student1 / password123 sur la page CAS
echo   5. CAS renvoie un ticket vers DAP
echo   6. DAP verifie le ticket aupres de CAS
echo   7. Si valide → utilisateur connecte dans DAP
echo.
echo Page CAS externe: http://localhost:8888/cas/login
echo.
pause