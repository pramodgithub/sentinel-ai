from app.core.shared_store import append_thinking_trace

class RunbookAgent:

    def run(self, state):

        runbook = {
            "incident": state.incident["description"],
            "diagnosis": state.diagnosis,
            "actions": state.plan
        }

        #print("Runbook generated:")
        #print(runbook)
        
        append_thinking_trace(state.execution_id, {
            "agent": "runbookAgent",
            "step": "runbook_generation",
            "input": state.incident,
            "decision": "Generate runbook based on incident and diagnosis",
            "output": runbook
        })

        return state