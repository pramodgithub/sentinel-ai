from core.state import ExecutionState
from core.event_log import EventLogger
from llm.router import ModelRouter
import json

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

                Your job is to create an execution plan using ONLY the available system capabilities.

                Available capabilities:
                - retrieve_policy_documents
                - analyze_policy_rules
                - generate_answer

                User Question:
                {state.goal}

                Rules:
                - Use only the capabilities listed above
                - Do not invent new steps
                - Do not include explanations
                - Do not number the steps

                Return ONLY valid JSON in this format:

                {{
                "plan":[
                "retrieve_policy_documents",
                "analyze_policy_rules",
                "generate_answer"
                ]
                }}
                """

        response = self.llm.generate(prompt)

        plan = json.loads(response)["plan"]
        state.plan = plan

        self.logger.log(
            state.execution_id,
            "PLANNER_COMPLETED",
            {"plan": plan}
        )

        return state