import json
from sqlalchemy import text
from app.storage.db import SessionLocal
from app.services.embedding_service import EmbeddingService

embedding_service = EmbeddingService()


class MemoryService:

    def search_similar_incidents(self, incident_text, limit=3):

        db = SessionLocal()

        try:

            embedding = embedding_service.embed(incident_text)

            result = db.execute(
                text("""
                SELECT
                    incident_text,
                    diagnosis,
                    actions,
                    results,
                    outcome,
                    embedding <-> CAST(:embedding AS vector) AS distance
                FROM incident_memory
                ORDER BY embedding <-> CAST(:embedding AS vector)
                LIMIT :limit
                """),
                {
                    "embedding": str(embedding),
                    "limit": limit
                }
            )

            memories = []

            for row in result:
                memories.append({
                    "incident":  row[0],
                    "diagnosis": row[1],
                    "actions":   row[2],
                    "results":   row[3],
                    "outcome":   row[4],
                    "distance":  row[5],
                })

            return memories

        finally:
            db.close()


    def store_incident_memory(self, incident, diagnosis, actions, results, outcome):

        db = SessionLocal()

        try:

            embedding = embedding_service.embed(
                incident["description"]
            )

            embedding_str = str(embedding)

            db.execute(
                text("""
                INSERT INTO incident_memory
                (
                    incident_text,
                    embedding,
                    diagnosis,
                    actions,
                    results,
                    outcome
                )
                VALUES
                (
                    :incident_text,
                    CAST(:embedding AS vector),
                    :diagnosis,
                    :actions,
                    :results,
                    :outcome
                )
                """),
                {
                    "incident_text": incident["description"],
                    "embedding": embedding_str,
                    "diagnosis": json.dumps(diagnosis),
                    "actions": json.dumps(actions),
                    "results": json.dumps(results) if results is not None else None,
                    "outcome": json.dumps(outcome)
                }
            )

            db.commit()

        finally:
            db.close()

