from sqlalchemy import text
from app.storage.db import engine
import json

class AuditService:

    def log(self, execution_id, incident_id, agent, step, status, payload=None):

        query = text("""
        INSERT INTO audit_logs (
            execution_id,
            incident_id,
            agent,
            step,
            status,
            payload
        )
        VALUES (
            :execution_id,
            :incident_id,
            :agent,
            :step,
            :status,
            :payload
        )
        """)

        with engine.begin() as conn:
            conn.execute(query, {
                "execution_id": execution_id,
                "incident_id": incident_id,
                "agent": agent,
                "step": step,
                "status": status,
                "payload": json.dumps(payload) if payload else None
            })