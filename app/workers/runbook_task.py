from app.agents.runbook_agent import RunbookAgent
from app.core.state import ExecutionState
from app.workers.celery_app import celery_app


@celery_app.task(name="runbook_task")
def runbook_task(state_dict):
    # preserve before state.to_dict() wipes it
    live_results = state_dict.get("live_results", [])

    state = ExecutionState.from_dict(state_dict)
    runbook = RunbookAgent()
    state = runbook.run(state)

    result = state.to_dict()
    result["live_results"] = live_results  # restore

    
    return result