@echo off
echo ========================================
echo Creation des utilisateurs LDAP
echo ========================================
echo.

timeout /t 5 /nobreak > nul

echo [1/3] Creation de l'unite organisationnelle...
docker exec -i ping61-openldap ldapadd -x -D "cn=admin,dc=esigelec,dc=fr" -w admin < ldap-ou.ldif

echo [2/3] Creation de l'etudiant student1...
docker exec -i ping61-openldap ldapadd -x -D "cn=admin,dc=esigelec,dc=fr" -w admin < ldap-student1.ldif

echo [3/3] Creation de l'enseignant teacher1...
docker exec -i ping61-openldap ldapadd -x -D "cn=admin,dc=esigelec,dc=fr" -w admin < ldap-teacher1.ldif

echo.
echo ========================================
echo SUCCES - Utilisateurs crees !
echo ========================================
echo.
echo Comptes disponibles:
echo   - Etudiant: student1 / password123
echo   - Enseignant: teacher1 / password123
echo.
echo Interfaces web:
echo   - Application: http://localhost:3000
echo   - CAS Server: http://localhost:8888/cas
echo   - LDAP Manager: http://localhost:8081
echo.
pause
