from random import choice, randint

from app.tools.base_tool import BaseTool


class scaleService(BaseTool):

    name = "scale_service"

    def execute(self, state, step):

        print(f"[{step}] Scaling service")
        
        success = randint(0, 100) > 20
        replicas = randint(2, 6)

        state.intermediate_results[step] = {
                        "status": "success" if success else "failure",
                        "confidence": 0.85 if success else 0.5,
                        "data": {
                            "replicas": replicas,
                            "scaling": "up"
                        },
                        "observations": f"Scaled service to {replicas} replicas" if success else "Scaling failed due to limit",
                        "recommended_next": "monitor_service"
                    }

        return state