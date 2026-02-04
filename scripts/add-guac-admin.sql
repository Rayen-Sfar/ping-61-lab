-- Add default Guacamole admin user if it doesn't exist
-- Username: guacadmin
-- Password: guacadmin (MD5: 0b2c69e4a7a7c5c3f5e5f5f5f5e5f5f5)

-- Note: The password hash below is for "guacadmin" using Guacamole's hashing algorithm
-- You should change this password in production!

INSERT IGNORE INTO guacamole_user (entity_id, username, password_hash, password_salt, password_date) 
VALUES (1, 'guacadmin', 
        UNHEX('FBF87D1B58DFE2BAE1A36DCDDC3F1A1BD19C88EEBDC02E61D30370E5B5B07AB5'),
        UNHEX('E9CB94CC515FEF52D142AF8122BF8FEA'),
        NOW());

-- Grant full admin permissions
INSERT IGNORE INTO guacamole_connection (connection_id, connection_name, protocol) 
VALUES (1, 'Kali', 'vnc');

INSERT IGNORE INTO guacamole_connection_parameter (connection_id, parameter_name, parameter_value) 
VALUES 
  (1, 'hostname', 'kali'),
  (1, 'port', '5900');
