class RiskAgent:

    def __init__(self):
        self.high_risk_actions = [
            "scale_cluster",
            "delete_database",
            "shutdown_cluster"
        ]

    def run(self, state):

        # --- Validate structure ---
        if not isinstance(state.plan, dict):
            raise ValueError(f"Invalid plan format: {state.plan}")

        nodes = state.plan.get("nodes", [])
        edges = state.plan.get("edges", [])

        # --- Filter risky actions ---
        safe_nodes = []

        for action in nodes:
            if action in self.high_risk_actions:
                print(f"Blocked high risk action: {action}")
                continue

            safe_nodes.append(action)

        # --- Rebuild edges (remove invalid references) ---
        safe_set = set(safe_nodes)
        safe_edges = []

        for edge in edges:
            if (
                isinstance(edge, (list, tuple)) and
                len(edge) == 2 and
                edge[0] in safe_set and
                edge[1] in safe_set
            ):
                safe_edges.append(edge)

        # --- Assign back ---
        state.plan = {
            "nodes": safe_nodes,
            "edges": safe_edges
        }

        return state