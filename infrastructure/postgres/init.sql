-- PostgreSQL Initialization Script
-- Create extensions and initial setup

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pg_trgm for text search
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create eduproof database if not exists
SELECT 'CREATE DATABASE eduproof'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'eduproof')\gexec

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE eduproof TO eduproof;

-- Log initialization
DO $$
BEGIN
  RAISE NOTICE 'EduProof database initialized successfully';
END $$;
