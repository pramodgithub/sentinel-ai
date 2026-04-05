"""Tests for the planner agent."""

import pytest
from app.agents.planner_agent import PlannerAgent


@pytest.fixture
def planner_agent():
    """Create a planner agent for testing."""
    return PlannerAgent(name="test_planner")


@pytest.mark.asyncio
async def test_planner_agent_execution(planner_agent):
    """Test planner agent execution."""
    input_data = {
        "diagnosis": "Root cause identified",
        "incident_id": "INC-001",
        "available_tools": ["restart_container", "check_logs"]
    }

    result = await planner_agent.execute(input_data)
    assert result is not None
    assert "plan" in result or "actions" in result


@pytest.mark.asyncio
async def test_planner_agent_with_empty_input(planner_agent):
    """Test planner agent with empty input."""
    result = await planner_agent.execute({})
    assert result is not None
