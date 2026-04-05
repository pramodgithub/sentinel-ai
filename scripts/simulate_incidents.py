"""Script to simulate incidents for testing."""

import asyncio
import json
from typing import List, Dict, Any


async def generate_sample_incident() -> Dict[str, Any]:
    """Generate a sample incident."""
    return {
        "title": "Database Service Down",
        "description": "The primary database service is not responding to connections",
        "severity": "critical",
        "tags": ["database", "outage"],
        "logs": [
            "Connection timeout: 30s",
            "Failed to establish connection to database",
            "All queries returning timeout errors"
        ]
    }


async def simulate_incidents():
    """Simulate incidents for testing."""
    print("Simulating incidents...")
    
    # Generate sample incidents
    sample_incidents = []
    for i in range(5):
        incident = await generate_sample_incident()
        incident["id"] = f"SIM-{i+1:03d}"
        sample_incidents.append(incident)
    
    # Print incidents
    for incident in sample_incidents:
        print(json.dumps(incident, indent=2))
    
    print(f"\nGenerated {len(sample_incidents)} sample incidents")


if __name__ == "__main__":
    asyncio.run(simulate_incidents())
