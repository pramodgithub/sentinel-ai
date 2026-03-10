from core.state import ExecutionState
from core.event_log import EventLogger
from llm.router import ModelRouter


class PlannerAgent:

    def __init__(self):
        self.llm = ModelRouter()
        self.logger = EventLogger()

    def run(self, state: ExecutionState):

        self.logger.log(
            state.execution_id,
            "PLANNER_STARTED",
            {"goal": state.goal}
        )

        prompt = f"""
                You are the planning agent of an AI system.

                You must create an execution plan using ONLY the available system capabilities.

                Available capabilities:
                - retrieve_policy_documents
                - analyze_policy_rules
                - generate_answer

                User Question:
                {state.goal}

                Rules:
                - Use ONLY the available capabilities
                - Return 3 or fewer steps
                - Each step must start with the capability name
                - Do not suggest human actions like contacting HR

                Return only the numbered plan.
                """

        response = self.llm.generate(prompt)

        plan = [
            step.strip()
            for step in response.split("\n")
            if step.strip()
        ]

        state.plan = plan

        self.logger.log(
            state.execution_id,
            "PLANNER_COMPLETED",
            {"plan": plan}
        )

        return state