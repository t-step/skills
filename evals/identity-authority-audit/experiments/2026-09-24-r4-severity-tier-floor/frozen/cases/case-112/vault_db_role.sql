-- Vault database secrets engine role definition for
-- "reporting-service-creds". This is the SQL Vault runs, with the
-- generated username substituted in, every time it mints a new lease for
-- this service.

CREATE ROLE "{{name}}" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO "{{name}}";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA analytics TO "{{name}}";

-- The reporting service's own code (see db_connection.py, and every
-- caller of get_connection() elsewhere in this service) only ever issues
-- SELECT queries against this schema -- it has no INSERT, UPDATE, DELETE,
-- or DDL statement anywhere in its source.
