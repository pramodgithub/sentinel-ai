CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE incidents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service TEXT,
    description TEXT,
    severity TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    execution_id TEXT,
    incident_id TEXT,
    agent TEXT,
    step TEXT,
    status TEXT,
    payload JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE incident_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_text TEXT,
    embedding vector(384),
    diagnosis JSONB,
    actions JSONB,
    outcome JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);