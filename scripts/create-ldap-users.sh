#!/bin/bash
# Script pour créer des utilisateurs dans LDAP

echo "🔧 Création des utilisateurs LDAP..."

# Attendre que LDAP soit prêt
sleep 5

# Créer l'unité organisationnelle pour les utilisateurs
docker exec ping61-openldap ldapadd -x -D "cn=admin,dc=esigelec,dc=fr" -w admin << EOF
dn: ou=users,dc=esigelec,dc=fr
objectClass: organizationalUnit
ou: users
EOF

# Créer un étudiant
docker exec ping61-openldap ldapadd -x -D "cn=admin,dc=esigelec,dc=fr" -w admin << EOF
dn: uid=student1,ou=users,dc=esigelec,dc=fr
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: student1
cn: Jean Dupont
sn: Dupont
givenName: Jean
mail: jean.dupont@esigelec.fr
uidNumber: 10001
gidNumber: 10001
homeDirectory: /home/student1
userPassword: {SSHA}password123
EOF

# Créer un enseignant
docker exec ping61-openldap ldapadd -x -D "cn=admin,dc=esigelec,dc=fr" -w admin << EOF
dn: uid=teacher1,ou=users,dc=esigelec,dc=fr
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: teacher1
cn: Marie Martin
sn: Martin
givenName: Marie
mail: marie.martin@esigelec.fr
uidNumber: 10002
gidNumber: 10002
homeDirectory: /home/teacher1
userPassword: {SSHA}password123
EOF

echo "✅ Utilisateurs LDAP créés avec succès!"
echo ""
echo "📋 Comptes disponibles:"
echo "  - Étudiant: student1 / password123"
echo "  - Enseignant: teacher1 / password123"
echo ""
echo "🌐 Accès LDAP Account Manager: http://localhost:8081"
echo "   Login: cn=admin,dc=esigelec,dc=fr"
echo "   Password: admin"
