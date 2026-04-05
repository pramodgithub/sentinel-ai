from random import choice, randint

from app.tools.base_tool import BaseTool


class clearCache(BaseTool):

    name = "clear_cache"

    def execute(self, state, step):

        print(f"[{step}] Clearing cache")
        
        success = randint(0, 100) > 10

        state.intermediate_results[step] = {
                        "status": "success" if success else "failure",
                        "confidence": 0.9 if success else 0.6,
                        "data": {
                            "cache_cleared": success,
                            "latency_improvement": randint(10, 40) if success else 0
                        },
                        "observations": "Cache cleared, latency improved" if success else "Cache clear had no effect",
                        "recommended_next": "monitor_service"
                    }

        return state