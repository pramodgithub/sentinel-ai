from random import choice, randint

from app.tools.base_tool import BaseTool


class checkHealthEndpoint(BaseTool):

    name = "check_health_endpoint"

    def execute(self, state, step):

        print(f"[{step}] Checking health endpoint")
        outcomes = [
            ("ok", 0.9),
            ("degraded", 0.7),
            ("error", 0.4),
            ("timeout", 0.3)
        ]

        status, confidence = choice(outcomes)
        state.intermediate_results[step] = {
                        "status": "success",
                        "confidence": confidence,
                        "data": {
                            "health": status,
                            "response_time_ms": randint(100, 1500)
                        },
                        "observations": f"Health endpoint returned {status}",
                        "recommended_next": "restart_container" if status in ["error", "timeout"] else "monitor_service"
                    }

        return state