from random import choice, randint

from app.tools.base_tool import BaseTool


class alertHuman(BaseTool):

    name = "alert_human"

    def execute(self, state, step):

        print(f"[{step}] Alerting human")
        
        acknowledged = randint(0, 100) > 30

        state.intermediate_results[step] = {
                        "status": "success",
                        "confidence": 0.95,
                        "data": {
                            "alert_sent": True,
                            "acknowledged": acknowledged
                        },
                        "observations": "Human alerted" + (" and acknowledged" if acknowledged else " but not yet acknowledged"),
                        "recommended_next": "wait_for_manual_intervention"
                    }

        return state