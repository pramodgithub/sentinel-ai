"""Script to seed the system with documents."""

import asyncio
from typing import List


async def seed_documents():
    """Seed the system with initial documents."""
    # TODO: Implement document seeding logic
    print("Seeding documents...")
    sample_docs = [
        {"title": "Service Architecture", "content": "..."},
        {"title": "Incident Procedures", "content": "..."},
        {"title": "Troubleshooting Guide", "content": "..."}
    ]
    
    # Process documents
    for doc in sample_docs:
        print(f"Seeding: {doc['title']}")
    
    print("Document seeding completed!")


if __name__ == "__main__":
    asyncio.run(seed_documents())
