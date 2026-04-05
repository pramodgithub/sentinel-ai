from app.core.shared_store import append_thinking_trace

class LearningAgent:

    def run(self, state):

        learning_record = {
            "incident": state.incident,
            "diagnosis": state.diagnosis,
            "plan": state.plan,
            "results": state.intermediate_results,
            "evaluation": state.evaluation
        }

        if state.evaluation["resolved"]:
            learning_record["type"] = "successful_pattern"
        else:
            learning_record["type"] = "failure_pattern"

        #save_learning_pattern(learning_record)

        append_thinking_trace(state.execution_id, {
            "agent": "learningAgent",
            "step": "learning_generation",
            "input": state.incident,
            "decision": "If evaluation is resolved, label as successful_pattern, else failure_pattern",
            "output": learning_record
            
        })

        return state