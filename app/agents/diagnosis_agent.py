from app.llm.router import ModelRouter
from app.services.audit_service import AuditService
from app.agents.base_agent import BaseAgent
from app.core.shared_store import append_thinking_trace
from app.llm.prompts.diagnosis_prompt import build_diagnosis_prompt
router = ModelRouter()
audit = AuditService()


class DiagnosisAgent(BaseAgent):

    def run(self, state):

        memories = self.format_memories(state.similar_incidents)
        
        prompt = build_diagnosis_prompt(
            state.incident,
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

        try:
            import json
            diagnosis = json.loads(response)
        except:
            diagnosis = {
                "probable_cause": "Unknown issue",
                "confidence": 0.5
            }

        state.diagnosis = diagnosis
        append_thinking_trace(state.execution_id, {
            "agent": "diagnosis",
            "step": "root_cause_analysis",
            "input": state.incident,
            "retrieved_context": state.similar_incidents,
            "decision": state.diagnosis["probable_cause"],
            "confidence": state.diagnosis["confidence"],
            "llm_metrics": llm_metrics
        })
        audit.log(
            state.execution_id,
            state.incident_id,
            "DiagnosisAgent",
            "diagnose_incident",
            "completed",
            diagnosis
        )

        return state
    
    def format_memories(self, memories):
            formatted = []

            for m in memories[:3]:  # top 3 only
                formatted.append(
                                    f"""
                                    Incident: {m['incident']}
                                    Diagnosis: {m['diagnosis']}
                                    Outcome: {m['outcome']}
                                    Similarity Score: {round(1 - m['distance'], 2)}
                                    """
                                )

            return "\n---\n".join(formatted)