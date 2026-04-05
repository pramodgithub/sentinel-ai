from random import choice, randint

from app.tools.base_tool import BaseTool


class rollbackDeployment(BaseTool):

    name = "rollback_deployment"

    def execute(self, state, step):

        print(f"[{step}] Rolling back deployment")
        
        success = randint(0, 100) > 25

        state.intermediate_results[step] = {
                        "status": "success" if success else "failure",
                        "confidence": 0.88 if success else 0.45,
                        "data": {
                            "version": "previous_stable",
                            "rollback": success
                        },
                        "observations": "Rollback successful" if success else "Rollback failed",
                        "recommended_next": "monitor_service" if success else "alert_human"
                    }

        return state