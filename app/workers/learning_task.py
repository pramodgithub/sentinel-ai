from app.agents.learning_agent import LearningAgent
from app.core.state import ExecutionState
from app.workers.celery_app import celery_app


@celery_app.task(name="learning_task")
def learning_task(state_dict):

    state = ExecutionState.from_dict(state_dict)

    learning = LearningAgent()

    state = learning.run(state)

    return state.to_dict()