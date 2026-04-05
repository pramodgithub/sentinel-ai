"""Pipeline orchestration for running agents in sequence."""

from typing import Dict, Any, List
from ..agents.base_agent import BaseAgent


class AgentPipeline:
    """Orchestrates execution of agents in a pipeline."""

    def __init__(self, agents: List[BaseAgent]):
        """Initialize the pipeline with agents.
        
        Args:
            agents: List of agents to execute in order
        """
        self.agents = agents

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the pipeline.
        
        Args:
            input_data: Initial input data
            
        Returns:
            Final output from the pipeline
        """
        result = input_data
        for agent in self.agents:
            result = await agent.execute(result)
        return result
