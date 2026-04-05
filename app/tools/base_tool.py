
class BaseTool:

    name = "base_tool"

    def execute(self, state):
        raise NotImplementedError