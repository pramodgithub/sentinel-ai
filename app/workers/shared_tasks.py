# -------------------------------------------------------------------
# Helper tasks
# -------------------------------------------------------------------

from app.core.shared_store import clear_execution_results, get_execution_results, get_execution_state, save_execution_state
from app.workers.celery_app import celery_app
import json
from uuid import UUID


@celery_app.task(name="passthrough")
def passthrough(previous_results, current_results=None):
    """
    Accumulates results across DAG levels
    """

    if previous_results is None:
        previous_results = []

    if current_results is None:
        return previous_results

    # Normalize to list
    if not isinstance(previous_results, list):
        previous_results = [previous_results]

    if not isinstance(current_results, list):
        current_results = [current_results]

    return previous_results + current_results


@celery_app.task(bind=True, name="finalize_execution")
def finalize_execution(self, results, execution_id, incident_id):

    print(f"[FINALIZE] execution={execution_id}")

    # ✅ Fetch FULL DAG results
    final_results = get_execution_results(execution_id)

     # ✅ Save state with live_results before clearing
    existing_state = get_execution_state(execution_id) or {}
    existing_state["live_results"] = final_results
    existing_state["execution_id"] = execution_id
    existing_state["incident_id"] = incident_id
    save_execution_state(execution_id, make_serializable(existing_state))
    
    # Optional cleanup
    clear_execution_results(execution_id)

    return {
        "execution_id": execution_id,
        "incident_id": incident_id,
        "results": final_results
    }


@celery_app.task(bind=True, name="handle_failure")
def handle_failure(self, *args, execution_id=None, incident_id=None):
    # args = (request, exc, traceback) injected by Celery
    request   = args[0] if len(args) > 0 else None
    exc       = args[1] if len(args) > 1 else None
    traceback = args[2] if len(args) > 2 else None

    step_id = request.get("headers", {}).get("step_id") if isinstance(request, dict) else None

    print(f"[FAILURE] step={step_id} exc={exc}")

    return {
        "execution_id": execution_id,
        "incident_id": incident_id,
        "status": "failed",
        "failed_step_id": step_id,
        "error": str(exc)
    }

def make_serializable(obj):
    """Recursively convert non-serializable types to strings."""
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_serializable(i) for i in obj]
    return obj 

@celery_app.task(name="save_state_task")
def save_state_task(state_dict: dict) -> dict:
    execution_id = state_dict.get("execution_id")
    if execution_id:
        clean = make_serializable(state_dict)

        # live_results = intermediate_results if it's already a list
        intermediate = clean.get("intermediate_results", [])
        if isinstance(intermediate, list) and intermediate:
            clean["live_results"] = intermediate
        elif isinstance(intermediate, dict):
            # convert dict → list format for dashboard
            clean["live_results"] = [
                {"step": k, "result": v} 
                for k, v in intermediate.items()
            ]

        save_execution_state(str(execution_id), clean)
        return clean
    return state_dict


