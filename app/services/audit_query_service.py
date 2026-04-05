from sqlalchemy import text
from app.storage.db import engine


class AuditQueryService:

    def get_incident_timeline(self, incident_id):

        query = text("""
        SELECT
            agent,
            step,
            status,
            created_at
        FROM audit_logs
        WHERE incident_id = :incident_id
        ORDER BY created_at
        """)

        with engine.begin() as conn:

            rows = conn.execute(query, {"incident_id": incident_id}).fetchall()

            timeline = []

            for r in rows:
                timeline.append({
                    "agent": r.agent,
                    "step": r.step,
                    "status": r.status,
                    "timestamp": str(r.created_at)
                })

        return timeline