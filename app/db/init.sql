CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE incidents (
    id UUID PRIMARY KEY,
    title TEXT,
    description TEXT,
    severity VARCHAR(20),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE workflows (
    id UUID PRIMARY KEY,
    incident_id UUID,
    state VARCHAR(50),
    current_step INT,
    retries INT DEFAULT 0,
    started_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE workflow_steps (
    id UUID PRIMARY KEY,
    workflow_id UUID,
    step_number INT,
    action VARCHAR(100),
    status VARCHAR(50)
);

CREATE TABLE incident_memory (
    id UUID PRIMARY KEY,
    incident_id UUID,
    summary TEXT,
    embedding VECTOR(1536)
);

CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    document_id TEXT,
    chunk TEXT,
    embedding VECTOR(384),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);