from app.agents.memory_agent import MemoryAgent
from app.core.state import ExecutionState
from app.workers.celery_app import celery_app


@celery_app.task(name="memory_store_task")
def memory_store_task(state_dict):

    state = ExecutionState.from_dict(state_dict)

    memory = MemoryAgent()

    state = memory.store(state)

    return state.to_dict()