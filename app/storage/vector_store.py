from sqlalchemy import text
from app.db.db import engine

def insert_chunk(document_id, chunk, embedding):

    query = text("""
    INSERT INTO document_chunks (document_id, chunk, embedding)
    VALUES (:document_id, :chunk, :embedding)
    """)

    with engine.connect() as conn:
        conn.execute(
            query,
            {
                "document_id": document_id,
                "chunk": chunk,
                "embedding": embedding
            }
        )
        conn.commit()

def search_similar(query_embedding, k=5):

    vector = "[" + ",".join(map(str, query_embedding)) + "]"

    query = text("""
        SELECT document_id,
            chunk,
            embedding <-> CAST(:query_embedding AS vector) AS distance
        FROM document_chunks
        ORDER BY embedding <-> CAST(:query_embedding AS vector)
        LIMIT :k
    """)

    with engine.connect() as conn:
        results = conn.execute(
            query,
            {"query_embedding": vector, "k": k}
        )

        rows = results.fetchall()

    return [
        {
            "document_id": r[0],
            "chunk": r[1],
            "distance": float(r[2])
        }
        for r in rows
    ]