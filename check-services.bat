@echo off
echo ========================================
echo Verification de l'etat des services
echo ========================================
echo.

echo [1] Conteneurs en cours d'execution:
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | findstr ping61
echo.

echo [2] Test de connexion LDAP:
docker exec ping61-openldap ldapsearch -x -H ldap://localhost -b "dc=esigelec,dc=fr" -D "cn=admin,dc=esigelec,dc=fr" -w admin "(uid=student1)" 2>nul
if %errorlevel% equ 0 (
    echo    [OK] LDAP fonctionne - Utilisateur student1 trouve
) else (
    echo    [ERREUR] LDAP ne repond pas ou utilisateur non trouve
)
echo.

echo [3] Test de connexion Backend:
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo    [OK] Backend accessible sur http://localhost:8000
) else (
    echo    [ERREUR] Backend non accessible
)
echo.

echo [4] Test de connexion CAS:
curl -s http://localhost:8888/cas/login >nul 2>&1
if %errorlevel% equ 0 (
    echo    [OK] CAS accessible sur http://localhost:8888/cas
) else (
    echo    [ERREUR] CAS non accessible
)
echo.

echo [5] Test de connexion Frontend:
curl -s http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo    [OK] Frontend accessible sur http://localhost:3000
) else (
    echo    [ERREUR] Frontend non accessible
)
echo.

echo ========================================
echo Verification terminee
echo ========================================
echo.
echo Si tous les tests sont OK, vous pouvez acceder a:
echo   http://localhost:3000
echo.
echo Sinon, verifiez les logs avec:
echo   docker-compose logs [nom-du-service]
echo.
pause
