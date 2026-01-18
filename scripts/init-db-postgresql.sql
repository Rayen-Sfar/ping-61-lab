-- Script d'initialisation de la base de données PostgreSQL
-- Créer les tables pour Lab on Demand

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    cas_id VARCHAR UNIQUE,
    email VARCHAR UNIQUE,
    first_name VARCHAR,
    last_name VARCHAR,
    role VARCHAR DEFAULT 'student',
    auth_provider VARCHAR DEFAULT 'cas',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Table des TPs
CREATE TABLE IF NOT EXISTS tps (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    instructions TEXT,
    difficulty VARCHAR DEFAULT 'Moyen',
    duration VARCHAR DEFAULT '2h',
    created_by VARCHAR,
    vm_type VARCHAR,
    status VARCHAR DEFAULT 'Published',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insérer des données de test
INSERT INTO tps (title, description, instructions, difficulty, duration, created_by, vm_type, status)
VALUES 
('TP 1: Introduction à Linux', 
 'Apprendre les commandes de base Linux et la navigation dans le système de fichiers',
 '# Instructions TP 1\n\n## Objectifs\n1. Connectez-vous à la VM\n2. Apprenez les commandes de base (ls, cd, pwd, mkdir, touch)\n3. Créez une arborescence de fichiers\n4. Manipulez les permissions\n\n## Étapes\n1. Lancez la VM Linux\n2. Ouvrez un terminal\n3. Explorez la structure des répertoires\n4. Créez un nouveau répertoire "mon-projet"\n5. Naviguez dans ce répertoire\n6. Créez un fichier test.txt\n7. Affichez le contenu du répertoire avec ls -la',
 'Facile', '2h', 'Admin', 'Linux', 'Published')
ON CONFLICT DO NOTHING;

INSERT INTO tps (title, description, instructions, difficulty, duration, created_by, vm_type, status)
VALUES 
('TP 2: Administration Système', 
 'Gérer les utilisateurs, les groupes et les permissions sous Linux',
 '# Instructions TP 2\n\n## Objectifs\n1. Créer et supprimer des utilisateurs\n2. Gérer les groupes\n3. Modifier les permissions\n4. Utiliser sudo\n\n## Étapes\n1. Créez un nouvel utilisateur: sudo useradd student\n2. Définissez un mot de passe: sudo passwd student\n3. Créez un groupe: sudo groupadd developers\n4. Ajoutez l''utilisateur au groupe: sudo usermod -aG developers student\n5. Modifiez les permissions: chmod 755 mon-projet',
 'Moyen', '3h', 'Admin', 'Linux', 'Published')
ON CONFLICT DO NOTHING;

INSERT INTO tps (title, description, instructions, difficulty, duration, created_by, vm_type, status)
VALUES 
('TP 3: Services Réseau', 
 'Configurer et utiliser les services réseau essentiels',
 '# Instructions TP 3\n\n## Objectifs\n1. Configurer un serveur Web\n2. Utiliser SSH\n3. Gérer les ports réseau\n4. Tester les connexions\n\n## Étapes\n1. Installez Apache: sudo apt-get install apache2\n2. Démarrez le service: sudo systemctl start apache2\n3. Vérifiez le statut: sudo systemctl status apache2\n4. Testez la connexion: curl http://localhost\n5. Configurez le pare-feu si nécessaire',
 'Difficile', '4h', 'Admin', 'Linux', 'Published')
ON CONFLICT DO NOTHING;
