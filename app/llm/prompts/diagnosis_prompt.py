def build_diagnosis_prompt(incident, memories):


   

    return f"""
            You are an expert AI SRE (Site Reliability Engineer) responsible for diagnosing production incidents.

            Incident Description:
            {incident}

            Relevant Past Incidents (ordered by similarity, lower distance = more relevant):
            {memories}

            Your task:
            - Analyze the current incident.
            - Compare it with similar past incidents.
            - Identify the most probable root cause.

            Guidelines:
            - Use past incidents to inform your reasoning, but do NOT blindly copy them.
            - Give higher weight to past incidents with:
            - lower distance (more similar)
            - successful outcomes
            - If past incidents had poor outcomes, reduce their influence.
            - Consider multiple possible causes if signals are conflicting.
            - If the data is insufficient or noisy, reflect uncertainty in confidence.

            Output Requirements:
            Return ONLY valid JSON with the following fields:

            {{
            "probable_cause": "short, clear root cause",
            "confidence": 0.0-1.0,
            "supporting_signals": [
                "key observation 1",
                "key observation 2"
            ],
            "similar_incident_reference": "brief note about most relevant past incident or null",
            "uncertainty_reason": "why confidence is not 1.0 (if applicable)"
            }}
            """