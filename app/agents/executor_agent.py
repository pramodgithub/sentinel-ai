from app.workers.learning_task import learning_task
from app.workers.memory_store_task import memory_store_task

from app.workers.runbook_task import runbook_task

from app.workers.evaluation_tasks import evaluate_execution
from app.workers.shared_tasks import finalize_execution, handle_failure, passthrough, save_state_task
from celery import chord, group, chain
from app.workers.action_tasks import execute_action
from app.core.dag import compute_levels
from app.core.shared_store import clear_execution_results, append_thinking_trace



# -------------------------------------------------------------------
# Executor Agent
# -------------------------------------------------------------------

class ExecutorAgent:

    def run(self, state):

        clear_execution_results(state.execution_id)
        # ── 1. Normalize plan ──────────────────────────────────────
        if isinstance(state.plan, list):
            nodes = state.plan
            edges = []
        else:
            nodes = state.plan.get("nodes", [])
            edges = state.plan.get("edges", [])

        print(f"[EXECUTOR] nodes={nodes} edges={edges}")

        # ── 2. Compute DAG levels ─────────────────────────────────
        levels = compute_levels(nodes, edges)
        
        print(f"[EXECUTOR] levels={levels}")
        print(f"[EXECUTOR] level[0] type={type(levels[0])}") 
        

        if not levels:
            return state

        # ── 3. Build lazy workflow (IMPORTANT) ─────────────────────
        chain_parts = []

        for i, level in enumerate(levels):

            sigs = [
                execute_action.si(
                    step,
                    state.execution_id,
                    state.incident_id,
                    state.to_dict()
                ).set(headers={"step_id": step})
                for step in level
            ]

            if not sigs:
                continue

            level_group = group(sigs)

            # LAST level → finalize
            if i == len(levels) - 1:
                body = chain(
                        finalize_execution.s(
                            execution_id=state.execution_id,
                            incident_id=state.incident_id
                        ),
                        evaluate_execution.s(
                            execution_id=state.execution_id,
                            incident_id=state.incident_id,
                            state_dict=state.to_dict()
                        ),
                        save_state_task.s(),          # ← save after evaluate
                        learning_task.s(),
                        save_state_task.s(),          # ← save after learning
                        memory_store_task.s(),
                        save_state_task.s(),          # ← save after memory
                        runbook_task.s(),
                        save_state_task.s()           # ← save after memory
                    )
            else:
                body = passthrough.s()

            # ✅ ALWAYS chord (never raw group in chain)
            level_chord = chord(level_group, body)

            chain_parts.append(level_chord)

        if not chain_parts:
            return state

        # Build full workflow lazily
        workflow = chain(*chain_parts)

        # ── 4. Execute once ────────────────────────────────────────
        workflow.apply_async(
            link_error=handle_failure.s(
                execution_id=state.execution_id,
                incident_id=state.incident_id
            )
        )

        print(f"[EXECUTOR] Workflow dispatched for execution={state.execution_id}")
        return state