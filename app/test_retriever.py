from agents.retriever_agent import RetrieverAgent
from core.state import ExecutionState

state = ExecutionState(
    goal="What are carry forward leave rules?"
)

agent = RetrieverAgent()

state = agent.run(state)

print(state.retrieved_docs)