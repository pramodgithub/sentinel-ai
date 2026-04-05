from app.agents.base_agent import BaseAgent
from app.services.memory_service import MemoryService
from app.core.shared_store import append_thinking_trace

memory_service = MemoryService()


class MemoryAgent(BaseAgent):

    def retrieve(self, state):

        memories = memory_service.search_similar_incidents(
            state.incident["description"]
        )

        state.similar_incidents = memories

        return state


    def store(self, state):

        memory_service.store_incident_memory(
            incident=state.incident,
            diagnosis=state.diagnosis,
            actions=state.plan,
            results=state.intermediate_results,
            outcome=state.evaluation
        )

        append_thinking_trace(state.execution_id, {
            "agent": "memoryAgent",
            "step": "memory_store",
            "input": state.incident,
            "decision": "Store incident memory for future reference",
            "output": {"message": "Memory stored successfully"}
        })

       

        return state