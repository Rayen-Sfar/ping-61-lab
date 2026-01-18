@echo off
cls
echo ========================================
echo   AJOUTER UN NOUVEL UTILISATEUR LDAP
echo ========================================
echo.

set /p username="Nom d'utilisateur: "
set /p firstname="Prenom: "
set /p lastname="Nom de famille: "
set /p email="Email (optionnel): "
set /p password="Mot de passe: "

if "%username%"=="" (
    echo Erreur: Le nom d'utilisateur est obligatoire
    pause
    exit /b
)

if "%password%"=="" (
    echo Erreur: Le mot de passe est obligatoire
    pause
    exit /b
)

if "%email%"=="" set email=%username%@esigelec.fr
if "%firstname%"=="" set firstname=%username%
if "%lastname%"=="" set lastname=User

echo.
echo Creation de l'utilisateur %username%...

docker exec ping61-openldap ldapadd -x -D "cn=admin,dc=esigelec,dc=fr" -w admin << EOF
dn: uid=%username%,ou=users,dc=esigelec,dc=fr
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: %username%
cn: %firstname% %lastname%
sn: %lastname%
givenName: %firstname%
mail: %email%
uidNumber: 1000%RANDOM:~-2%
gidNumber: 1000%RANDOM:~-2%
homeDirectory: /home/%username%
userPassword: %password%
EOF

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   UTILISATEUR CREE AVEC SUCCES !
    echo ========================================
    echo.
    echo Identifiant: %username%
    echo Mot de passe: %password%
    echo Email: %email%
    echo.
    echo Vous pouvez maintenant vous connecter avec ces identifiants sur:
    echo   http://localhost:3000
    echo.
) else (
    echo.
    echo Erreur lors de la creation de l'utilisateur.
    echo Verifiez que l'utilisateur n'existe pas deja.
)

pause