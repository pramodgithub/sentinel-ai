from app.workers import celery_app
from app.agents.planner_agent import PlannerAgent

from app.core.state import ExecutionState
from app.services.memory_service import MemoryService

@celery_app.task(bind=True, name="planner_task")
def planner_task(self, decision_result):

    if decision_result["decision"] != "replan":
        return decision_result

    print("[PLANNER] generating new plan...")

    new_plan = generate_new_plan(decision_result)

    state = rebuild_state_with_new_plan(decision_result, new_plan)

    from app.agents.executor_agent import ExecutorAgent
    ExecutorAgent().run(state)

    return {"status": "replanned"}


def generate_new_plan(eval_result):

    state = eval_result["state_dict"]

    planner_input = {
        "goal": state.get("goal"),
        "current_plan": state.get("plan"),
        "failed_steps": eval_result.get("failed_steps"),
        "errors": eval_result.get("errors"),
        "execution_history": state.get("history", [])
    }


    planner = PlannerAgent()
    new_state = planner.run(planner_input)

    return new_state.plan   # nodes + edges


def rebuild_state_with_new_plan(eval_result, new_plan):

    
    old = eval_result["state_dict"]

    memory_service = MemoryService()

    # ---------------------------------------------------
    # 🔍 1. Build query from current failure
    # ---------------------------------------------------
    failed_steps = eval_result.get("failed_steps", [])
    errors = eval_result.get("errors", [])

    incident_text = f"""
    Failed steps: {failed_steps}
    Errors: {errors}
    Goal: {old.get("goal")}
    """

    # ---------------------------------------------------
    # 🧠 2. Retrieve similar incidents
    # ---------------------------------------------------
    similar_incidents = memory_service.search_similar_incidents(
        incident_text,
        limit=3
    )

    # ---------------------------------------------------
    # 🧩 3. Normalize memory into usable format
    # ---------------------------------------------------
    retrieved_memory = []

    for row in similar_incidents:
        retrieved_memory.append({
            "incident": row["incident_text"],
            "diagnosis": row["diagnosis"],
            "actions": row["actions"],
            "results": row["results"],
            "outcome": row["outcome"],
            "distance": row.get("distance")
        })

    # ---------------------------------------------------
    # 🔗 4. Merge memory safely
    # ---------------------------------------------------
    existing_memory = old.get("memory", {})

    merged_memory = {
        **existing_memory,
        "retrieved_incidents": retrieved_memory,
        "last_failure": {
            "failed_steps": failed_steps,
            "errors": errors
        }
    }

    # ---------------------------------------------------
    # 📜 5. Update history (audit trail)
    # ---------------------------------------------------
    history = old.get("history", [])

    history.append({
        "event": "replan",
        "failed_steps": failed_steps,
        "errors": errors,
        "retrieved_memory_count": len(retrieved_memory)
    })

    # ---------------------------------------------------
    # 🔁 6. Build new state
    # ---------------------------------------------------
    return State(
        execution_id=eval_result["execution_id"],
        incident_id=eval_result["incident_id"],

        # 🔥 new DAG
        plan=new_plan,

        # 🧠 enriched memory
        memory=merged_memory,

        # 📜 audit trail
        history=history,

        # 🔁 retry tracking
        retry_count=old.get("retry_count", 0) + 1
    )