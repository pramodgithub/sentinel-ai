from app.core.shared_store import get_execution_results, get_execution_state, get_incident_execution_mapping, get_live_results, get_thinking_trace, normalize_live_results
from fastapi import APIRouter
from app.services.incident_service import IncidentService
from app.workers.incident_tasks import process_incident
from app.schemas.incident_schema import IncidentRequest
from app.core.dag import compute_levels

router = APIRouter()

incident_service = IncidentService()


@router.post("/incident")
def create_incident(payload: IncidentRequest):

    incident_id = incident_service.create_incident(payload)

    process_incident.delay(incident_id)

    return {
        "incident_id": incident_id
    }

@router.get("/execution/{execution_id}")
def get_execution(execution_id: str):
    state = get_execution_state(execution_id)
    if not state:
        return {"status": "pending", "execution_id": execution_id}
    
    results = get_execution_results(execution_id)
    state["live_results"] = results
    return state


@router.get("/execution/{execution_id}/results")
def get_execution_results_endpoint(execution_id: str):
    results = get_execution_results(execution_id)
    return {"execution_id": execution_id, "results": results}

@router.get("/incident/{incident_id}/execution")
async def get_execution_id(incident_id: str):
    execution_id = get_incident_execution_mapping(incident_id)
    if not execution_id:
        return {"status": "pending", "execution_id": None}
    return {"status": "found", "execution_id": execution_id}


@router.get("/execution/{execution_id}/levels")
async def get_levels(execution_id: str):
    state = get_execution_state(execution_id)
    if not state:
        return {"levels": []}
    plan = state.get("plan", {})
    nodes = plan.get("nodes", [])
    edges = plan.get("edges", [])
    levels = compute_levels(nodes, edges)
    return {"levels": levels}


@router.get("/execution/{execution_id}/live_results")
def get_execution(execution_id: str):

    state = get_execution_state(execution_id) or {}

    # 🔥 ALWAYS hydrate live_results from Redis list
    live_results = get_live_results(execution_id)
    live_results = normalize_live_results(live_results)

    state["live_results"] = live_results

    return state


@router.get("/execution/{execution_id}/thinking")
def get_thinking(execution_id: str):

    traces = get_thinking_trace(execution_id)

    return {"thinking": traces}