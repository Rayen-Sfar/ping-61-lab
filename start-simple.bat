@echo off
cls
echo ========================================
echo   Lab on Demand - Demarrage Simple
echo ========================================
echo.

echo [1/5] Arret des anciens conteneurs...
docker-compose down 2>nul
echo.

echo [2/5] Demarrage des services essentiels...
docker-compose up -d postgres openldap cas backend frontend
echo.

echo [3/5] Attente du demarrage (20 secondes)...
timeout /t 20 /nobreak > nul
echo.

echo [4/5] Creation des utilisateurs LDAP...
cd scripts
call create-ldap-users.bat
cd ..
echo.

echo [5/5] Verification...
echo.
echo Test CAS:
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:8888/cas/login
echo.
echo Test Backend:
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:8000/health
echo.

echo ========================================
echo   DEMARRAGE TERMINE !
echo ========================================
echo.
echo Acces:
echo   - Application:  http://localhost:3000
echo   - CAS Login:    http://localhost:8888/cas/login
echo   - Backend API:  http://localhost:8000
echo   - LDAP Manager: http://localhost:8081
echo.
echo Comptes:
echo   - student1 / password123
echo   - teacher1 / password123
echo.
echo Pour voir les logs: docker-compose logs -f cas
echo.
pause
