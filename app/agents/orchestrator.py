from app.tools.tool_registry import ToolRegistry


class Orchestrator:

    def __init__(self):

        self.tool_registry = ToolRegistry()

    def run(self, state):

        for step in state.plan:

            print(f"Executing step: {step}")

            tool = self.tool_registry.get_tool(step)

            if tool is None:
                raise Exception(f"No tool registered for step: {step}")

            state = tool.run(state)

        return state
