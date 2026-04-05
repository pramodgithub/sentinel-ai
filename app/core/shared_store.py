#import traceback

from app.workers.celery_app import celery_app
from app.core.config import settings
import redis
import json

redis_client = redis.Redis.from_url(settings.REDIS_URL)

def save_incident_execution_mapping(incident_id: str, execution_id: str):
    key = f"sentinel:incident:{incident_id}:execution_id"
    redis_client.set(key, execution_id, ex=3600)

def get_incident_execution_mapping(incident_id: str) -> str | None:
    key = f"sentinel:incident:{incident_id}:execution_id"
    value = redis_client.get(key)
    return value.decode() if value else None

def append_execution_result(execution_id, result):
    key = f"sentinel:execution:{execution_id}:results"
    redis_client.rpush(key, json.dumps(result))


def get_execution_results(execution_id):
    key = f"sentinel:execution:{execution_id}:results"
    results = redis_client.lrange(key, 0, -1)
    return [json.loads(r) for r in results]


def clear_execution_results(execution_id):
    key = f"sentinel:execution:{execution_id}:results"
    redis_client.delete(key)

def save_execution_state(execution_id: str, state_dict: dict):
    key = f"sentinel:execution:{execution_id}:state"

    # 🔥 ALWAYS OVERRIDE live_results FROM REDIS
    live_results = get_live_results(execution_id)

    state_dict["live_results"] = live_results

    redis_client.set(key, json.dumps(state_dict), ex=3600)


def get_execution_state(execution_id: str):
    key = f"sentinel:execution:{execution_id}:state"
    data = redis_client.get(key)
    
    state = json.loads(data) if data else {}

    # 🔥 Inject live results dynamically
    state["live_results"] = get_live_results(execution_id)

    return state


def push_execution_result(execution_id: str, step: str, result: dict):
    key = f"sentinel:execution:{execution_id}:results"
    redis_client.rpush(key, json.dumps({
        "step": step,
        "result": result
    }))

def append_live_result(execution_id: str, step_name: str, output):

    key = f"sentinel:execution:{execution_id}:live_results"

    event = {
        "step": step_name,
        "status": "completed",
        "result": output
    }

    redis_client.rpush(key, json.dumps(event))


def get_live_results(execution_id: str):
    key = f"sentinel:execution:{execution_id}:live_results"
    results = redis_client.lrange(key, 0, -1)
    return [json.loads(r) for r in results]


def append_thinking_trace(execution_id: str, trace: dict):
    key = f"sentinel:execution:{execution_id}:thinking"

    redis_client.rpush(key, json.dumps(trace))


def get_thinking_trace(execution_id: str):
    key = f"sentinel:execution:{execution_id}:thinking"
    results = redis_client.lrange(key, 0, -1)

    return [json.loads(r) for r in results]

def normalize_live_results(results):

    cleaned = []

    for item in results:

        # already correct
        if isinstance(item, dict) and "step" in item:
            cleaned.append(item)
            continue

        # dict but missing structure
        if isinstance(item, dict):
            cleaned.append({
                "step": "unknown_step",
                "status": item.get("status", "completed"),
                "result": item
            })
            continue

        # string fallback
        cleaned.append({
            "step": "unknown_step",
            "status": "completed",
            "result": item
        })

    return cleaned


def generate_decision_summary(step_name, result):

    if step_name == "inspect_metrics":
        cpu = result.get("cpu", 0)
        if cpu > 90:
            return f"High CPU detected ({cpu}%), indicates system stress"
        return "Metrics within acceptable range"

    elif step_name == "check_logs":
        if isinstance(result, str) and "No critical errors" in result:
            return "Logs show no critical errors"
        return "Logs indicate potential issues"

    elif step_name == "restart_container":
        if result.get("status") == "success":
            return "Container restarted successfully to recover system"
        return "Restart failed"

    elif step_name == "monitor_service":
        if result.get("healthy"):
            return "System stabilized after intervention"
        return "System still unstable"

    return "Step executed"
