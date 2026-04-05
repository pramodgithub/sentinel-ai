from random import choice, randint

from app.tools.base_tool import BaseTool


class closeIncident(BaseTool):

    name = "close_incident"

    def execute(self, state, step):

        print(f"[{step}] Closing incident")
        
        success = randint(0, 100) > 15
        state.intermediate_results[step] = {
                    "status": "success" if success else "failure",
                    "confidence": 0.95 if success else 0.4,
                    "data": {
                        "closed": success
                    },
                    "observations": "Incident closed successfully" if success else "Closure failed due to unresolved signals",
                    "recommended_next": None if success else "monitor_service"
                }

        return state