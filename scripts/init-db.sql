-- Connect to the database (assuming it exists)
\c ping61;

-- Create guacamole schema for Guacamole if it doesn't exist
CREATE SCHEMA IF NOT EXISTS guacamole;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE ping61 TO ping61;
GRANT ALL ON SCHEMA guacamole TO guac; 
