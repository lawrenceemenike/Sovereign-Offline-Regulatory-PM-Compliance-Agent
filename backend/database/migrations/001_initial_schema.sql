-- ====================================================================
-- LexGuard: Sovereign Compliance Agent - PostgreSQL Migration
-- Migration: 001_initial_schema.sql
-- Organization: Brendan Nicholas Holdings (BNH)
-- ====================================================================

-- 1. Create Custom Enum Types
DO $$ BEGIN
    CREATE TYPE compliance_status_enum AS ENUM (
        'Compliant',
        'Review Required',
        'Non-Compliant Violation'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 2. Create Subsidiary Pillars Table
CREATE TABLE IF NOT EXISTS subsidiary_pillars (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    vertical VARCHAR(64) NOT NULL,
    head_of_compliance VARCHAR(255) NOT NULL,
    operational_jurisdiction VARCHAR(255) DEFAULT 'Federal Republic of Nigeria',
    current_risk_rating VARCHAR(32) DEFAULT 'Low',
    last_audit_date TIMESTAMP WITHOUT TIME ZONE
);

-- 3. Create Milestone Audits Table
CREATE TABLE IF NOT EXISTS milestone_audits (
    id SERIAL PRIMARY KEY,
    subsidiary_id VARCHAR(64) NOT NULL,
    subsidiary_vertical VARCHAR(64) NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    submitted_text TEXT NOT NULL,
    risk_score DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    compliance_status compliance_status_enum NOT NULL DEFAULT 'Review Required',
    raw_ai_response JSONB NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create indexes for executive query velocity
CREATE INDEX IF NOT EXISTS idx_milestone_audits_sub_id ON milestone_audits (subsidiary_id);
CREATE INDEX IF NOT EXISTS idx_milestone_audits_vertical ON milestone_audits (subsidiary_vertical);
CREATE INDEX IF NOT EXISTS idx_milestone_audits_status ON milestone_audits (compliance_status);
CREATE INDEX IF NOT EXISTS idx_milestone_audits_created ON milestone_audits (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_milestone_audits_gin_ai ON milestone_audits USING GIN (raw_ai_response);

-- 4. Create Regulatory Docs Metadata Table
CREATE TABLE IF NOT EXISTS regulatory_docs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(64) NOT NULL,
    chunk_count INTEGER NOT NULL DEFAULT 0,
    source_filename VARCHAR(255),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_reg_docs_category ON regulatory_docs (category);

-- 5. Seed Initial Institutional Subsidiaries for Brendan Nicholas Holdings
INSERT INTO subsidiary_pillars (id, name, vertical, head_of_compliance, current_risk_rating)
VALUES 
    ('BNH-ENG-01', 'BNH Energy & Midstream', 'Energy', 'Engr. Aliyu Bello', 'Moderate'),
    ('BNH-PROP-02', 'BNH Property & Real Estate Holdings', 'Property', 'Barr. Chidinma Okafor', 'Low'),
    ('BNH-TECH-03', 'BNH GovTech & Sovereign Cloud', 'GovTech', 'Dr. Femi Adeleke', 'High'),
    ('BNH-AGRI-04', 'BNH Agribusiness & Food Security', 'Agribusiness', 'Hajiya Zainab Usman', 'Low'),
    ('BNH-CAP-05', 'BNH Capital & Infrastructure Projects', 'Infrastructure', 'Tariq Al-Mansoor', 'Low')
ON CONFLICT (id) DO NOTHING;
