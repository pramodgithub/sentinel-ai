from agents.retriever_agent import RetrieverAgent
from agents.reasoning_agent import ReasoningAgent
from core.state import ExecutionState

state = ExecutionState(
    goal="What is AI governance?"
)

retriever = RetrieverAgent()
reasoner = ReasoningAgent()

state = retriever.run(state)
state = reasoner.run(state)

print("\nGoal:")
print(state.goal)

print("\nRetrieved Docs:")
print(state.retrieved_docs)

print("\nFinal Answer:")
print(state.final_answer)