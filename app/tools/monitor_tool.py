from random import choice, randint

from app.tools.base_tool import BaseTool


class MonitorTool(BaseTool):

    name = "monitor_service"

    def execute(self, state, step):

        print(f"[{step}] Monitoring service for stability")
        outcomes = [
                    ("healthy", 0.9),
                    ("recovering", 0.75),
                    ("still_unstable", 0.5),
                    ("down", 0.3)
                ]

        status, confidence = choice(outcomes)
        state.intermediate_results[step] = {
                            "status": "success",
                            "confidence": confidence,
                            "data": {
                                "service_status": status,
                                "latency_ms": randint(50, 500)
                            },
                            "observations": f"Service is {status}",
                            "recommended_next": "close_incident" if status == "healthy" else "restart_container"
                        }

        return state