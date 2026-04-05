import time

from app.llm.router import ModelRouter
from app.services.audit_service import AuditService
from app.agents.base_agent import BaseAgent
from app.core.shared_store import append_thinking_trace
from app.llm.prompts.evaluator_prompt import build_evaluator_prompt
from app.services.helper_services import compute_llm_metrics

router = ModelRouter()
audit = AuditService()



class EvaluatorAgent(BaseAgent):

    def run(self, state):

        prompt = build_evaluator_prompt(
            state.incident,
            state.diagnosis,
            state.plan,
            state.intermediate_results
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

        try:
            import json
            evaluation = json.loads(response)
        except:
            evaluation = {
                "resolved": False,
                "confidence": 0.5,
                "recommendation": "Manual review required"
            }

        # --- Derive status (NEW) ---
        confidence = evaluation.get("confidence", 0.5)
        resolved = evaluation.get("resolved", False)
        obervations = evaluation.get("observations", "")

        if resolved and confidence >= 0.75:
            status = "resolved"
        elif confidence >= 0.5:
            status = "partial"
        else:
            status = "failed"

        # --- Enrich evaluation (NEW) ---
        enriched_evaluation = {
            "resolved": resolved,
            "status": status,
            "confidence": round(confidence, 2),
            "recommendation": evaluation.get("recommendation"),
            "observations": obervations,
            "timestamp": time.time()
        }

        # --- Update state (IMPORTANT CHANGE) ---
        state.evaluation = enriched_evaluation

        # --- Optional: keep raw response for audit/debug ---
        state.evaluation_raw = response

        # --- Thinking trace ---
        append_thinking_trace(state.execution_id, {
            "agent": "evaluation",
            "step": "post_execution_analysis",
            "decision": enriched_evaluation["recommendation"],
            "confidence": enriched_evaluation["confidence"],
            "status": enriched_evaluation["status"],
            "llm_metrics": llm_metrics
        })

        # --- Audit log ---
        audit.log(
            state.execution_id,
            state.incident_id,
            "EvaluatorAgent",
            "evaluate_resolution",
            "completed",
            enriched_evaluation
        )

        # --- LLM Metrics ---
        metrics = compute_llm_metrics(state.execution_id, llm_metrics.get("model", "unknown"))  
        state.evaluation["llm_metrics"] = metrics

        return state