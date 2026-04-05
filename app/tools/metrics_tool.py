from random import choice, randint

from app.tools.base_tool import BaseTool


class MetricsTool(BaseTool):

    name = "inspect_metrics"

    def execute(self, state, step):

        metrics = {
                        "status": "success",
                        "confidence": 0.8,
                        "data": {
                            "cpu": randint(40, 95),
                            "memory": randint(30, 90)
                        }
                    }

        state.intermediate_results[step] = metrics

        print(f"[{step}] Metrics inspected")

        return state