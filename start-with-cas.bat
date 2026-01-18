@echo off
echo ========================================
echo Lab on Demand - Demarrage complet
echo ========================================
echo.

echo [1/4] Arret des conteneurs existants...
docker-compose down
echo.

echo [2/4] Demarrage des services...
docker-compose up -d
echo.

echo [3/4] Attente du demarrage (30 secondes)...
timeout /t 30 /nobreak
echo.

echo [4/4] Creation des utilisateurs LDAP...
cd scripts
call create-ldap-users.bat
cd ..
echo.

echo ========================================
echo DEMARRAGE TERMINE !
echo ========================================
echo.
echo Services disponibles:
echo   - Application:    http://localhost:3000
echo   - Backend API:    http://localhost:8000
echo   - CAS Server:     http://localhost:8888/cas
echo   - LDAP Manager:   http://localhost:8081
echo   - Guacamole:      http://localhost:8088
echo.
echo Comptes de test:
echo   - Etudiant:  student1 / password123
echo   - Enseignant: teacher1 / password123
echo.
echo Pour voir les logs: docker-compose logs -f
echo Pour arreter: docker-compose down
echo.
pause
