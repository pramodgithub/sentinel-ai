from app.workers import celery_app
from app.workers.action_tasks import execute_action
from app.workers.decision_tasks import decision_task
from app.workers.evaluation_tasks import evaluate_execution
\
from app.workers.shared_tasks import finalize_execution
from celery import chord, group, chain

@celery_app.task(bind=True, name="recovery_task")
def recovery_task(self, decision_result):
    from app.workers.planner_tasks import planner_task
    if decision_result["decision"] != "retry":
        return decision_result

    print("[RECOVERY] Retrying failed steps...")

    failed_steps = decision_result.get("failed_steps", [])
    state_dict = decision_result["state_dict"]

    retry_sigs = []
    for step in state_dict["plan"]["nodes"]:
        if step["id"] in failed_steps:
            retry_sigs.append(
                execute_action.si(
                    step,
                    decision_result["execution_id"],
                    decision_result["incident_id"],
                    state_dict
                )
            )

    return chord(
        group(retry_sigs),
        chain(
            finalize_execution.s(
                execution_id=decision_result["execution_id"],
                incident_id=decision_result["incident_id"]
            ),
            evaluate_execution.s(
                execution_id=decision_result["execution_id"],
                incident_id=decision_result["incident_id"],
                state_dict=decision_result["state_dict"]
            ),
            decision_task.s(),     # 👈 LOOP BACK
            recovery_task.s(),     # 👈 continue retry if needed
            planner_task.s()       # 👈 fallback if decision changes
        )
    ).apply_async()