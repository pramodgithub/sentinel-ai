from llm.router import ModelRouter


class ReasoningAgent:

    def __init__(self):
        self.llm = ModelRouter()

    def run(self, state):

        question = state.goal
        docs = state.retrieved_docs

        context = "\n\n".join([doc["chunk"] for doc in docs])

        prompt = f"""
                    You are an AI governance assistant.

                    Answer the question using ONLY the provided policy context.

                    If the answer is not present in the context, say:
                    "I could not find this information in the policy documents."

                    Policy Context:
                    {context}

                    Question:
                    {question}

                    Answer in clear sentences using the policy information.
                    """

        response = self.llm.generate(prompt)

        state.final_answer = response
        state.intermediate_results["reasoning"] = response

        return state