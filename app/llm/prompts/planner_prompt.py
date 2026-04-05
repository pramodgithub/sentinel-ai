def build_planner_prompt(incident, diagnosis, actions, memories):

    memory_context = ""

    for m in memories:
        memory_context += f"""
            Previous Incident:
            {m['incident']}

            Actions Taken:
            {m['actions']}

            Outcome:
            {m['outcome']}
            """

    actions_list = "\n".join(actions)

    return f"""
            You are an AI SRE (Site Reliability Engineering) planner responsible for resolving production incidents.

            Incident Details:
            {incident}

            Diagnosis Summary:
            {diagnosis}

            Available Actions:
            {actions_list}

            Relevant Past Incidents (Memory):
            {memory_context}

            Your task is to generate an execution plan as a Directed Acyclic Graph (DAG).

            Planning Guidelines:
            - Prefer low-risk and reversible actions first.
            - Run independent diagnostic actions in parallel where possible.
            - Ensure remediation actions depend on relevant diagnostics.
            - Avoid unnecessary or redundant steps.
            - If confidence in diagnosis is low, include additional verification steps.
            - Include monitoring after any remediation action.
            - Escalate to "alert_human" if:
            - multiple remediation attempts fail
            - or confidence remains low after retries

            Output Requirements:
            - Return ONLY valid JSON
            - Do NOT include explanations

            Expected Format:
            {{
                "decision": "Brief explanation of the plan and why",
                "nodes": ["action1", "action2", "action3"],
                "edges": [["action1", "action2"], ["action2", "action3"]]
            }}
            """