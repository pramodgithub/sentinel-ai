import json

from app.core.capability_registry import CapabilityRegistry
from app.llm.router import ModelRouter
from app.llm.prompts.planner_prompt import build_planner_prompt
from app.services.audit_service import AuditService
from app.agents.base_agent import BaseAgent
from app.core.shared_store import append_thinking_trace
from app.core.dag import compute_levels

router = ModelRouter()
registry = CapabilityRegistry()
audit = AuditService()


class PlannerAgent(BaseAgent):

    def run(self, state):

        memories = state.similar_incidents or []
        allowed_actions = registry.list_actions()

        prompt = build_planner_prompt(
            state.incident,
            state.diagnosis,
            allowed_actions,
            memories
        )

        result = router.generate(prompt)
        response = result["text"]

        # Store metrics
        llm_metrics = {
            "agent":            "plannerAgent",   # set per agent
            "provider":         result["provider"],
            "model":            result["model"],
            "input_tokens":     result["input_tokens"],
            "output_tokens":    result["output_tokens"],
            "total_tokens":     result["total_tokens"],
            "latency_ms":       result["latency_ms"],
            "context_window_pct": round((result["input_tokens"] / 128000) * 100, 2),  # adjust per model
            "fallback_used":    result.get("fallback", False),
        }

        # --- Step 1: Parse response safely ---
        try:
            parsed = json.loads(response)
            
            # Case 1: wrapped response
            if "plan" in parsed:
                plan = parsed["plan"]
            else:
                plan = parsed

        except Exception:
            plan = {
                "nodes": ["inspect_metrics", "check_logs"],
                "edges": []
            }

        # --- Step 2: Normalize to DAG format ---
        if isinstance(plan, list):
            plan = {
                "nodes": plan,
                "edges": []
            }

        elif isinstance(plan, dict):

            # 🚨 CRITICAL: ensure correct structure
            if "nodes" not in plan or not isinstance(plan["nodes"], list):
                plan["nodes"] = []

            if "edges" not in plan or not isinstance(plan["edges"], list):
                plan["edges"] = []

        else:
            plan = {
                "nodes": ["inspect_metrics", "check_logs"],
                "edges": []
            }

        print("[PLANNER FINAL PLAN]", plan)
        decision = plan.get("decision", "No decision provided")
        nodes = plan.get("nodes", [])
        edges = plan.get("edges", [])

        # --- Step 3: Validate nodes ---
        validated_nodes = []

        for step in plan["nodes"]:

            if isinstance(step, dict):
                action = step.get("action")
            else:
                action = step

            if action and registry.is_valid(action):
                validated_nodes.append(action)
            else:
                print(f"Removed invalid action from planner: {step}")

        # --- Step 4: Validate edges (only keep valid references) ---
        validated_edges = []
        valid_set = set(validated_nodes)

        for edge in edges:
            if (
                isinstance(edge, (list, tuple)) and
                len(edge) == 2 and
                edge[0] in valid_set and
                edge[1] in valid_set
            ):
                validated_edges.append(edge)

        # --- Step 5: Final normalized plan ---
        state.plan = {
            "decision": decision,
            "nodes": validated_nodes,
            "edges": validated_edges
        }

        append_thinking_trace(state.execution_id, {
            "agent": "planner",
            "step": "plan_generation",
            "input": state.incident,
            "decision": decision,
            "output": compute_levels(nodes, edges),
            "llm_metrics": llm_metrics
        })
        audit.log(
            state.execution_id,
            state.incident_id,
            "PlannerAgent",
            "generate_plan",
            "completed",
            {"plan": state.plan}

        )

        return state