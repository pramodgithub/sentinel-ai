from app.workers.celery_app import celery_app
from app.agents.evaluator_agent import EvaluatorAgent
from app.core.state import ExecutionState
from app.core.shared_store import append_thinking_trace, clear_execution_results, get_execution_results


@celery_app.task(name="evaluate_execution")
def evaluate_execution(results, execution_id, incident_id, state_dict):

    state = ExecutionState.from_dict(state_dict)

    state.intermediate_results = results.get("results", [])

    evaluator = EvaluatorAgent()

    state = evaluator.run(state)

    return state.to_dict()