from sqlalchemy import text
from app.storage.db import SessionLocal


class IncidentService:

    def get_incident(self, incident_id):

        db = SessionLocal()

        try:

            result = db.execute(
                text("""
                SELECT description
                FROM incidents
                WHERE id = :id
                """),
                {"id": incident_id}
            ).fetchone()

            if result is None:
                raise Exception(f"Incident {incident_id} not found")

            return {
                "description": result[0]
            }

        finally:
            db.close()


    def create_incident(self, payload):

        db = SessionLocal()

        result = db.execute(
            text("""
            INSERT INTO incidents (service, description, severity)
            VALUES (:service, :description, :severity)
            RETURNING id
            """),
            {
                "service": payload.service,
                "description": payload.description,
                "severity": payload.severity.value
            }
        )

        incident_id = result.fetchone()[0]

        db.commit()
        db.close()

        return incident_id