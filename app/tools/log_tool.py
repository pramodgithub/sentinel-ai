from random import choice, randint

from app.tools.base_tool import BaseTool


class LogTool(BaseTool):

    name = "check_logs"

    def execute(self, state, step):

        scenarios = [
                        {"error": "timeout error", "confidence": 0.9},
                        {"error": "memory leak detected", "confidence": 0.85},
                        {"error": "no issue", "confidence": 0.6},
                        {"error": "disk I/O spike", "confidence": 0.75}
                    ]
        logs = choice(scenarios)

        state.intermediate_results[step] = logs

        print(f"[{step}] Logs inspected")

        return state