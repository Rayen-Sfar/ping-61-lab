@echo off
cls
echo ========================================
echo   UTILISATEURS LDAP DISPONIBLES
echo ========================================
echo.

echo Recherche des utilisateurs dans LDAP...
echo.

docker exec ping61-openldap ldapsearch -x -H ldap://localhost -b "dc=esigelec,dc=fr" -D "cn=admin,dc=esigelec,dc=fr" -w admin "(objectClass=inetOrgPerson)" uid cn mail

echo.
echo ========================================
echo   TOUS CES UTILISATEURS FONCTIONNENT
echo ========================================
echo.
echo Vous pouvez vous connecter avec:
echo   - Tous les utilisateurs listes ci-dessus
echo   - Mot de passe: password123 (pour les comptes de test)
echo.
echo Pour ajouter de nouveaux utilisateurs:
echo   - Interface web: http://localhost:8081
echo   - Ou modifiez: scripts/create-ldap-users.bat
echo.
pause