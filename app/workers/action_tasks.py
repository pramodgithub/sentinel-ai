from app.mcp.client import call_mcp_tool
from app.workers.celery_app import celery_app
from app.tools.tool_registry import ToolRegistry
from app.services.audit_service import AuditService
from app.core.state import ExecutionState
from app.core.shared_store import append_execution_result, append_live_result, append_thinking_trace, save_execution_state, generate_decision_summary
import asyncio
import time

registry = ToolRegistry()
audit = AuditService()


@celery_app.task(name="execute_action", bind=True)
def execute_action(self, step, execution_id, incident_id, state_dict):

    state = ExecutionState.from_dict(state_dict)

    tool = registry.get_tool(step)

    if not tool:
        result = {"step": step, "status": "invalid_tool"}
        append_execution_result(execution_id, result)
        return result

    try:
        audit.log(
            execution_id,
            incident_id,
            "ExecutorAgent",
            step,
            "started"
        )

        # Prefer MCP-backed execution for selected tools.

        try:

            start_time = time.time()
            payload = build_mcp_payload(step, state)
            result = asyncio.run(
                call_mcp_tool(
                    tool_name=step,
                    payload=payload,
                    retries=3,
                    timeout=10
                )
            )

            latency_ms = round((time.time() - start_time) * 1000, 2)

            final_result = {
                "step": step,
                "source": "mcp",
                "status": result["status"],
                "latency_ms": latency_ms,
                "result": result
            }

            state.intermediate_results[step] = final_result

        except Exception as e:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            final_result = {
                "step": step,
                "source": "executor",
                "status": "failed",
                "latency_ms": latency_ms,
                "error": str(e)
            }

            state.intermediate_results[step] = final_result

        # result available for DB save / append_execution_result()

        result = state.intermediate_results[step]

        #    state = tool.execute(state, step)
        #    result = state.intermediate_results.get(step)

        append_thinking_trace(execution_id, {
            "agent": "tool",
            "step": step,
            "phase": "end",
            "input": "metrics/logs/system state",
            "decision": generate_decision_summary(step, result),
            "output": result
        })

        final_result = {
            "step": step,
            "status": "completed",
            "result": result
        }

    # ✅ Persist result
        append_execution_result(execution_id, final_result)

        save_execution_state(execution_id, state.to_dict())

        append_live_result(execution_id, step, result)

        audit.log(
            execution_id,
            incident_id,
            "ExecutorAgent",
            step,
            "completed",
            result
        )

        print(f"[EXECUTE] step={step}")

        return final_result

    except Exception as e:

        error_result = {
            "step": step,
            "status": "failed",
            "error": str(e)
        }

        # ✅ Persist failure
        append_execution_result(execution_id, error_result)

        audit.log(
            execution_id,
            incident_id,
            "ExecutorAgent",
            step,
            "failed",
            str(e)
        )

        return error_result


# ---------------------------------------------------

# Build payload dynamically per tool

# ---------------------------------------------------

def build_mcp_payload(step, state):

    service = state.incident.get("service", "unknown-service")
    incident_id = state.incident.get("id", "unknown-incident")
    severity = state.incident.get("severity", "high")

    if step == "check_logs":
        return {
            "step": step,
            "service": service
        }

    elif step == "alert_human":
        return {
            "step": step,
            "severity": severity
        }

    elif step == "check_health_endpoint":
        service_url = f"http://{service}/health"
        return {
            "step": step,
            "service_url": service_url
        }

    elif step == "clear_cache":
        return {
            "step": step,
            "cache_type": "default"
        }

    elif step == "close_incident":
        return {
            "step": step,
            "incident_id": incident_id
        }

    elif step == "inspect_metrics":
        return {
            "step": step,
            "service": service
        }

    elif step == "monitor_service":
        return {
            "step": step,
            "service": service
        }

    elif step == "restart_container":
        return {
            "step": step,
            "container_id": service
        }

    elif step == "rollback_deployment":
        return {
            "step": step,
            "deployment_id": service
        }

    elif step == "scale_service":
        return {
            "step": step,
            "service": service,
            "direction": "up"
        }

    else:
        return {
            "step": step,
            "service": service
        }
