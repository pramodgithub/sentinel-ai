from random import choice, randint

from app.tools.base_tool import BaseTool


class RestartTool(BaseTool):

    name = "restart_container"

    def execute(self, state, step):
        success = randint(0, 100) > 20
       

        state.intermediate_results[step] = {
                "status": "success" if success else "failure",
                "confidence": 0.9 if success else 0.4,
                "data": {"action": "restart_attempted"}
            }
        print(f"[{step}] Container restarted (success={success})")
        return state