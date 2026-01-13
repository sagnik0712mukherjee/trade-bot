from openai import OpenAI
from config.config import LLM_MODEL_NAME


class OpenAIClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")

        self.client = OpenAI(api_key=api_key)

    def chat(self, messages: list[dict]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=LLM_MODEL_NAME,
                messages=messages
            )
            content = response.choices[0].message.content
            print(f"LLM RESPONSE:\n{content}\n")
            return content
        except Exception as e:
            error_msg = f"Error calling OpenAI API: {str(e)}"
            print(f"\n!!! {error_msg} !!!\n")
            return f"I encountered an error while trying to reach the AI model: {str(e)}"
