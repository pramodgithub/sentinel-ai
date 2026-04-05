from app.workers.celery_app import celery_app
from app.tools.tool_registry import ToolRegistry
from app.services.audit_service import AuditService
from app.core.state import ExecutionState
from app.core.shared_store import append_execution_result, append_live_result, append_thinking_trace, save_execution_state, generate_decision_summary

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
        
        state = tool.execute(state, step)

        result = state.intermediate_results.get(step)

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