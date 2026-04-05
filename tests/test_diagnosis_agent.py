"""Tests for the diagnosis agent."""

import pytest
from app.agents.diagnosis_agent import DiagnosisAgent


@pytest.fixture
def diagnosis_agent():
    """Create a diagnosis agent for testing."""
    return DiagnosisAgent(name="test_diagnosis")


@pytest.mark.asyncio
async def test_diagnosis_agent_execution(diagnosis_agent):
    """Test diagnosis agent execution."""
    input_data = {
        "incident_description": "Service is down",
        "logs": ["Error: Connection refused"],
        "metrics": {"cpu": 95, "memory": 88}
    }

    result = await diagnosis_agent.execute(input_data)
    assert result is not None
    assert "diagnosis" in result


@pytest.mark.asyncio
async def test_diagnosis_agent_with_empty_input(diagnosis_agent):
    """Test diagnosis agent with empty input."""
    result = await diagnosis_agent.execute({})
    assert result is not None
