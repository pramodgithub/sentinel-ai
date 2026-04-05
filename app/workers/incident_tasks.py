from app.core.shared_store import save_execution_state, save_incident_execution_mapping
from app.workers.celery_app import celery_app
from app.core.state import ExecutionState

from app.agents.diagnosis_agent import DiagnosisAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.executor_agent import ExecutorAgent
from app.agents.evaluator_agent import EvaluatorAgent
from app.agents.memory_agent import MemoryAgent
from app.agents.risk_agent import RiskAgent
from app.agents.learning_agent import LearningAgent
from app.agents.runbook_agent import RunbookAgent   

from app.services.incident_service import IncidentService

incident_service = IncidentService()


@celery_app.task(name="process_incident")
def process_incident(incident_id):

    # load incident from DB
    incident = incident_service.get_incident(incident_id)

    state = ExecutionState()

    state.incident_id = incident_id
    state.incident = incident

     # save initial state
    save_incident_execution_mapping(incident_id, state.execution_id) 
    save_execution_state(state.execution_id, state.to_dict())
    
    diagnosis = DiagnosisAgent()
    planner = PlannerAgent()
    executor = ExecutorAgent()
    evaluator = EvaluatorAgent()
    memory = MemoryAgent()
    risk = RiskAgent()
    learning = LearningAgent()
    runbook = RunbookAgent()

    state = memory.retrieve(state)
    save_execution_state(state.execution_id, state.to_dict())

    state = diagnosis.run(state)
    save_execution_state(state.execution_id, state.to_dict())

    state = planner.run(state)
    save_execution_state(state.execution_id, state.to_dict())

    state = risk.run(state)
    save_execution_state(state.execution_id, state.to_dict())

    state = executor.run(state)
    save_execution_state(state.execution_id, state.to_dict())

    # state = evaluator.run(state)

    # state = learning.run(state)

    # state = memory.store(state)

    # state = runbook.run(state)

    return {
        "execution_id": state.execution_id,
        "incident_id": state.incident_id,
        "diagnosis": state.diagnosis,
        "plan": state.plan,
        "evaluation": state.evaluation
    }