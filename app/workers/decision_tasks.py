from app.workers.celery_app import celery_app


@celery_app.task(bind=True, name="decision_task")
def decision_task(self, eval_result):

    print("[DECISION] evaluating outcome...")

    if eval_result["resolved"]:
        return {**eval_result, "decision": "done"}

    retry_count = eval_result.get("retry_count", 0)
    error_type = eval_result.get("error_type", "unknown")

    # 🔁 retry only for transient issues
    if error_type in ["timeout", "rate_limit", "network"]:
        if retry_count < 2:
            return {**eval_result, "decision": "retry"}

    # 🧠 otherwise replan
    return {**eval_result, "decision": "replan"}