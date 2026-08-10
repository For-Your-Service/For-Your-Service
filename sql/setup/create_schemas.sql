-- Create Unity Catalog schemas for For Your Service
-- Run this first to set up the database structure

-- Create catalog (if doesn't exist)
CREATE CATALOG IF NOT EXISTS veteran_intake
  COMMENT 'For Your Service - Veteran job matching platform';

-- Create Bronze layer schema
CREATE SCHEMA IF NOT EXISTS veteran_intake.bronze
  COMMENT 'Raw data from API ingestion';

-- Create Silver layer schema
CREATE SCHEMA IF NOT EXISTS veteran_intake.silver
  COMMENT 'Cleaned and deduplicated data';

-- Create Gold layer schema
CREATE SCHEMA IF NOT EXISTS veteran_intake.gold
  COMMENT 'Business-level aggregations and match results';

-- Set catalog
USE CATALOG veteran_intake;

SHOW SCHEMAS;
