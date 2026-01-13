from src.rag.prompt import SYSTEM_PROMPT, build_user_prompt


class QAChain:
    def __init__(self, retriever, llm_client):
        self.retriever = retriever
        self.llm = llm_client

    def answer(self, question: str) -> str:
        question_lower = question.lower()

        if ("list all" in question_lower or "what are the" in question_lower) and ("fund" in question_lower or "portfolio" in question_lower):
            if hasattr(self.retriever, "unique_funds") and self.retriever.unique_funds:
                return "The funds available in the dataset are:\n\n" + \
                    "\n".join(self.retriever.unique_funds)

        retrieval_result = self.retriever.retrieve(question)
        retrieved_docs = retrieval_result.get("docs", [])
        summary = retrieval_result.get("summary", "")

        # Prepare global information
        available_funds = ", ".join(self.retriever.unique_funds) if hasattr(self.retriever, "unique_funds") else "Unknown"
        
        if not retrieved_docs and not summary:
            full_context = f"No specific records found for this query.\n\nAvailable portfolios in database: {available_funds}"
        else:
            context = "\n\n".join(doc["text"] for doc in retrieved_docs)
            full_context = f"{context}\n\nSystem Data Summary:\n{summary}\n\nAll Available portfolios: {available_funds}"

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(full_context, question)},
        ]

        # Debug print
        print(f"DEBUG PROMPT SENT TO LLM:\n{messages}\n")

        response = self.llm.chat(messages)
        return response.strip()
