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

echo [3/5] Creation de l'enseignant teacher1...
docker exec -i ping61-openldap ldapadd -x -D "cn=admin,dc=esigelec,dc=fr" -w admin < ldap-teacher1.ldif

echo [4/5] Creation de l'utilisateur rayen (enseignant)...
docker cp ldap-rayen.ldif ping61-openldap:/tmp/ldap-rayen.ldif
docker exec -i ping61-openldap ldapadd -x -D "cn=admin,dc=esigelec,dc=fr" -w admin -f /tmp/ldap-rayen.ldif

echo [5/5] Creation des groupes (teachers, students)...
docker exec -i ping61-openldap ldapadd -x -D "cn=admin,dc=esigelec,dc=fr" -w admin < ldap-groups.ldif

echo Ajout de rayen au groupe teachers...
docker cp ldap-add-rayen-to-teachers.ldif ping61-openldap:/tmp/ldap-add-rayen-to-teachers.ldif
docker exec -i ping61-openldap ldapmodify -x -D "cn=admin,dc=esigelec,dc=fr" -w admin -f /tmp/ldap-add-rayen-to-teachers.ldif

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
