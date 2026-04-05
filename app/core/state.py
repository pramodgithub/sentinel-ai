import uuid
from app.workers.shared_tasks import get_execution_results

class ExecutionState:

    def __init__(self):

        self.execution_id = str(uuid.uuid4())

        self.incident_id = None

        self.incident = None

        self.diagnosis = None

        self.plan = []

        self.intermediate_results = {}

        self.evaluation = None


 # ✅ Convert state → serializable dict
    def to_dict(self):
        results = get_execution_results(str(self.execution_id))
        
        return {
            "execution_id": self.execution_id,
            "incident_id": str(self.incident_id) if self.incident_id else None,
            "incident": self.incident,
            "diagnosis": self.diagnosis,
            "plan": self.plan,
            "intermediate_results": self.intermediate_results,
            "evaluation": self.evaluation,
            "live_results": results 
        }

    # ✅ Rebuild state from Celery payload
    @classmethod
    def from_dict(cls, data):

        state = cls()

        state.execution_id = data.get("execution_id")
        state.incident_id = data.get("incident_id")
        state.incident = data.get("incident")
        state.diagnosis = data.get("diagnosis")
        state.plan = data.get("plan", [])
        state.intermediate_results = data.get("intermediate_results", {})
        state.evaluation = data.get("evaluation")

        return state
        