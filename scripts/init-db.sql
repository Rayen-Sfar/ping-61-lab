-- Connect to the database (assuming it exists)
\c labondemand;

-- Create guacamole schema for Guacamole if it doesn't exist
CREATE SCHEMA IF NOT EXISTS guacamole;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE labondemand TO postgres;
GRANT ALL ON SCHEMA guacamole TO postgres;
